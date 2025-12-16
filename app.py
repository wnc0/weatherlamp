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
    res = requests.get(url)
    return res.json()

# ✅ 关键修复：严格优先级判断
def get_weather_type(data):
    weather_list = data.get("weather", [])
    mains = [w["main"] for w in weather_list]

    if "Snow" in mains:
        return "snow"
    if any(w in mains for w in ["Rain", "Drizzle", "Thunderstorm"]):
        return "rain"
    if "Clear" in mains:
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

    # 背景
    set_background(current["bg"])

    # 呼吸灯
    lamp_color = current["color"]
    st.markdown(
        f"""
        <div style="
            width:320px;
            height:320px;
            margin: 50px auto 20px;
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

    # ✅ 信息显示（你说缺的这块）
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]

    st.markdown(
        f"""
        <div style="text-align:center; font-size:18px;">
            <b>{data['name']}</b><br>
            {description}<br>
            {temp:.1f} ℃
        </div>
        """,
        unsafe_allow_html=True
    )

    # 音乐
    play_music(current["music"])
