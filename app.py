import streamlit as st

st.title("🌐 Weather Emotion Lamp")

st.text_input("请输入城市名", "Seoul")

st.markdown(
    """
    <div style="width:200px; height:200px; border-radius:50%; background-color:#FFD93D; margin:auto;"></div>
    """,
    unsafe_allow_html=True
)

st.image("https://images.unsplash.com/photo-1502082553048-f009c37129b9", use_column_width=True)

st.button("查询天气（暂时不动作）")
