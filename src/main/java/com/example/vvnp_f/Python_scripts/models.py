import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima.model import ARIMA
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import os

# od ziri
df = pd.read_csv(r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\Data_set\eurovision_1957-2021.csv')

df = df.drop(columns=['Unnamed: 0', 'Edition',])
df['Points_type'] = df['Points type'].apply(lambda x: 1 if x == 'Points given by televoters' else 0)
df = df[df['Points_type'] == 0]
df = df.drop(columns=['Points_type'])

# Create the new datasets based on the specified intervals
df1 = df[(df['Year'] >= 1957) & (df['Year'] <= 1975)]
df2 = df[(df['Year'] > 1975) & (df['Year'] <= 2004)]
df3 = df[(df['Year'] > 2004) & (df['Year'] <= 2008)]
df4 = df[df['Year'] > 2008]


# Function to split data
def split_data(df):
    train_size = int(len(df) * 0.8)
    train, test = df[:train_size], df[train_size:]
    return train, test

train_df1, test_df1 = split_data(df1)
train_df2, test_df2 = split_data(df2)
train_df3, test_df3 = split_data(df3)
train_df4, test_df4 = split_data(df4)

# Function to train and predict using ARIMA
def train_predict_arima(train, test):
    predictions = []
    for country in test['From'].unique():
        country_train = train[train['From'] == country]['Points']
        country_test = test[test['From'] == country]['Points']

        if len(country_train) > 5:
            try:
                model = ARIMA(country_train, order=(5,1,0))
                model_fit = model.fit()
                forecast = model_fit.forecast(steps=len(country_test))
                predictions.extend(forecast)
            except Exception as e:
                print(f"Model fitting failed for {country}: {e}")
                predictions.extend([np.nan]*len(country_test))
        else:
            predictions.extend([np.nan]*len(country_test))

    return predictions

# Predicting for df1
pred_df1 = train_predict_arima(train_df1, test_df1)

# Create new DataFrame with From, To, Predicted_Points for df1
result_df1 = test_df1[['From', 'To']].iloc[:len(pred_df1)].copy()
result_df1['Predicted_Points'] = pred_df1

# Function to preprocess data for LSTM
def preprocess_data(df, feature_col='Points', time_steps=10):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[[feature_col]])

    X, y = [], []
    for i in range(time_steps, len(scaled_data)):
        X.append(scaled_data[i-time_steps:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y, scaler

# Function to build LSTM model
def build_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(units=50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Function to train and predict using LSTM
def train_predict_lstm(train, test, time_steps=10):
    X_train, y_train, scaler = preprocess_data(train, time_steps=time_steps)
    X_test, y_test, _ = preprocess_data(test, time_steps=time_steps)

    model = build_lstm_model((X_train.shape[1], 1))
    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)

    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)
    y_test = scaler.inverse_transform([y_test])

    return predictions, y_test[0], len(X_test)

# Predicting for df2, df3, df4
pred_df2, true_df2, len_pred2 = train_predict_lstm(train_df2, test_df2)
pred_df3, true_df3, len_pred3 = train_predict_lstm(train_df3, test_df3)
pred_df4, true_df4, len_pred4 = train_predict_lstm(train_df4, test_df4)

# Create new DataFrames with From, To, Predicted_Points for df2, df3, df4
result_df2 = test_df2[['From', 'To']].iloc[-len_pred2:].copy()
result_df2['Predicted_Points'] = pred_df2

result_df3 = test_df3[['From', 'To']].iloc[-len_pred3:].copy()
result_df3['Predicted_Points'] = pred_df3

result_df4 = test_df4[['From', 'To']].iloc[-len_pred4:].copy()
result_df4['Predicted_Points'] = pred_df4

# Function to calculate MSE
def calculate_mse(true_values, predictions):
    min_len = min(len(true_values), len(predictions))
    mse = mean_squared_error(true_values[:min_len], predictions[:min_len])
    return mse

# Calculate_MSE
mse_df1 = calculate_mse(test_df1['Points'].dropna(), result_df1['Predicted_Points'].dropna())
mse_df2 = calculate_mse(true_df2[:len(result_df2['Predicted_Points'])], result_df2['Predicted_Points'])
mse_df3 = calculate_mse(true_df3[:len(result_df3['Predicted_Points'])], result_df3['Predicted_Points'])
mse_df4 = calculate_mse(true_df4[:len(result_df4['Predicted_Points'])], result_df4['Predicted_Points'])

# Print_MSE
print(f"MSE за периодот 1957-1975: {mse_df1}")
print(f"MSE за периодот 1976-2004: {mse_df2}")
print(f"MSE за периодот 2005-2008: {mse_df3}")
print(f"MSE за периодот 2009-понатаму: {mse_df4}")


# Concat to df2, df3, df4
combined_df = pd.concat([result_df2, result_df3, result_df4])

# Group by From and To
final_df = combined_df.groupby(['From', 'To']).agg({
    'Predicted_Points': 'mean'
}).reset_index()

# Convert to Integer
final_df['Predicted_Points'] = final_df['Predicted_Points'].round().astype(int)

# Save a datasets
file_path = r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\New_DataSet\model_ziri.csv'
directory = os.path.dirname(file_path)


