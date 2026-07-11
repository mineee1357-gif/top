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

# 긴 자바스크립트 코드를 직접 넣지 않고, iframe 내부에 독립된 HTML 환경을 구현합니다.
# 이 구조는 코드 잘림이나 부등호(<, >), 따옴표 충돌로부터 100% 안전합니다.
game_widget = """
<div style="text-align:center; font-family:sans-serif;">
  <h3>현재 점수: <span id="s">0</span> 층 | 상태: <span id="st" style="color:#2563eb">준비</span></h3>
  <p style="color:#64748b; font-size:14px;"><b>🎮 조작법:</b> 마우스를 좌우로 움직여 조준하고 <b>[클릭]</b>하면 낙하합니다!</p>
  <canvas id="c" width="480" height="450" style="background:#f1f5f9; border:3px solid #cbd5e1; border-radius:12px; cursor:pointer;"></canvas>
</div>

<script>
const cvs=document.getElementById("c"), ctx=cvs.getContext("2d");
const sDsp=document.getElementById("s"), tDsp=document.getElementById("st");
let score=0, over=false, drop=false;
let b={x:240, y:40, w:60, h:25, vx:0, vy:0, col:"#FF4B4B"};
let stack=[]; const ground={x:0, y:400, w:480, h:50};

cvs.addEventListener("mousemove", (e)=>{
  if(over||drop) return;
  const rect=cvs.getBoundingClientRect();
  b.x = e.clientX - rect.left;
});
cvs.addEventListener("click", ()=>{
  if(over||drop) return;
  drop=true; tDsp.innerText="낙하 중!"; tDsp.style.color="#ea580c";
});

function loop(){
  if(!over){
    if(drop){
      b.vy+=0.4; b.y+=b.vy;
      let targetY=ground.y, hit=false, miss=false;
      if(stack.length===0){
        if(b.y+b.h>=ground.y) hit=true;
      }else{
        const top=stack[stack.length-1];
        if(b.x+b.w/2>top.x-top.w/2 && b.x-b.w/2<top.x+top.w/2){
          if(b.y+b.h>=top.y){ targetY=top.y; hit=true; }
        }else if(b.y+b.h>=ground.y){ hit=true; miss=true; }
      }
      if(hit){
        drop=false; b.vy=0;
        if(miss){ over=true; }
        else{
          b.y=targetY-b.h; stack.push({...b}); score++;
          tDsp.innerText="준비"; tDsp.style.color="#2563eb";
          b={x:240, y:40, w:Math.floor(
