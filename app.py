import streamlit as st
import requests
import base64
from datetime import datetime

st.set_page_config(page_title="🌦 Weather Breathing Lamp", layout="centered")

API_KEY = "f79b327c6e33c90c48948f41a5b62e38"

# ======================
# 获取未来天气（关键）
# ======================
def get_forecast(city):
    url = (
        "https://api.openweathermap.org/data/2.5/forecast"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    return requests.get(url).json()

def decide_weather_type(data):
    forecast_list = data.get("list", [])

    # 只看未来 24 小时（8 个 3h 数据）
    next_24h = forecast_list[:8]

    for item in next_24h:
        wid = item["weather"][0]["id"]

        if "snow" in item or 600 <= wid <= 622:
            return "snow"
        if "rain" in item or 500 <= wid <= 531 or 300 <= wid <= 321:
            return "rain"

    # 如果未来 24 小时都没降水，再看最近一次
    wid = forecast_list[0]["weather"][0]["id"]

    if wid == 800:
        return "clear"
    return "clouds"

def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def play_music(audio_file):
    with open(audio_file, "rb") as audio:
        st.audio(audio.read(), format="audio/mp3", autoplay=True)

# ======================
# UI
# ======================
st.title("🌦 Weather Breathing Lamp")
city = st.text_input("请输入城市名")

if city:
    data = get_forecast(city)

    if data.get("cod") != "200":
        st.error("无法获取城市天气")
        st.stop()

    weather_type = decide_weather_type(data)

    theme = {
        "clear":  {"color": "#FFD700", "bg": "clear.jpg",  "music": "clear.mp3"},
        "clouds":{"color": "#B0C4DE", "bg": "clouds.jpg","music": "clouds.mp3"},
        "rain":  {"color": "#4A90E2", "bg": "rain.jpg",  "music": "rain.mp3"},
        "snow":  {"color": "#E6F7FF", "bg": "snow.jpg",  "music": "snow.mp3"},
    }

    current = theme[weather_type]

    set_background(current["bg"])

    lamp_color = current["color"]
    st.markdown(
        f"""
        <div style="
            width:320px;
            height:320px;
            margin: 50px auto 15px;
            border-radius:50%;
            background: radial-gradient(circle, {lamp_color} 0%, rgba(0,0,0,0) 70%);
            box-shadow: 0 0 80px {lamp_color};
            animation: breathe 3s ease-in-out infinite;
        "></div>

        <style>
        @keyframes breathe {{
            0% {{ transform: scale(1); box-shadow: 0 0 40px {lamp_color}; }}
            50% {{ transform: scale(1.12); box-shadow: 0 0 120px {lamp_color}; }}
            100% {{ transform: scale(1); box-shadow: 0 0 40px {lamp_color}; }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    now = data["list"][0]
    desc = now["weather"][0]["description"]
    temp = now["main"]["temp"]

    st.markdown(
        f"""
        <div style="
            text-align:center;
            color:white;
            background: rgba(0,0,0,0.35);
            padding:10px;
            border-radius:12px;
            width:260px;
            margin:0 auto;
        ">
            <b>{data['city']['name']}</b><br>
            {desc}<br>
            {temp:.1f} ℃
        </div>
        """,
        unsafe_allow_html=True
    )

    play_music(current["music"])
