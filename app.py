import streamlit as st
import requests
import os
import base64

st.set_page_config(page_title="Weather Lamp", layout="centered")

API_KEY = "f79b327c6e33c90c48948f41a5b62e38"

def map_weather(weather_list):
    mains = [w["main"].lower() for w in weather_list]
    if "snow" in mains:
        return "snow"
    if "rain" in mains or "drizzle" in mains:
        return "rain"
    if "clouds" in mains or "mist" in mains or "fog":
        return "clouds"
    return "clear"


WEATHER_CONFIG = {
    "clear": {
        "color": "#FFD966",
        "image": "images/clear.jpg",
        "music": "music/clear.mp3"
    },
    "clouds": {
        "color": "#A9B7C6",
        "image": "images/clouds.jpg",
        "music": "music/clouds.mp3"
    },
    "rain": {
        "color": "#5DADE2",
        "image": "images/rain.jpg",
        "music": "music/rain.mp3"
    },
    "snow": {
        "color": "#E8F8F5",
        "image": "images/snow.jpg",
        "music": "music/snow.mp3"
    }
}

st.title("🌦 Weather Breathing Lamp")
city = st.text_input("请输入城市名")

def set_background(image_path):
    if not os.path.exists(image_path):
        st.warning(f"⚠️ 找不到背景图片：{image_path}")
        return

    with open(image_path, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

if city:
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    res = requests.get(url).json()

    if res.get("cod") != 200:
        st.error("获取天气失败")
        st.json(res)
    else:
        weather_type = map_weather(res["weather"])
        config = WEATHER_CONFIG[weather_type]

        set_background(config["image"])

        lamp_color = config["color"]

        st.markdown(
            f"""
            <div style="
                width:320px;
                height:320px;
                margin: 60px auto;
                border-radius:50%;
                background: radial-gradient(circle, {lamp_color} 0%, rgba(0,0,0,0) 70%);
                box-shadow: 0 0 70px {lamp_color};
                animation: breathe 3s ease-in-out infinite;
            "></div>

            <style>
            @keyframes breathe {{
                0% {{
                    transform: scale(1);
                    box-shadow: 0 0 35px {lamp_color};
                }}
                50% {{
                    transform: scale(1.12);
                    box-shadow: 0 0 100px {lamp_color};
                }}
                100% {{
                    transform: scale(1);
                    box-shadow: 0 0 35px {lamp_color};
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        if os.path.exists(config["music"]):
            st.audio(config["music"], autoplay=True, loop=True)

        st.markdown(
            f"""
            <div style="text-align:center; font-size:18px; color:white;">
                <p><b>{res["name"]}</b></p>
                <p>{res["weather"][0]["description"]}</p>
                <p>{res["main"]["temp"]} °C</p>
            </div>
            """,
            unsafe_allow_html=True
        )
