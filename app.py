import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from sklearn.linear_model import LinearRegression
import numpy as np

st.title("Екологічна аналітика")

# --- Завантаження даних ---
df = pd.read_csv("data/air_quality.csv")
df['datetime'] = pd.to_datetime(df['datetime'])

# --- Карта забруднення ---
st.subheader("Карта забруднення")
m = folium.Map(location=[48.685, 26.588], zoom_start=13)  # Центр Кам'янця-Подільського
for i, row in df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=7,
        color="red" if row['PM2.5']>35 else "green",
        fill=True,
        fill_opacity=0.7,
        popup=f"PM2.5: {row['PM2.5']}"
    ).add_to(m)

st_folium(m, width=700, height=500)

# --- Аналіз трендів ---
st.subheader("Тренди PM2.5")
fig = px.line(df, x='datetime', y='PM2.5', title="Динаміка PM2.5")
st.plotly_chart(fig)

import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px
import streamlit as st

# --- Створення колонки для тренду часу ---
df['time_index'] = range(len(df))

# --- Модель лінійної регресії ---
X = df[['time_index']]
y = df['PM2.5']

model = LinearRegression()
model.fit(X, y)

# --- Прогноз на наступні 10 годин ---
future_index = pd.DataFrame({'time_index': range(len(df), len(df)+10)})
future_timestamps = pd.date_range(start=df['datetime'].iloc[-1] + pd.Timedelta(hours=1), periods=10, freq='H')
future_pred = model.predict(future_index)

forecast_df = pd.DataFrame({
    'datetime': future_timestamps,
    'PM2.5': future_pred
})

# --- Візуалізація ---
st.subheader("Прогноз PM2.5 на 10 годин вперед для Кам'янця-Подільського")
fig_forecast = px.line(forecast_df, x='datetime', y='PM2.5', markers=True)
st.plotly_chart(fig_forecast)
