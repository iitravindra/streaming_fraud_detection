from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType,TimestampType,BooleanType
from pyspark.sql.functions import from_json, col, hour, lit,udf
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier  # Example model, replace with your model
import psycopg2  # PostgreSQL driver
from psycopg2 import sql
import numpy as np
from datetime import datetime, timedelta


# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaFraudDetection") \
    .getOrCreate()

# PostgreSQL connection setup
def get_db_connection():
    connection = psycopg2.connect(
        host="timescaledb",  # Update with the correct Docker service name or IP
        database="fraud_detection",
        user="user", 
        password="password"
    )
    return connection

# Read `account_details` table from TimescaleDB running in Docker
def get_timescale_connection():
    return {
        "url": "jdbc:postgresql://timescaledb:5432/fraud_detection",
        "driver": "org.postgresql.Driver",
        "user": "user",  
        "password": "password",
        "dbtable": "account_details"
    }

# Define schema of transaction data (adjust according to your data)
schema = StructType([
    StructField("account_id", IntegerType(), True),
    StructField("transaction_amount", DoubleType(), True),
    StructField("transaction_time", TimestampType(), True),
    StructField("location", StringType(), True),
    StructField("transaction_method", StringType(), True),
    StructField("user_transactions_last_24h", IntegerType(), True),
])

# Load pre-trained model (from scikit-learn)
with open('fraud_detection_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)


# Step 5: UDF to run fraud detection inference
@udf(BooleanType())
def detect_fraud_udf(transaction_amount, transaction_hour, account_age, user_transactions_last_24h):
    # Prepare a dictionary for a single transaction
    transaction = {
        'transaction_amount': transaction_amount,
        'transaction_hour': transaction_hour,
        'account_age': account_age,
        'user_transactions_last_24h': user_transactions_last_24h
    }

    # Ensure all model features are present
    model_features = ['transaction_amount', 'transaction_hour', 'account_age',
                      'user_transactions_last_24h']

    # Add missing features as 0 (for one-hot encoded fields)
    for feature in model_features:
        if feature not in transaction:
            transaction[feature] = 0

    # Convert to a DataFrame for prediction
    transaction_df = pd.DataFrame([transaction])
    
    # Perform fraud detection using pre-trained model
    is_fraud = model.predict(transaction_df)[0]
    return bool(is_fraud)


# Read streaming data from Kafka
transaction_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "raw_transactions") \
    .load()

# Deserialize Kafka value (transaction data is in JSON format)
transaction_data = transaction_stream.selectExpr("CAST(value AS STRING)")
transaction_json = transaction_data.select(from_json(col("value"), schema).alias("transaction_data"))

# Convert the JSON into individual columns
transaction_df = transaction_json.select("transaction_data.*")

# Load the account_details table into a DataFrame
account_details_df = spark.read \
    .format("jdbc") \
    .option("url", get_timescale_connection()['url']) \
    .option("dbtable", get_timescale_connection()['dbtable']) \
    .option("user", get_timescale_connection()['user']) \
    .option("password", get_timescale_connection()['password']) \
    .option("driver", get_timescale_connection()['driver']) \
    .load()

# caching the DF as we are going to use it multiple times
account_details_df.cache()

#Join `transaction_df` with `account_details_df` to get `account_age`
joined_df = transaction_df.join(account_details_df, "account_id") \
    .withColumn("account_age", (lit(datetime.now()) - col("signup_time")).cast("int") / 86400)  # Account age in days

# Extract transaction hour from `transaction_time`
joined_df = joined_df.withColumn("transaction_hour", hour("transaction_time"))

# modify and add later logic to calculate user_transactions_last_24h, Right now it's hardcode and coming from data producers.
# Ideally user_transactions_last_24h should be calculated by setting a counter of transctions.
#joined_df = joined_df.withColumn("user_transactions_last_24h", lit(0))

joined_df = joined_df.withColumn("is_fraud", detect_fraud_udf(
    col("transaction_amount"),
    col("transaction_hour"),
    col("account_age"),
    col("user_transactions_last_24h")
))

# Step 7: Write the result (including `is_fraud`) to the PostgreSQL (TimescaleDB) transactions table
def write_to_db(batch_df, batch_id):
    # Drop the 'signup_time' column from df.
    cleaned_batch_df = batch_df.drop("signup_time")
    # write df in the  transactions table in timescale db.
    cleaned_batch_df.write \
        .format("jdbc") \
        .option("url", get_timescale_connection()['url']) \
        .option("dbtable", "transactions") \
        .option("user", get_timescale_connection()['user']) \
        .option("password", get_timescale_connection()['password']) \
        .option("driver", get_timescale_connection()['driver']) \
        .mode("append") \
        .save()

# Apply processing and detect fraud in real-time
joined_df.writeStream \
    .foreachBatch(write_to_db) \
    .start() \
    .awaitTermination()
