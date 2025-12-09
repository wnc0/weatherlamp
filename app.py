import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# 页面设置
st.set_page_config(page_title="Weather Emotion Lamp", layout="centered")

st.title("🌐 Weather Emotion Lamp")

# 输入城市
city = st.text_input("请输入城市名", "Seoul")

# 模拟天气数据（真实可改成API）
city_lower = city.lower()
if city_lower in ["seoul", "beijing", "tokyo"]:
    weather = "sunny"
    lamp_color = "#FFD93D"
    bg_url = "https://images.unsplash.com/photo-1502082553048-f009c37129b9"  # 晴天背景
    music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
elif city_lower in ["london", "seattle"]:
    weather = "cloudy"
    lamp_color = "#6CA0DC"
    bg_url = "https://images.unsplash.com/photo-1501594907352-04cda38ebc29"  # 阴天背景
    music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
else:
    weather = "other"
    lamp_color = "#A9A9A9"
    bg_url = "https://images.unsplash.com/photo-1506744038136-46273834b3fb"  # 其他背景
    music_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"

# 背景图片
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{bg_url}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 呼吸灯效果
st.markdown(
    f"""
    <div style="
        width:300px;
        height:300px;
        margin:auto;
        border-radius:50%;
        background: radial-gradient(circle, {lamp_color} 0%, rgba(0,0,0,0) 70%);
        box-shadow: 0 0 40px {lamp_color};
        animation: breathe 2s infinite alternate;
    "></div>

    <style>
    @keyframes breathe {{
        0% {{ transform: scale(1); box-shadow: 0 0 20px {lamp_color}; }}
        50% {{ transform: scale(1.1); box-shadow: 0 0 50px {lamp_color}; }}
        100% {{ transform: scale(1); box-shadow: 0 0 20px {lamp_color}; }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 音乐播放
st.audio(music_url, format="audio/mp3")
