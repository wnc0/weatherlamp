import streamlit as st
import requests

st.set_page_config(page_title="Weather Lamp", layout="centered")

st.title("🌦 Weather Emotion Lamp")

city = st.text_input("请输入城市名", "Seoul")

API_KEY = "f79b327c6e33c90c48948f41a5b62e38"  # ← 换成你自己的
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

weather = None

response = requests.get(url)
data = response.json()

# st.write("调试信息：", data)  # ← 这一行很重要

if response.status_code == 200:
    weather = data["weather"][0]["main"].lower()
else:
    st.error(f"获取天气失败：{data.get('message')}")


# 根据真实天气设置颜色
if weather == "clear":
    lamp_color = "#FFD93D"   # 晴
elif weather == "clouds":
    lamp_color = "#6CA0DC"   # 阴
elif weather == "rain":
    lamp_color = "#4A6FA5"   # 雨
elif weather == "snow":
    lamp_color = "#E6F0FF"   # 雪
else:
    lamp_color = "#999999"

# 呼吸灯（中心实色 → 边缘透明 + 立体感）
st.markdown(
    f"""
    <div style="
        width:320px;
        height:320px;
        margin: 40px auto;
        border-radius:50%;
        background: radial-gradient(circle, {lamp_color} 0%, rgba(0,0,0,0) 70%);
        box-shadow: 0 0 60px {lamp_color};
        animation: breathe 3s ease-in-out infinite;
    "></div>

    <style>
    @keyframes breathe {{
        0% {{
            transform: scale(1);
            box-shadow: 0 0 30px {lamp_color};
        }}
        50% {{
            transform: scale(1.1);
            box-shadow: 0 0 80px {lamp_color};
        }}
        100% {{
            transform: scale(1);
            box-shadow: 0 0 30px {lamp_color};
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)



