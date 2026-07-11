import streamlit as st
import base64

st.set_page_config(
    page_title="실시간 물리 탑 쌓기 게임",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 마우스 드래그! 실시간 물리 탑 쌓기 게임")
st.markdown("""
이제 블록을 **마우스 움직임**으로 직접 제어할 수 있습니다! 
블록을 조준하고 클릭하면 중력을 받아 실시간으로 떨어지며, 중심을 잃고 비껴나가면 완전히 바닥으로 추락한 뒤 게임 오버를 시각적으로 연출합니다.
""")

if st.button("🔄 게임 새로 시작하기", type="primary"):
    st.rerun()

st.divider()

# 자바스크립트 게임 소스코드를 Base64 텍스트로 안전하게 변환한 값입니다.
# 특수문자, 따옴표, 줄바꿈이 전혀 없어서 100% 문법 에러를 방지합니다.
b64_game = (
    "PGRpdiBzdHlsZT0idGV4dC1hbGlnbjogY2VudGVyOyI+PGRpdiBzdHlsZT0ibWFyZ2luLWJvdHRv"
    "bTogMTBweDsgZm9udC1mYW1pbHk6IHNhbnMtc2VyaWY7IGZvbnQtc2l6ZTogMThweDsgZm9udC13"
    "ZWlnaHQ6IGJvbGQ7IGNvbG9yOiAjMWUyOTNiOyI+currentIHBvaW50OiA8c3BhbiBpZD0ic2Nv"
    "cmUtZGlzcGxheSI+MDwvc3Bhbj4gfCBzdGF0dXM6IDxzcGFuIGlkPSJzdGF0dXMtZGlzcGxheSIg"
    "c3R5bGU9ImNvbG9yOiAjMjU2M2ViOyI+YmxvY2sgY29udHJvbDwvc3Bhbj48L2Rpdj48ZGl2IHN0"
    "eWxlPSJtYXJnaW4tYm90dG9tOiAxNXB4OyBmb250LWZhbWlseTogc2Fucy1zZXJpZjsgZm9udC1z"
    "aXplOiAxNHB4OyBjb2xvcjogIzY0NzQ4YjsiPjxiPq0GIGNvbnRyb2w6PC9iPiBtb3ZlIG1vdXNl"
    "LCBjbGljayB0byBkcm9wITwvZGl2PjxjYW52YXMgaWQ9ImdhbWVDYW52YXMiIHdpZHRoPSI1MDAi"
    "IGhlaWdodD0iNTAwIiBzdHlsZT0iYmFja2dyb3VuZDogI2YxZjVmOTsgYm9yZGVyOiAzcHggc29s"
    "aWQ6ICNjYmQ1ZTE7IGJvcmRlci1yYWRpdXM6IDEycHg7IGN1cnNvcjogcG9pbnRlcjsiPjwvY2Fu"
    "dmFzPjwvZGl2PjxzY3JpcHQ+Y29uc3QgY2FudmFzPWRvY3VtZW50LmdldEVsZW1lbnRCeUlkKCJn"
    "YW1lQ2FudmFzIiksY3R4PWNhbnZhcy5nZXRDb250ZXh0KCIyZCIpLHNjb3JlRGlzcGxheT1kb2N1"
    "bWVudC5nZXRFbGVtZW50QnlJZCgic2NvcmUtZGlzcGxheSIpLHN0YXR1c0Rpc3BsYXk9ZG9jdW1l"
    "bnQuZ2V0RWxlbWV5dEJ5SWQoInN0YXR1cy1kaXNwbGF5Iik7bGV0IHNjb3JlPTAsZ2FtZU92ZXI9"
    "ITEsaXNGYWxsaW5nPSExLGN1cnJlbnRCbG9jayB9IHg6MjUwLHk6NTAsdzYwLGg6MjUsdng6MCx2"
    "eTowLGNvbG9yOiIjRkY0QjRCIn0sc3RhY2tlZEJsb2Nrcz1bXTtjb25zdCBncm91bmQ9eyB4OjAs"
    "eTo0NTAsdzo1MDAsaDo1MCB9O2Z1bmN0aW9uIGdldFJhbmRvbUNvbG9yKCl7Y29uc3QgZT1bIiNG"
    "RjRCNEIiLCIjM0I4MkY2IiwiIzEwQjk4MSIsIiNGNTlFMEIiLCIjOEI1Q0Y2IiwiI0VDNDg5OSJd"
    "O3JldHVybiBlW01hdGguZmxvb3IoTWF0aC5yYW5kb20oKSplLmxlbmd0aCldfWNhbnZhcy5hZGRF"
    "dmVudExpc3RlbmVyKCJtb3VzZW1vdmUiLChlPT57aWYoZ2FtZU92ZXJ8fGlzRmFsbGluZylyZXR1"
    "cm47Y29uc3QgdD1jYW52YXMuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCksbj1lLmNsaWVudFgtdC5s"
    "ZWZ0O24+Y3VycmVudEJsb2NrLncvMiYmbjxjYW52YXMud2lkdGgtY3VycmVudEJsb2NrLncvMiYm"
    "KGN1cnJlbnRCbG9jay54PW4pfSksY2FudmFzLmFkZEV2ZW50TGlzdGVuZXIoImNsaWNrIiwoKCk9"
    "PntpZihnYW1lT3Zlcnx8aXNGYWxsaW5nKXJldHVybjtpY0ZhbGxpbmdfMSEsc3RhdHVzRGlzcGxh"
    "eS5pbm5lclRleHQ9ImRyb3BwaW5nLi4uIOKckyIsc3RhdHVzRGlzcGxheS5zdHlsZS5jb2xvcj0i"
    "I2VhNTgwYyJ9KSxmdW5jdGlvbiB1cGRhdGUoKXtpZighZ2FtZU92ZXImJmlzRmFsbGluZyl7Y3Vy"
    "cmVudEJsb2NrLnZ5Kz0uNCxjdXJyZW50QmxvY2sueSsrY3VycmVudEJsb2NrLnZ5O2xldCBlPWdy"
    "b3VuZC55LHQ9ITEsbj1udWxsO2lmKDA9PT1zdGFja2VkQmxvY2tzLmxlbmd0aCljdXJyZW50Qmxv"
    "Y2sueStjdXJyZW50QmxvY2suaD49Z3JvdW5kLnkmJihlPWdyb3VuZC55LHQ9ITApO2Vsc2V7Y29u"
    "c3Qgby1zdGFja2VkQmxvY2tzW3N0YWNrZWRCbG9ja3MubGVuZ3RoLTFdO2N1cnJlbnRCbG9jay54"
    "K2N1cnJlbnRCbG9jay53LzI+by54LW8udy8yJiZjdXJyZW50QmxvY2cueS1jdXJyZW50QmxvY2su"
    "dy8yPG8ueCtvLncvMj9jdXJyZW50QmxvY2cueStjdXJyZW50QmxvY2suaD49by55JiYoZT1vLnk9"
    "dD0hMCxuPW8pOmN1cnJlbnRCbG9jay55K2N1cnJlbnRCbG9jay5oPj1ncm91bmQueSYmKGU9Z3Jv"
    "dW5kLnksdD0hMCxuPSJtaXNzIil9aWYodCl7aXNGYWxsaW5nPSExLGN1cnJlbnRCbG9jay52eT0w"
    "LDA9PT1zdGFja2VkQmxvY2tzLmxlbmd0aD8oY3VycmVudEJsb2NrLnk9ZS1jdXJyZW50QmxvY2su"
    "aCxzdGFja2VkQmxvY2tzLnB1c2goey4uLmN1cnJlbnRCbG9ja30pLHNjb3JlKyssbmV4dFR1cm4o"
    "KSk6Im1pc3MiPT09bj8oZ2FtZU92ZXI9ITAsaGFuZGxlR2FtZU92ZXIoKSk6TWF0aC5hYnMoY3Vy"
    "cmVudEJsb2NrLngubi54KT5uLncvMj8oZ2FtZU92ZXI9ITAsY3VycmVudEJsb2NrLnZ4PWN1cnJl"
    "bnRCbG9jay54Pm4ueD80Oi00LGFuaW1hdGVGYWxsT3V0KCkpOihjdXJyZW50QmxvY2cueT1lLWN1"
    "cnJlbnRCbG9jay5oLHN0YWNrZWRCbG9ja3MucHVzaChey4uLmN1cnJlbnRCbG9ja30pLHNjb3Jl"
    "KyssbmV4dFR1cm
