import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pyodbc

# Import
df = pd.read_excel("rates.xlsx", usecols=["origin", "destination", "weight", "rate"])

# Numpy
X = df[["zip_code_origin", "zip_code_destination", "weight"]].values
y = df["rate"].values

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# RFM Model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Prediction Set
y_pred = model.predict(X_test)

# Eval Mean SEM
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Convert DF
predictions_df = pd.DataFrame({'predicted_rate': y_pred})

# Connect to ADB
server = ''
database = ''
username = ''
password = ''
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

# Insert DF to ADB
predictions_df.to_sql('predictions', cnxn, if_exists='replace')