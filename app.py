import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import folium
from streamlit_folium import st_folium

# Заголовок додатку
st.title("Екологічна аналітика – Кам'янець-Подільський")

# Завантаження даних з GitHub RAW
DATA_URL = "https://raw.githubusercontent.com/OoverHeaven/ekologichna_analityka/main/data/air_quality.csv"
df = pd.read_csv(DATA_URL)

# Перейменовуємо у зручніші назви
df["lat"] = df["latitude"]
df["lng"] = df["longitude"]

# Центр карти
center_lat = df["lat"].mean()
center_lng = df["lng"].mean()

# Карта забруднення
st.header("Карта забруднення")
m = folium.Map(location=[center_lat, center_lng], zoom_start=13)

for i, row in df.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lng"]],
        radius=row["PM2.5"] / 2,
        popup=f"PM2.5: {row['PM2.5']}",
        fill=True
    ).add_to(m)

st_folium(m, width=700, height=500)

# Аналіз трендів
st.header("Тренд PM2.5")
df["datetime"] = pd.to_datetime(df["datetime"])
df = df.sort_values("datetime")

plt.figure()
plt.plot(df["datetime"], df["PM2.5"])
plt.xlabel("Дата та час")
plt.ylabel("PM2.5")
plt.title("Динаміка забруднення PM2.5")
st.pyplot(plt)

# Прогноз PM2.5 (лінійна регресія)
st.header("Прогноз PM2.5")
model = LinearRegression()
df["time_index"] = range(len(df))
model.fit(df[["time_index"]], df["PM2.5"])
future_index = pd.DataFrame({"time_index": range(len(df), len(df) + 5)})
future_pred = model.predict(future_index)

st.write("Прогноз на наступні 5 вимірювань:")
st.write(future_pred)
