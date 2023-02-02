import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load the loan data
loan_data = pd.read_csv("loan_data.csv")

# Split the data into features (X) and target (y)
X = loan_data.drop("loan_status", axis=1)
y = loan_data["loan_status"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate the model on the test data
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

# Predict the loan status for a new loan application
new_loan_application = pd.DataFrame({"loan_amount": [100000],
                                     "annual_income": [100000],
                                     "credit_score": [700]})

prediction = model.predict(new_loan_application)
print("Loan Status Prediction:", prediction)