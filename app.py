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
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=11)
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

# --- Прогноз PM2.5 ---
st.subheader("Прогноз PM2.5")
df_sorted = df.sort_values('datetime')
df_sorted['timestamp'] = df_sorted['datetime'].map(pd.Timestamp.timestamp)
X = df_sorted[['timestamp']]
y = df_sorted['PM2.5']
model = LinearRegression()
model.fit(X, y)

future_times = pd.date_range(df_sorted['datetime'].max(), periods=10, freq='H')
future_timestamps = np.array([t.timestamp() for t in future_times]).reshape(-1,1)
forecast = model.predict(future_timestamps)

forecast_df = pd.DataFrame({
    'datetime': future_times,
    'PM2.5': forecast
})

fig_forecast = px.line(forecast_df, x='datetime', y='PM2.5', title="Прогноз PM2.5")
st.plotly_chart(fig_forecast)
