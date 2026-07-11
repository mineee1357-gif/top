import streamlit as st
import numpy as np

st.set_page_config(
    page_title="물리 법칙 탑 쌓기 게임",
    page_icon="🧱",
    layout="centered"
)

# 세션 상태 초기화 (게임 진행 데이터 저장)
if "blocks" not in st.session_state:
    st.session_state.blocks = []  # 쌓인 블록 목록: {'type': 'rect'/'circle', 'x': float, 'w': float, 'h': float, 'color': str}
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

st.title("🧱 물리 법칙 탑 쌓기 게임 (Tower Stacker)")
st.markdown("""
스트림릿에서 물리 엔진(간이 계산)과 SVG 그래픽을 활용하여 구현한 **탑 쌓기 게임**입니다!  
중심을 잘 맞추어 무너지지 않게 최대한 높이 탑을 쌓아보세요.  

---
### 🎮 게임 규칙
1. **블록 종류와 크기**를 선택합니다.
2. **X축 위치(좌우 위치)**를 조절하여 떨어뜨릴 위치를 정합니다.
3. **블록 떨어뜨리기** 버튼을 누르면 탑 위에 블록이 안착합니다.
4. **⚠️ 주의:** 새로 놓은 블록의 중심이 기존 탑의 범위를 벗어나 무게중심이 무너지면 **게임 오버**가 됩니다!
""")

# 게임 리셋 버튼
if st.button("🔄 게임 새로 시작하기", type="primary"):
    st.session_state.blocks = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.rerun()

st.divider()

# 게임판 및 컨트롤러 레이아웃
if not st.session_state.game_over:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🛠️ 블록 조작")
        block_type = st.radio("도형 모양 선택", ["사각형 (직사각형)", "원형 (공)"])
        
        if block_type == "사각형 (직사각형)":
            width = st.slider("블록 너비", 20, 80, 50, step=5)
            height = st.slider("블록 높이", 15, 40, 20, step=5)
            shape_param = (width, height)
        else:
            radius = st.slider("원 반지름", 10, 30, 20, step=2)
            shape_param = (radius * 2, radius * 2) # SVG 변환용
            
        # 낙하 위치 선택 (0~400 px 범위의 가상 스크린)
        drop_x = st.slider("낙하 위치 (X축)", 50, 350, 200, step=5)
        
        # 블록 색상 고르기
        color = st.color_picker("블록 색상 선택", "#FF4B4B")
        
        # 떨어뜨리기 버튼 클릭 이벤트
        if st.button("👇 블록 떨어뜨리기 !", use_container_width=True):
            current_y = 350 # 바닥 높이 기준선 (아래로 갈수록 커지는 SVG 축 기준)
            w, h = shape_param
            
            if len(st.session_state.blocks) == 0:
                # 첫 번째 블록은 무조건 바닥(GROUND) 위에 안착
                target_y = current_y - h
                st.session_state.blocks.append({
                    'type': 'rect' if block_type == "사각형 (직사각형)" else 'circle',
                    'x': drop_x,
                    'y': target_y,
                    'w': w,
                    'h': h,
                    'color': color
                })
                st.session_state.score += 1
                st.rerun()
            else:
                last_block = st.session_state.blocks[-1]
                
                # 간이 물리 충돌 체크 (직전 블록의 좌우 boundary 연산)
                last_left = last_block['x'] - last_block['w']/2
                last_right = last_block['x'] + last_block['w']/2
                
                current_left = drop_x - w/2
                current_right = drop_x + w/2
                
                # 두 블록 면적이 공중에서 비껴나가지 않고 조금이라도 겹치는지 체크
                if current_right > last_left and current_left < last_right:
                    # 무게중심(Center of mass) 검증: 새로 떨어진 블록의 중심(drop_x)이 
                    # 아래 블록의 지지대 표면을 벗어나면 중력에 의해 기울어 떨어짐(게임오버)
                    if drop_x < last_left or drop_x > last_right:
                        st.session_state.game_over = True
                        st.rerun()
                    else:
                        # 안정적 안착 성공: 이전 블록의 Y층 위로 적재
                        target_y = last_block['y'] - h
                        st.session_state.blocks.append({
                            'type': 'rect' if block_type == "사각형 (직사각형)" else 'circle',
                            'x': drop_x,
                            'y': target_y,
                            'w': w,
                            'h': h,
                            'color': color
                        })
                        st.session_state.score += 1
                        st.success("🎯 안전하게 안착했습니다!")
                        st.rerun()
                else:
                    # 완전히 허공에 드롭됨 -> 추락 및 즉시 게임오버
                    st.session_state.game_over = True
                    st.rerun()

    with col2:
        st.subheader("🎯 실시간 타워 상태")
        st.metric(label="현재 쌓은 탑 높이", value=f"{st.session_state.score} 층")
        
        # HTML SVG 도면 생성
        svg_content = """
        <svg width="400" height="400" style="background-color: #f1f5f9; border-radius: 10px; border: 2px solid #cbd5e1;">
            <rect x="0" y="350" width="400" height="50" fill="#64748b" />
            <text x="165" y="380" fill="white" font-weight="bold" font-family="sans-serif">GROUND</text>
        """
        
        # 데이터에 기록된 도형들 실시간 드로잉
        for b in st.session_state.blocks:
            if b['type'] == 'rect':
                svg_content += f'<rect x="{b["x"] - b["w"]/2}" y="{b["y"]}" width="{b["w"]}" height="{b["h"]}" fill="{b["color"]}" stroke="#1e293b" stroke-width="2" rx="3" />'
            else:
                radius = b['w'] / 2
                svg_content += f'<circle cx="{b["x"]}" cy="{b["y"] + radius}" r="{radius}" fill="{b["color"]}" stroke="#1e293b" stroke-width="2" />'
                
        # 가이드 가상 조준선 렌더링
        if 'w' in locals():
            svg_content += f'<line x1="{drop_x}" y1="0" x2="{drop_x}" y2="350" stroke="#94a3b8" stroke-dasharray="4" />'
            if block_type == "사각형 (직사각형)":
                svg_content += f'<rect x="{drop_x - w/2}" y="10" width="{w}" height="{h}" fill="{color}" opacity="0.5" />'
            else:
                svg_content += f'<circle cx="{drop_x}" cy="{10 + (w/2)}" r="{w/2}" fill="{color}" opacity="0.5" />'
                
        svg_content += "</svg>"
        
        # 스트림릿 내부에 실시간 컴포넌트로 주입
        st.components.v1.html(svg_content, height=410)

else:
    st.error(f"💥 균형이 깨져 무너졌습니다! 최종 점수: {st.session_state.score} 층")
    
    # 실패 연출용 붉은색 스크린 전환
    svg_content = """
    <svg width="400" height="400" style="background-color: #fee2e2; border-radius: 10px; border: 2px solid #ef4444;">
        <rect x="0" y="350" width="400" height="50" fill="#475569" />
        <text x="110" y="200" fill="#b91c1c" font-size="28" font-weight="bold" font-family="sans-serif">💥 TOWER COLLAPSED</text>
    </svg>
    """
    st.components.v1.html(svg_content, height=410)
    st.balloons() # 게임 종료 축하 폭죽 효과
