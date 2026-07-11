import streamlit as st
import os

st.set_page_config(
    page_title="실시간 물리 탑 쌓기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 마우스 드래그! 실시간 물리 탑 쌓기 게임")
st.markdown("마우스를 움직여 조준하고 클릭해서 탑을 쌓으세요!")

if st.button("🔄 게임 새로 시작하기", type="primary"):
    st.rerun()

st.divider()

# 외부의 index.html 파일을 안전하게 읽어와서 화면에 출력합니다.
# 이 구조는 코드 내부의 기호 충돌이나 잘림 현상(SyntaxError)을 물리적으로 차단합니다.
html_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        game_html = f.read()
    st.components.v1.html(game_html, height=530)
else:
    st.error("index.html 파일을 찾을 수 없습니다. main.py와 같은 폴더에 생성해 주세요!")
