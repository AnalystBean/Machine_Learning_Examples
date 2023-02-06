import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

# Load the stock data into a pandas dataframe
df = pd.read_csv("stock_data.csv")

# Split the data into feature data and target data
X = df[['Open', 'High', 'Low', 'Volume']].values
y = df['Close'].values

# Split the data into training data and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train the Random Forest regressor model on the training data
rf_reg = RandomForestRegressor().fit(X_train, y_train)

# Use the trained Random Forest regressor to predict the stock price on the test data
rf_y_pred = rf_reg.predict(X_test)

# Create a simple neural network model
nn_model = Sequential()
nn_model.add(Dense(16, input_dim=4, activation='relu'))
nn_model.add(Dense(8, activation='relu'))
nn_model.add(Dense(1, activation='linear'))
nn_model.compile(loss='mean_squared_error', optimizer='adam')

# Train the neural network model on the training data
nn_model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)

# Use the trained neural network to predict the stock price on the test data
nn_y_pred = nn_model.predict(X_test).flatten()

# Combine the predictions of the Random Forest regressor and the neural network
y_pred = (rf_y_pred + nn_y_pred) / 2

# Evaluate the hybrid model
mse = np.mean((y_pred - y_test)**2)
print("Mean Squared Error: ", mse)