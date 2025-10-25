import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

st.set_page_config(page_title="Екологічна аналітика", layout="wide")

st.title("Екологічна аналітика — Кам'янець-Подільський")

# 1. Завантаження даних з GitHub
URL = "https://raw.githubusercontent.com/OoverHeaven/ekologichna_analityka/main/data/air_quality.csv"
df = pd.read_csv(URL)

# 2. Відображення таблиці
st.subheader("Дані якості повітря")
st.dataframe(df)

# 3. Створення карти
st.subheader("Карта забруднення PM2.5")

center_lat = df["lat"].mean()
center_lon = df["lon"].mean()

map_sensor = folium.Map(location=[center_lat, center_lon], zoom_start=13)

for _, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=8,
        popup=f"{row['location']}: PM2.5 = {row['pm25']}",
        fill=True,
    ).add_to(map_sensor)

st_folium(map_sensor, width=700, height=500)

# 4. Аналіз тренду PM2.5
st.subheader("Тренд зміни PM2.5")

df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

plt.figure()
plt.plot(df["datetime"], df["pm25"])
plt.xlabel("Дата")
plt.ylabel("PM2.5")
plt.title("Тренд якості повітря")
plt.xticks(rotation=45)
st.pyplot(plt)

# 5. Простий прогноз PM2.5
st.subheader("Прогноз PM2.5 на наступні 5 годин")

df["hour"] = df["datetime"].dt.hour
model = LinearRegression()
model.fit(df[["hour"]], df["pm25"])

future_hours = np.array([[h] for h in range(24, 29)])
pred = model.predict(future_hours)

future_df = pd.DataFrame({
    "Година": future_hours.flatten(),
    "Прогноз PM2.5": pred
})

st.dataframe(future_df)
