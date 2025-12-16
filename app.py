import streamlit as st
import requests
import base64

# ======================
# 基本设置
# ======================
st.set_page_config(page_title="🌦 Weather Breathing Lamp", layout="centered")

API_KEY = "f79b327c6e33c90c48948f41a5b62e38"

# ======================
# 工具函数
# ======================
def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    res = requests.get(url)
    return res.json()

def get_weather_type(data):
    weather_list = data.get("weather", [])
    weather_mains = [w["main"] for w in weather_list]

    # ⚠️ 关键修复点：遍历判断
    if "Snow" in weather_mains:
        return "snow"
    elif "Rain" in weather_mains or "Drizzle" in weather_mains or "Thunderstorm" in weather_mains:
        return "rain"
    elif "Clear" in weather_mains:
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
        audio_bytes = audio.read()
    st.audio(audio_bytes, format="audio/mp3", autoplay=True)

# ======================
# UI
# ======================
st.title("🌦 Weather Breathing Lamp")
city = st.text_input("请输入城市名")

if city:
    data = get_weather(city)

    if data.get("cod") != 200:
        st.error("❌ 无法获取城市天气，请检查城市名")
        st.stop()

    weather_type = get_weather_type(data)

    # ======================
    # 天气映射
    # ======================
    theme = {
        "clear": {
            "color": "#FFD700",
            "bg": "clear.jpg",
            "music": "clear.mp3"
        },
        "clouds": {
            "color": "#B0C4DE",
            "bg": "clouds.jpg",
            "music": "clouds.mp3"
        },
        "rain": {
            "color": "#4A90E2",
            "bg": "rain.jpg",
            "music": "rain.mp3"
        },
        "snow": {
            "color": "#E6F7FF",
            "bg": "snow.jpg",
            "music": "snow.mp3"
        }
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
            margin: 60px auto;
            border-radius:50%;
            background: radial-gradient(circle, {lamp_color} 0%, rgba(0,0,0,0) 70%);
            box-shadow: 0 0 80px {lamp_color};
            animation: breathe 3s ease-in-out infinite;
        "></div>

        <style>
        @keyframes breathe {{
            0% {{
                transform: scale(1);
                box-shadow: 0 0 40px {lamp_color};
            }}
            50% {{
                transform: scale(1.12);
                box-shadow: 0 0 120px {lamp_color};
            }}
            100% {{
                transform: scale(1);
                box-shadow: 0 0 40px {lamp_color};
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # 音乐
    play_music(current["music"])

    # 调试信息（你之后可以删）
    st.caption(f"🌍 当前天气类型：{weather_type}")
