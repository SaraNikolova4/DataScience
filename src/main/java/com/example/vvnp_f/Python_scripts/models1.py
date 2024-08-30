import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# od tv
df = pd.read_csv(r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\Data_set\eurovision_1957-2021.csv')

df = df.drop(columns=['Unnamed: 0', 'Edition',])
df['Points type'] = df['Points type'].apply(lambda x: 1 if x == 'Points given by televoters' else 0)
df = df[df['Points type'] == 1]
df = df.drop(columns=['Points type'])

df4 = df[df['Year'] > 2008]


# Function to split data
def split_data(df):
    train_size = int(len(df) * 0.8)
    train, test = df[:train_size], df[train_size:]
    return train, test


train_df4, test_df4 = split_data(df4)

# Function to preprocess data for LSTM
def preprocess_data(df, feature_col='Points', time_steps=10):
    if feature_col not in df.columns:
        raise ValueError(f"Column '{feature_col}' does not exist in DataFrame")

    if df.empty:
        raise ValueError("The DataFrame is empty and cannot be processed")

    scaler = MinMaxScaler(feature_range=(0, 1))

    # Филтрирање на DataFrame за да се отстранат редовите со недостасувачки вредности во колоната 'Points'
    df_filtered = df.dropna(subset=[feature_col])

    if df_filtered.empty:
        raise ValueError("The DataFrame has no valid data after filtering for NaN values")

    scaled_data = scaler.fit_transform(df_filtered[[feature_col]])

    if len(scaled_data) < time_steps:
        raise ValueError(f"Not enough data points ({len(scaled_data)}) to create sequences with {time_steps} time steps")

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


pred_df4, true_df4, len_pred4 = train_predict_lstm(train_df4, test_df4)


result_df4 = test_df4[['From', 'To']].iloc[-len_pred4:].copy()
result_df4['Predicted_Points'] = pred_df4

# Function to calculate MSE
def calculate_mse(true_values, predictions):
    min_len = min(len(true_values), len(predictions))
    mse = mean_squared_error(true_values[:min_len], predictions[:min_len])
    return mse

mse_df4 = calculate_mse(true_df4[:len(result_df4['Predicted_Points'])], result_df4['Predicted_Points'])
print(f"MSE за периодот 2009-понатаму: {mse_df4}")


# Merging the results of df2, df3, df4
combined_df = pd.concat([result_df4])

# Grouping by 'From' and 'To' and calculating average predicted points
final_df = combined_df.groupby(['From', 'To']).agg({
    'Predicted_Points': 'mean'
}).reset_index()

# Convert in Integer
final_df['Predicted_Points'] = final_df['Predicted_Points'].round().astype(int)

# Save data_set
file_path = r'C:\Users\Lenovo\Desktop\VVNP_F\src\main\java\com\example\vvnp_f\New_DataSet\model_tv.csv'
directory = os.path.dirname(file_path)


