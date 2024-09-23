import time
import random
from kafka import KafkaProducer
import json
import numpy as np
from datetime import datetime, timedelta


class TransactionProducer:
    def __init__(self, brokers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic
    # Function to generate random datetime between two datetime objects
    def produce_transactions(self):
        while True:
            transaction = {
            'account_id': random.choice([11111, 22222]),  # Ensures account_id is either 11111 or 22222
            'transaction_amount': round(np.random.uniform(1, 1000), 2),  # Transaction amount between 1 and 1000
            'transaction_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Current datetime in a PostgreSQL-friendly format
            'location': random.choice(['USA', 'Canada', 'UK', 'Germany', 'France', 'India', 'China']),
            'transaction_method': random.choice(['CreditCard', 'BankTransfer', 'PayPal', 'Cryptocurrency']),
            'user_transactions_last_24h': np.random.randint(0, 4)  # Number of transactions made by the user in the last 24 hours;[]
            }

            # Send transaction data to Kafka topic
            self.producer.send(self.topic, value=transaction)
            print(f"Produced: {transaction}")
            # Sleep for a certain interval before producing the next transaction
            time.sleep(1)

if __name__ == '__main__':
    brokers = ['broker:29092']
    topic = 'raw_transactions'

    producer = TransactionProducer(brokers, topic)
    producer.produce_transactions()