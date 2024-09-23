import pandas as pd
import numpy as np

# Set the random seed for reproducibility
np.random.seed(42)

# Number of samples to generate
num_samples = 10000

# Generate features
data = pd.DataFrame({
    'transaction_amount': np.random.uniform(1, 1000, num_samples),  # Transaction amount between 1 and 1000
    'transaction_hour': np.random.randint(0, 24, num_samples),  # Hour of the day
    'account_age': np.random.randint(1, 3650, num_samples),  # Account age in days (up to 10 years)
    'user_transactions_last_24h': np.random.randint(0, 5, num_samples),  # Number of transactions made by the user in the last 24 hours
})

# Assign fraud cases
fraud_indices = np.random.choice(num_samples, size=int(0.02 * num_samples), replace=False)  # 2% of data will be fraud
data['is_fraud'] = 0  # Set all transactions to non-fraud by default
data.loc[fraud_indices, 'is_fraud'] = 1  # Set fraud cases

# Adding some patterns to fraudulent cases

# Fraudulent transactions may have larger amounts and less frequent users
data.loc[fraud_indices, 'transaction_amount'] = np.random.uniform(500, 1000, len(fraud_indices))  # High transaction amounts
data.loc[fraud_indices, 'user_transactions_last_24h'] = np.random.randint(5, 10, len(fraud_indices))  # More frequent transactions in the last 24h
data.loc[fraud_indices, 'account_age'] = np.random.randint(1, 30, len(fraud_indices))  # Fraud from newer accounts

# Show the first few rows of the synthetic dataset
print(data.head())

# Save to CSV
data.to_csv('synthetic_fraud_data.csv', index=False)
