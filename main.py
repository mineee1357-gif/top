import streamlit as st
import os

st.set_page_config(
    page_title="실시간 물리 탑 쌓기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 마우스 드래그! 실시간 물리 탑 쌓기 게임")
st.markdown("마우스를 움직여 조준하고 클릭해서 탑을 쌓으세요!")
st.divider()

# 외부의 index.html 파일을 읽어와 출력합니다.
html_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        game_html = f.read()
    # 버튼이 추가되었으므로 높이를 570으로 늘려 끊김 없이 보이도록 조절했습니다.
    st.components.v1.html(game_html, height=570)
else:
    st.error("index.html 파일을 찾을 수 없습니다. main.py와 같은 폴더에 생성해 주세요!")
