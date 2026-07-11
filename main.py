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

# 에디터가 강제 줄바꿈을 하더라도 문법 오류가 나지 않도록 글자를 완전히 쪼개어 결합합니다.
g = '<div style="text-align: center;">'
g += '<div style="margin-bottom: 10px; '
g += 'font-family: sans-serif; font-size: 18px; '
g += 'font-weight: bold; color: #1e293b;">'
g += '현재 점수: <span id="score-display">0</span> 층 '
g += '| 상태: <span id="status-display" '
g += 'style="color: #2563eb;">블록 조절 중</span>'
g += '</div>'
g += '<div style="margin-bottom: 15px; '
g += 'font-family: sans-serif; font-size: 14px; '
g += 'color: #64748b;">'
g += '<b>🎮 조작법:</b> 게임판 위에서 '
g += '마우스를 좌우로 움직여 조준하고, '
g += '<b>[마우스 왼쪽 클릭]</b> 시 블록이 투하됩니다!'
g += '</div>'
g += '<canvas id="gameCanvas" width="500" height="500" '
g += 'style="background: #f1f5f9; border: 3px solid #cbd5e1; '
g += 'border-radius: 12px; cursor: pointer;"></canvas>'
g += '</div>'
g += '<script>'
g += 'const canvas = document.getElementById("gameCanvas");'
g += 'const ctx = canvas.getContext("2d");'
g += 'const scoreDisplay = document.getElementById("score-display");'
g += 'const statusDisplay = document.getElementById("status-display");'
g += 'let score = 0; let gameOver = false; let isFalling = false;'
g += 'let currentBlock = { x: 250, y: 50, w: 60, h: 25, '
g += 'vx: 0, vy: 0, color: "#FF4B4B" };'
g += 'let stackedBlocks = [];'
g += 'const ground = { x: 0, y: 450, w: 500, h: 50 };'
g += 'function getRandomColor() {'
g += 'const c = ["#FF4B4B", "#3B82F6", "#10B981", '
g += '"#F59E0B", "#8B5CF6", "#EC4899"];'
g += 'return c[Math.floor(Math.random() * c.length)];'
g += '}'
g += 'canvas.addEventListener("mousemove", (e) => {'
g += 'if (gameOver || isFalling) return;'
g += 'const r = canvas.getBoundingClientRect();'
g += 'const m = e.clientX - r.left;'
g += 'if (m > currentBlock.w / 2 && '
g += 'm < canvas.width -
