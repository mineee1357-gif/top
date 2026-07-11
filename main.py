import streamlit as st

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

# 에러를 유발하는 삼중 따옴표 대신 일반 문자열 더하기 방식을 씁니다.
# 자바스크립트 내의 &&, <, > 기호를 모두 제거하여 분석기 버그를 차단했습니다.
h = '<div style="text-align:center;">'
h += '<h3>점수: <span id="s">0</span> | 상태: <span id="st">준비</span></h3>'
h += '<canvas id="c" width="480" height="400" style="background:#f1f5f9; border:3px solid #cbd5e1; border-radius:12px; cursor:pointer;"></canvas>'
h += '</div>'
h += '<script>'
h += 'const cvs=document.getElementById("c"), ctx=cvs.getContext("2d");'
h += 'const sDsp=document.getElementById("s"), tDsp=document.getElementById("st");'
h += 'let score=0, over=false, drop=false;'
h += 'let b={x:240, y:40, w:60, h:25, vy:0, col:"#FF4B4B"};'
h += 'let stack=[]; const ground={y:360};'
h += 'cvs.addEventListener("mousemove", (e)=>{'
h += '  if(over) return; if(drop) return;'
h += '  const rect=cvs.getBoundingClientRect();'
h += '  b.x = e.clientX - rect.left;'
h += '});'
h += 'cvs.addEventListener("click", ()=>{'
h += '  if(over) return; if(drop) return;'
h += '  drop=true; tDsp.innerText="낙하!";'
h += '});'
h += 'function loop(){'
h += '  if(over){'
h += '    tDsp.innerText="게임오버";'
h += '    ctx.fillStyle="rgba(220,38,38,0.1)"; ctx.fillRect(0,0,480,400);'
h += '    ctx.fillStyle="#dc2626"; ctx.font="bold 30px sans-serif";'
h += '    ctx.fillText("GAME OVER", 150, 200);'
h += '    return;'
h += '  }'
h += '  if(drop){'
h += '    b.vy+=0.4; b.y+=b.vy;'
h += '    let targetY=ground.y, hit=false, miss=false;'
h += '    if(stack.length===0){'
h += '      if(b.y+b.h >= ground.y) hit=true;'
h += '    }else{'
h += '      const top=stack[stack.length-1];'
h += '      let leftCheck = false; let rightCheck = false;'
h += '      if(b.x+b.w/2 >= top.x-top.w/2) leftCheck = true;'
h += '      if(b.x-b.w/2 <= top.x+top.w/2) rightCheck = true;'
h += '      if(leftCheck){'
h += '        if(rightCheck){'
h += '          if(b.y+b.h >= top.y){ targetY=top.y; hit=true; }'
h += '        }'
h += '      }'
h += '      if(!hit){'
h += '        if(b.y+b.h >= ground.y){ hit=true; miss=true; }'
h += '      }'
h += '    }'
h += '    if(hit){'
h += '      drop=false; b.vy=0;'
h += '      if(miss){ over=true; }'
h += '      else{'
h += '        b.y=targetY-b.h; stack.push(Object.assign({},b)); score++;'
h += '        tDsp.innerText="준비";'
h += '        b={x:240, y:40, w:50, h:20, vy:0, col:"#3B82F6"};'
h += '      }'
h += '      sDsp.innerText=score;'
h += '    }'
h += '  }'
h += '  ctx.clearRect(0,0,480,400);'
h += '  ctx.fillStyle="#475569"; ctx.fillRect(0, ground.y, 480, 40);'
h += '  stack.forEach(s=>{'
h += '    ctx.fillStyle=s.col; ctx.fillRect(s.x-s.w/2, s.y, s.w, s.h);'
h += '    ctx.strokeStyle="#1e293b"; ctx.strokeRect(s.x-s.w/2, s.y, s.w, s.h);'
h += '  });'
h += '  ctx.fillStyle=b.col; ctx.fillRect(b.x-b.w/2, b.y, b.w, b
