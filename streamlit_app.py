import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Tampilkan judul
st.title('Aplikasi Prediksi Saham')

# Menampilkan data saham
st.subheader('Data Saham')
st.write(df)

# Menampilkan grafik prediksi
plt.figure(figsize=(16, 6))
for stock, data in data_dict.items():
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=len(future_predictions[stock]) + 1, freq='B')[1:]
    future_data = pd.Series(future_predictions[stock], index=future_dates)
    plt.plot(data.index, data['Close'], label=f'{stock} Actual')
    plt.plot(future_data.index, future_data, label=f'{stock} Future Prediction')
    
    if future_data[-1] > future_data[-2]:
        plt.annotate('↑', (future_data.index[-1], future_data.values[-1]), color='g', fontsize=30, ha='center', va='center')
    else:
        plt.annotate('↓', (future_data.index[-1], future_data.values[-1]), color='r', fontsize=30, ha='center', va='center')

    plt.title('Predictions for the Future')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    st.pyplot(plt)

# Menampilkan data aktual dan prediksi
st.subheader('Data Aktual dan Prediksi')
for stock, data in data_dict.items():
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=len(future_predictions[stock]) + 1, freq='B')[1:]
    future_data = pd.Series(future_predictions[stock], index=future_dates)
    combined_data = pd.concat([data, future_data], axis=1)
    st.write(f'\nData aktual dan prediksi untuk {stock}:')
    st.write(combined_data)
