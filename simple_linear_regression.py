import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pyodbc

# Import
df = pd.read_excel("rates.xlsx", usecols=["origin", "destination", "weight", "rate"])

# Numpy
X = df[["origin", "destination", "weight"]].values
y = df["rate"].values

# DATA In To Training Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train VIA LRM
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction via Test Set
y_pred = model.predict(X_test)

# Eval Mean with SEM
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Convert to DF
predictions_df = pd.DataFrame({'predicted_rate': y_pred})

# ASD Connection
server = ''
database = ''
username = ''
password = ''
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

#DF to ASD
predictions_df.to_sql('predictions', cnxn, if_exists='replace')