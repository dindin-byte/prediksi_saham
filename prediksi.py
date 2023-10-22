import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import streamlit as st

st.title('Aplikasi Prediksi Saham Menggunakan LSTM')

# Mendapatkan data saham
ticker = st.text_input("Masukkan simbol saham (contoh: AAPL untuk Apple):")
data = yf.download(ticker, start="2010-01-01", end="2023-10-01")

# Menampilkan data
st.subheader('Data Saham')
st.write(data)

# Memproses data
data = data['Close']
dataset = data.values.reshape(-1, 1)
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# Membagi data menjadi data latih dan data uji
train_size = int(len(dataset) * 0.8)
test_size = len(dataset) - train_size
train_data, test_data = dataset[0:train_size, :], dataset[train_size:len(dataset), :]

# Membuat dataset untuk LSTM
def create_dataset(dataset, time_step=1):
    data_x, data_y = [], []
    for i in range(len(dataset) - time_step - 1):
        a = dataset[i:(i + time_step), 0]
        data_x.append(a)
        data_y.append(dataset[i + time_step, 0])
    return np.array(data_x), np.array(data_y)

time_step = 100
x_train, y_train = create_dataset(train_data, time_step)
x_test, y_test = create_dataset(test_data, time_step)

# Reshape data ke bentuk yang dapat diterima oleh LSTM
x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)

# Membangun model LSTM
model = Sequential()
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(units=50, return_sequences=True))
model.add(LSTM(units=50))
model.add(Dense(units=1))
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=100, batch_size=64)

# Melakukan prediksi
train_predict = model.predict(x_train)
test_predict = model.predict(x_test)

# Mengubah data kebentuk awal
train_predict = scaler.inverse_transform(train_predict)
test_predict = scaler.inverse_transform(test_predict)

# Plot hasil prediksi
st.subheader('Hasil Prediksi Saham')
st.line_chart(data)

# Menampilkan prediksi pada data uji
st.subheader('Prediksi pada Data Uji')
test_data = data[len(data) - len(test_data):]
test_data['Predictions'] = test_predict
st.line_chart(test_data[['Close', 'Predictions']])
