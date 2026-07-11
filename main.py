import streamlit as st

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

# 자바스크립트 소스코드가 깨지는 것을 막기 위해 안전한 토막 문자열 더하기 방식을 사용합니다.
g = '<div style="text-align: center;"><div style="margin-bottom: 10px; font-family: sans-serif; font-size: 18px; font-weight: bold; color: #1e293b;">현재 점수: <span id="score-display">0</span> 층 | 상태: <span id="status-display" style="color: #2563eb;">블록 조절 중</span></div>'
g += '<div style="margin-bottom: 15px; font-family: sans-serif; font-size: 14px; color: #64748b;"><b>🎮 조작법:</b> 게임판 위에서 마우스를 좌우로 움직여 조준하고, <b>[마우스 왼쪽 클릭]</b> 시 블록이 투하됩니다!</div>'
g += '<canvas id="gameCanvas" width="500" height="500" style="background: #f1f5f9; border: 3px solid #cbd5e1; border-radius: 12px; cursor: pointer;"></canvas></div>'
g += '<script>'
g += 'const canvas = document.getElementById("gameCanvas"); const ctx = canvas.getContext("2d"); const scoreDisplay = document.getElementById("score-display"); const statusDisplay = document.getElementById("status-display");'
g += 'let score = 0; let gameOver = false; let isFalling = false; let currentBlock = { x: 250, y: 50, w: 60, h: 25, vx: 0, vy: 0, color: "#FF4B4B" }; let stackedBlocks = []; const ground = { x: 0, y: 450, w: 500, h: 50 };'
g += 'function getRandomColor() { const c = ["#FF4B4B", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899"]; return c[Math.floor(Math.random() * c.length)]; }'
g += 'canvas.addEventListener("mousemove", (e) => { if (gameOver || isFalling) return; const r = canvas.getBoundingClientRect(); const m = e.clientX - r.left; if (m > currentBlock.w / 2 && m < canvas.width - currentBlock.w / 2) { currentBlock.x = m; } });'
g += 'canvas.addEventListener("click", () => { if (gameOver || isFalling) return; isFalling = true; statusDisplay.innerText = "낙하 중... 💥"; statusDisplay.style.color = "#ea580c"; });'
g += 'function update() { if (gameOver)
