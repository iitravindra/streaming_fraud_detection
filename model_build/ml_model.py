# 1. Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from imblearn.over_sampling import SMOTE
import pickle

# 2. Load data
data = pd.read_csv('synthetic_fraud_data.csv')

# 3. Preprocess data
# Handle missing values, encode categorical variables, and scale numerical values

# 4. Feature and target separation
X = data.drop('is_fraud', axis=1)  # Features
y = data['is_fraud']  # Target

# 5. Handle class imbalance using SMOTE
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X, y)

# 6. Split data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2, random_state=42)

# 7. Train a model (Random Forest in this example)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 8. Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
print(f'ROC AUC Score: {roc_auc_score(y_test, y_pred)}')

# Save the trained model to a file

with open('fraud_detection_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)
print("Model saved as fraud_detection_model.pkl")