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

# ✅ 关键新增：展示模式（兜底）
mode = st.selectbox(
    "展示模式（用于演示）",
    ["自动（真实天气）", "晴天", "阴天", "雨天", "雪天"]
)

if city:
    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("无法获取城市天气")
        st.stop()

    # ======================
    # 天气决定逻辑
    # ======================
    if mode != "自动（真实天气）":
        weather_type = {
            "晴天": "clear",
            "阴天": "clouds",
            "雨天": "rain",
            "雪天": "snow"
        }[mode]
    else:
        # 真实天气（保守）
        if "snow" in data:
            weather_type = "snow"
        elif "rain" in data:
            weather_type = "rain"
        elif data["weather"][0]["id"] == 800:
            weather_type = "clear"
        else:
            weather_type = "clouds"

    theme = {
        "clear":  {"color": "#FFD700", "bg": "clear.jpg",  "music": "clear.mp3"},
        "clouds":{"color": "#B0C4DE", "bg": "clouds.jpg","music": "clouds.mp3"},
        "rain":  {"color": "#4A90E2", "bg": "rain.jpg",  "music": "rain.mp3"},
        "snow":  {"color": "#E6F7FF", "bg": "snow.jpg",  "music": "snow.mp3"},
    }

    current = theme[weather_type]

    # 背景
    set_background(current["bg"])

    # 呼吸灯
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

    # 城市信息
    st.markdown(
        f"""
        <div style="
            text-align:center;
            color:white;
            background: rgba(0,0,0,0.35);
            padding:10px;
            border-radius:12px;
            width:240px;
            margin:0 auto;
        ">
            <b>{data['name']}</b><br>
            {data['weather'][0]['description']}<br>
            {data['main']['temp']:.1f} ℃
        </div>
        """,
        unsafe_allow_html=True
    )

    play_music(current["music"])
