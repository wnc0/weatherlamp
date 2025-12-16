import streamlit as st
import requests
import base64

st.set_page_config(page_title="🌦 Weather Breathing Lamp", layout="centered")

API_KEY = "f79b327c6e33c90c48948f41a5b62e38"

# ======================
# 获取天气
# ======================
def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    return requests.get(url).json()

# ✅ 唯一正确判断方式：weather.id
def get_weather_type(data):
    wid = data["weather"][0]["id"]

    if 200 <= wid <= 232:
        return "rain"
    elif 300 <= wid <= 321:
        return "rain"
    elif 500 <= wid <= 531:
        return "rain"
    elif 600 <= wid <= 622:
        return "snow"
    elif wid == 800:
        return "clear"
    else:
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
    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("无法获取城市天气")
        st.stop()

    weather_type = get_weather_type(data)

    theme = {
        "clear":  {"color": "#FFD700", "bg": "clear.jpg",  "music": "clear.mp3"},
        "clouds":{"color": "#B0C4DE", "bg": "clouds.jpg","music": "clouds.mp3"},
        "rain":  {"color": "#4A90E2", "bg": "rain.jpg",  "music": "rain.mp3"},
        "snow":  {"color": "#E6F7FF", "bg": "snow.jpg",  "music": "snow.mp3"},
    }

    current = theme[weather_type]

    set_background(current["bg"])

    # 呼吸灯（不动你的设计）
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

    # 信息显示（只做“看得清”处理）
    desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]

    st.markdown(
        f"""
        <div style="
            text-align:center;
            color:white;
            background: rgba(0,0,0,0.35);
            padding:10px;
            border-radius:12px;
            width:220px;
            margin:0 auto;
        ">
            <b>{data['name']}</b><br>
            {desc}<br>
            {temp:.1f} ℃
        </div>
        """,
        unsafe_allow_html=True
    )

    play_music(current["music"])
