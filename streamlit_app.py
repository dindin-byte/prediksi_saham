import streamlit as st
import pandas as pd
import plotly.express as px

# Tampilkan judul
st.title('Aplikasi Prediksi Saham')

# Menampilkan data saham
st.subheader('Data Saham')
st.write(df)

# Menampilkan grafik prediksi
for stock, data in data_dict.items():
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=len(future_predictions[stock]) + 1, freq='B')[1:]
    future_data = pd.Series(future_predictions[stock], index=future_dates)

    fig = px.line(data, x=data.index, y=data['Close'], title=f'{stock} Actual')
    fig.add_scatter(x=future_data.index, y=future_data.values, mode='lines', name=f'{stock} Future Prediction')
    
    if future_data[-1] > future_data[-2]:
        fig.add_annotation(x=future_data.index[-1], y=future_data.values[-1], text='↑', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2)
    else:
        fig.add_annotation(x=future_data.index[-1], y=future_data.values[-1], text='↓', showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2)

    st.plotly_chart(fig)

# Menampilkan data aktual dan prediksi
st.subheader('Data Aktual dan Prediksi')
for stock, data in data_dict.items():
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=len(future_predictions[stock]) + 1, freq='B')[1:]
    future_data = pd.Series(future_predictions[stock], index=future_dates)
    combined_data = pd.concat([data, future_data], axis=1)
    st.write(f'\nData aktual dan prediksi untuk {stock}:')
    st.write(combined_data)
