CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,       -- Auto-incrementing primary key
    account_id INTEGER,                      -- Account ID, either 11111 or 22222
    transaction_amount FLOAT,               -- Transaction amount
    transaction_time TIMESTAMP,         -- Timestamp of the transaction
    location VARCHAR,                        -- Location of the transaction
    transaction_method VARCHAR,              -- Payment method (Credit Card, Bank Transfer, etc.)
    account_age INTEGER,                     -- account age in days
    transaction_hour INTEGER,                -- Hour of transaction
    user_transactions_last_24h INTEGER,       -- transaction in last 24 hours
    is_fraud BOOLEAN                         -- Indicator of whether the transaction is fraudulent
);

CREATE TABLE account_details (
    account_id INTEGER PRIMARY KEY,   -- Unique account ID
    signup_time TIMESTAMP             -- Signup time for the account
);

INSERT INTO account_details (account_id, signup_time)
VALUES
(11111, TIMESTAMP '2022-09-18 14:35:22'),  -- Example random date 2 years ago
(22222, TIMESTAMP '2021-08-05 09:15:37');  -- Another random date 3 years ago