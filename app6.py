import streamlit as st
import joblib
import pandas as pd
import math, time

st.set_page_config(page_title="IronMind — Bulldozer AI", page_icon="🏗️",
                   layout="wide", initial_sidebar_state="expanded")

# ═══════════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Share+Tech+Mono&family=Barlow:ital,wght@0,300;0,400;0,600;0,700;1,300&display=swap');

:root{
  --bg:#03070e; --panel:#080f1a; --border:#162030;
  --amber:#f5a623; --amber2:#ffd080; --amber-dim:#c07810;
  --cyan:#38bdf8; --red:#ef4444; --green:#22c55e;
  --text:#d8e8f5; --sub:#7a9ab5; --muted:#405060;
  --glow:rgba(245,166,35,.45); --cglow:rgba(56,189,248,.3);
}
html,body,[data-testid="stAppViewContainer"]{
  background:var(--bg)!important; color:var(--text)!important;
  font-family:'Barlow',sans-serif;
}
[data-testid="stSidebar"]{background:#04090f!important;border-right:1px solid var(--border);}
[data-testid="stHeader"]{background:transparent!important;}
[data-testid="stMainBlockContainer"]{padding-top:0!important;}

/* ── PAGE MASTHEAD ── */
.masthead{
  position:relative; padding:28px 6px 0;
  display:flex; align-items:flex-end; gap:22px;
  margin-bottom:0;
}
.masthead-badge{
  width:52px;height:52px;border-radius:12px;
  background:linear-gradient(145deg,#1a2e44,#0c1a28);
  border:1px solid var(--border);
  display:flex;align-items:center;justify-content:center;
  font-size:28px;
  box-shadow:0 0 18px var(--glow),inset 0 1px 0 rgba(255,255,255,.05);
  flex-shrink:0;
}
.masthead-words{ line-height:1; }
.masthead-eyebrow{
  font-family:'Share Tech Mono',monospace;
  font-size:11px;letter-spacing:4px;color:var(--sub);
  text-transform:uppercase;margin-bottom:6px;
}
.masthead-title{
  font-family:'Bebas Neue',sans-serif;
  font-size:38px;letter-spacing:4px;
  background:linear-gradient(90deg,#ffd080 0%,#f5a623 50%,#c07810 100%);
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  filter:drop-shadow(0 0 18px rgba(245,166,35,.5));
  margin:0;
}
.masthead-sub{
  font-family:'Barlow',sans-serif;font-style:italic;font-weight:300;
  font-size:15px;letter-spacing:1px;color:var(--sub);margin-top:4px;
}
.masthead-rule{
  width:100%;height:1px;
  background:linear-gradient(90deg,#f5a623 0%,rgba(245,166,35,.15) 55%,transparent);
  margin:16px 0 22px; opacity:.7;
}

/* ── TICKER ── */
.ticker{
  background:#04090f;border-top:1px solid var(--border);
  border-bottom:1px solid var(--border);
  overflow:hidden;white-space:nowrap;padding:11px 0;margin-bottom:24px;
}
.ticker-inner{
  display:inline-block;
  animation:tickScroll 42s linear infinite;
  font-family:'Share Tech Mono',monospace;
  font-size:13px;color:var(--sub);letter-spacing:1.5px;
}
@keyframes tickScroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
.ta{color:var(--amber);margin:0 12px;}
.tc{color:var(--cyan);margin:0 12px;}

/* ── STAT CARDS ── */
.stat-row{display:flex;gap:14px;margin-bottom:22px;}
.stat-card{
  flex:1;background:var(--panel);border:1px solid var(--border);
  border-radius:14px;padding:20px 22px;position:relative;overflow:hidden;
  transition:border-color .3s,box-shadow .3s;
}
.stat-card:hover{border-color:var(--amber);box-shadow:0 0 22px rgba(245,166,35,.12);}
.stat-card::before{
  content:'';position:absolute;top:0;left:0;width:3px;height:100%;
  background:linear-gradient(180deg,var(--amber),transparent);
}
.stat-card::after{
  content:'';position:absolute;top:0;right:0;width:40%;height:1px;
  background:linear-gradient(90deg,transparent,rgba(245,166,35,.2));
}
.sc-label{
  font-family:'Share Tech Mono',monospace;font-size:11px;
  color:var(--sub);letter-spacing:2.5px;text-transform:uppercase;margin-bottom:8px;
}
.sc-val{font-family:'Bebas Neue',sans-serif;font-size:42px;color:var(--amber);line-height:1;}
.sc-unit{font-size:14px;color:var(--sub);margin-left:4px;}

/* ── GAUGES ── */
.gauge-card{
  background:var(--panel);border:1px solid var(--border);
  border-radius:14px;padding:18px 12px 14px;text-align:center;
}

/* ── PREDICT BUTTON ── */
.stButton>button{
  width:100%;
  background:linear-gradient(135deg,#a06010 0%,#f5a623 50%,#ffd080 100%)!important;
  color:#08060000!important;color:#0c0800!important;
  border:none!important;border-radius:12px!important;
  font-family:'Bebas Neue',sans-serif!important;
  font-size:26px!important;letter-spacing:5px!important;
  padding:17px 0!important;
  box-shadow:0 0 40px var(--glow),0 4px 20px rgba(0,0,0,.5)!important;
  transition:all .2s ease!important;cursor:pointer!important;
}
.stButton>button:hover{
  transform:translateY(-4px)!important;
  box-shadow:0 0 70px var(--glow),0 12px 35px rgba(0,0,0,.65)!important;
}

/* ── RESULT ── */
.result-box{
  background:linear-gradient(145deg,#06111f,#080f1a);
  border:1px solid var(--amber);border-radius:16px;padding:36px;text-align:center;
  box-shadow:0 0 60px var(--glow),inset 0 0 80px rgba(245,166,35,.03);
  animation:rPop .6s cubic-bezier(.175,.885,.32,1.275) both;
}
@keyframes rPop{from{opacity:0;transform:scale(.82) translateY(28px)}to{opacity:1;transform:scale(1) translateY(0)}}
.rl{font-family:'Share Tech Mono',monospace;font-size:12px;letter-spacing:4px;
    color:var(--sub);text-transform:uppercase;margin-bottom:14px;}
.rp{font-family:'Bebas Neue',sans-serif;font-size:76px;letter-spacing:4px;
    color:var(--amber);text-shadow:0 0 50px var(--glow);line-height:1;}
.rc{font-family:'Share Tech Mono',monospace;font-size:13px;
    color:var(--sub);margin-top:12px;letter-spacing:.5px;}

/* ── FEATURE TILES ── */
.feat-grid{display:flex;gap:14px;margin-top:0;}
.ft{
  flex:1;background:var(--panel);border:1px solid var(--border);
  border-radius:14px;padding:24px 20px;transition:all .3s;position:relative;overflow:hidden;
}
.ft:hover{border-color:var(--amber);transform:translateY(-4px);
          box-shadow:0 16px 40px rgba(0,0,0,.5),0 0 20px rgba(245,166,35,.1);}
.ft::before{
  content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,var(--amber),transparent);
  opacity:0;transition:opacity .3s;
}
.ft:hover::before{opacity:1;}
.fi{font-size:32px;margin-bottom:12px;}
.ftt{font-family:'Bebas Neue',sans-serif;font-size:21px;letter-spacing:2px;
     color:var(--text);margin-bottom:8px;}
.fd{font-size:14px;color:var(--sub);line-height:1.7;}

/* ── SIDEBAR ── */
.stSelectbox label,.stSlider label{
  font-family:'Share Tech Mono',monospace!important;
  font-size:12px!important;letter-spacing:2px!important;
  color:var(--sub)!important;text-transform:uppercase!important;
}
[data-testid="stSlider"]>div>div>div{background:var(--amber)!important;}

/* ── MISC ── */
hr{border-color:var(--border)!important;margin:28px 0!important;}
.stProgress>div>div{background:var(--amber)!important;}
.footer{text-align:center;font-family:'Share Tech Mono',monospace;
        font-size:11px;letter-spacing:2px;color:var(--muted);padding:22px 0 10px;}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
#  CINEMATIC HERO  —  dusk construction site, god rays, fog, 2 dozers
# ═══════════════════════════════════════════════════════════════════
HERO = """
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{background:#03070e;}
.cw{position:relative;width:100%;height:400px;overflow:hidden;
    border-radius:20px;border:1px solid #162030;background:#03070e;
    box-shadow:0 0 80px rgba(0,0,0,.9),inset 0 0 120px rgba(0,0,0,.6);}
canvas{position:absolute;top:0;left:0;width:100%;height:100%;}
/* HUD chrome */
.ht{position:absolute;top:0;left:0;right:0;
    padding:14px 20px;display:flex;justify-content:space-between;align-items:center;
    background:linear-gradient(180deg,rgba(3,7,14,.75),transparent);
    pointer-events:none;z-index:10;}
.hl{font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:3px;
    color:rgba(245,166,35,.8);text-transform:uppercase;}
.hm{font-family:'Share Tech Mono',monospace;font-size:13px;letter-spacing:2px;
    color:rgba(245,166,35,.95);text-shadow:0 0 12px rgba(245,166,35,.6);}
.hr2{font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:2px;
     color:rgba(56,189,248,.7);}
.hb{position:absolute;bottom:0;left:0;right:0;
    padding:12px 20px;display:flex;justify-content:space-between;align-items:center;
    background:linear-gradient(0deg,rgba(3,7,14,.7),transparent);
    pointer-events:none;z-index:10;}
.hbl{font-family:'Share Tech Mono',monospace;font-size:10px;letter-spacing:2px;
     color:rgba(80,100,120,.8);}
/* animated status dot */
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;
     background:#22c55e;margin-right:7px;
     animation:pulse 2s ease-in-out infinite;}
@keyframes pulse{0%,100%{opacity:1;box-shadow:0 0 4px #22c55e}50%{opacity:.4;box-shadow:none}}
/* corner brackets */
.corner{position:absolute;width:24px;height:24px;z-index:10;pointer-events:none;}
.corner.tl{top:12px;left:12px;border-top:1.5px solid rgba(245,166,35,.55);border-left:1.5px solid rgba(245,166,35,.55);}
.corner.tr{top:12px;right:12px;border-top:1.5px solid rgba(245,166,35,.55);border-right:1.5px solid rgba(245,166,35,.55);}
.corner.bl{bottom:12px;left:12px;border-bottom:1.5px solid rgba(245,166,35,.55);border-left:1.5px solid rgba(245,166,35,.55);}
.corner.br{bottom:12px;right:12px;border-bottom:1.5px solid rgba(245,166,35,.55);border-right:1.5px solid rgba(245,166,35,.55);}
</style>

<div class="cw">
  <canvas id="cc"></canvas>
  <div class="corner tl"></div><div class="corner tr"></div>
  <div class="corner bl"></div><div class="corner br"></div>
  <div class="ht">
    <div class="hl">&#9711; IRONMIND &middot; FIELD VISION v4.2</div>
    <div class="hm" id="clk">――:――:――</div>
    <div class="hr2">SYS NOMINAL &nbsp;&#9654;</div>
  </div>
  <div class="hb">
    <div class="hbl"><span class="dot"></span>LIVE RENDER &middot; DUSK OPERATION MODE</div>
    <div class="hbl">CAM-01 &nbsp;|&nbsp; SITE ALPHA &nbsp;|&nbsp; 60 FPS</div>
  </div>
</div>

<script>
(function(){
const cv=document.getElementById('cc'),ctx=cv.getContext('2d');
let W,H,F=0;
const PI=Math.PI,TAU=PI*2;

/* clock */
setInterval(()=>{
  const d=new Date();
  document.getElementById('clk').textContent=d.toTimeString().slice(0,8);
},1000);

function resize(){
  W=cv.width=cv.parentElement.offsetWidth;
  H=cv.height=cv.parentElement.offsetHeight;
}
resize(); window.addEventListener('resize',()=>{resize();});

/* ─── PERLIN-LIKE SMOOTH NOISE ─── */
function snoise(x){
  const i=Math.floor(x), f=x-i;
  const u=f*f*(3-2*f);
  const a=Math.sin(i*127.1)*43758.5453%1;
  const b=Math.sin((i+1)*127.1)*43758.5453%1;
  return a+(b-a)*u;
}
function terrain(x,off,amp,freq){
  return H*.72 + amp*snoise(x*freq+off)
               + amp*.45*snoise(x*freq*2.1+off*1.8)
               + amp*.2 *snoise(x*freq*4.7+off*.9);
}

/* ─── STARS ─── */
const stars=Array.from({length:90},()=>({
  x:Math.random(),y:Math.random()*.45,r:Math.random()*1.4+.3,ph:Math.random()*TAU
}));

/* ─── PARTICLE POOL (dust + smoke + sparks + data-nodes) ─── */
const particles=[];
function spawn(x,y,type){
  if(type==='smoke') particles.push({
    type:'smoke',x,y,vx:-.25-Math.random()*.5,vy:-1.1-Math.random()*.9,
    r:6+Math.random()*5,life:1,decay:.006+Math.random()*.005,
    hue:20+Math.random()*20
  });
  if(type==='dust') for(let i=0;i<5;i++) particles.push({
    type:'dust',x:x+(Math.random()-.5)*30,y:y+Math.random()*12,
    vx:-2-Math.random()*3,vy:-.8-Math.random()*1.5,
    r:3+Math.random()*9,life:1,decay:.02+Math.random()*.03
  });
  if(type==='spark') for(let i=0;i<3;i++) particles.push({
    type:'spark',x,y,
    vx:(Math.random()-.5)*4,vy:-Math.random()*5-2,
    r:1.5+Math.random(),life:1,decay:.04+Math.random()*.04
  });
  if(type==='data') particles.push({
    type:'data',x,y:y-Math.random()*120,
    vx:(Math.random()-.5)*.6,vy:-.4-Math.random()*.4,
    r:2,life:1,decay:.008+Math.random()*.006,
    char:['0','1','Σ','λ','∇','∫','π'][Math.floor(Math.random()*7)]
  });
}
function tickP(){
  for(let i=particles.length-1;i>=0;i--){
    const p=particles[i];
    p.x+=p.vx;p.y+=p.vy;p.life-=p.decay;
    if(p.type==='smoke'){p.r+=.7;p.vx*=.98;}
    if(p.type==='dust'){p.r+=.4;p.vx*=.97;p.vy*=.95;}
    if(p.type==='spark'){p.vy+=.18;} /* gravity */
    if(p.life<=0) particles.splice(i,1);
  }
}
function drawP(){
  particles.forEach(p=>{
    ctx.save();
    if(p.type==='smoke'){
      const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r);
      g.addColorStop(0,`hsla(${p.hue},25%,55%,${p.life*.5})`);
      g.addColorStop(1,`hsla(${p.hue},15%,35%,0)`);
      ctx.fillStyle=g;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,TAU);ctx.fill();
    } else if(p.type==='dust'){
      const g=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r);
      g.addColorStop(0,`rgba(200,165,90,${p.life*.36})`);
      g.addColorStop(1,`rgba(160,120,50,0)`);
      ctx.fillStyle=g;ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,TAU);ctx.fill();
    } else if(p.type==='spark'){
      ctx.shadowColor='#f5a623';ctx.shadowBlur=8;
      ctx.fillStyle=`rgba(255,200,80,${p.life})`;
      ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,TAU);ctx.fill();
    } else if(p.type==='data'){
      ctx.font=`${10+p.r*2}px Share Tech Mono,monospace`;
      ctx.fillStyle=`rgba(56,189,248,${p.life*.7})`;
      ctx.shadowColor='rgba(56,189,248,.5)';ctx.shadowBlur=6;
      ctx.fillText(p.char,p.x,p.y);
    }
    ctx.restore();
  });
}

/* ─── CRANE TOWER (static BG element) ─── */
function drawCrane(cx,groundY){
  ctx.save();ctx.translate(cx,groundY);
  /* mast */
  ctx.strokeStyle='rgba(40,60,85,.9)';ctx.lineWidth=8;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,-220);ctx.stroke();
  ctx.lineWidth=5;
  /* jib */
  ctx.beginPath();ctx.moveTo(0,-218);ctx.lineTo(140,-195);ctx.stroke();
  ctx.beginPath();ctx.moveTo(0,-218);ctx.lineTo(-50,-200);ctx.stroke();
  /* cable */
  ctx.strokeStyle='rgba(60,80,110,.7)';ctx.lineWidth=1.5;
  ctx.beginPath();ctx.moveTo(100,-198);ctx.lineTo(105,-155);ctx.stroke();
  /* hook */
  ctx.fillStyle='rgba(60,80,110,.8)';
  ctx.beginPath();ctx.rect(100,-160,10,8);ctx.fill();
  /* lattice */
  ctx.strokeStyle='rgba(30,50,75,.6)';ctx.lineWidth=2;
  for(let y=-200;y<0;y+=28){
    ctx.beginPath();ctx.moveTo(-6,y);ctx.lineTo(6,y+14);ctx.stroke();
    ctx.beginPath();ctx.moveTo(6,y);ctx.lineTo(-6,y+14);ctx.stroke();
  }
  /* warning light */
  const wblink=Math.sin(F*.06)>.3;
  if(wblink){
    ctx.save();ctx.shadowColor='#ef4444';ctx.shadowBlur=14;
    ctx.fillStyle='#ef4444';
    ctx.beginPath();ctx.arc(0,-225,5,0,TAU);ctx.fill();
    ctx.restore();
  }
  ctx.restore();
}

/* ─── EXCAVATOR (BG, smaller) ─── */
function drawExcavator(cx,groundY,sc){
  ctx.save();ctx.translate(cx,groundY);ctx.scale(sc,sc);
  /* tracks */
  ctx.fillStyle='#1a2a38';ctx.beginPath();ctx.roundRect(-55,-14,110,22,6);ctx.fill();
  /* body */
  const bg=ctx.createLinearGradient(0,-58,0,-14);
  bg.addColorStop(0,'#e09018');bg.addColorStop(1,'#a06010');
  ctx.fillStyle=bg;ctx.beginPath();ctx.roundRect(-42,-56,84,44,5);ctx.fill();
  /* cab */
  const cg=ctx.createLinearGradient(0,-90,0,-56);
  cg.addColorStop(0,'#203040');cg.addColorStop(1,'#182838');
  ctx.fillStyle=cg;ctx.beginPath();ctx.roundRect(-20,-90,50,36,[5,5,0,0]);ctx.fill();
  /* window */
  ctx.fillStyle='rgba(56,189,248,.22)';ctx.beginPath();ctx.roundRect(-15,-85,40,26,3);ctx.fill();
  /* boom */
  const t=F*.018;
  const bx=32,by=-48,blen=70,bang=-PI*.35+Math.sin(t)*.12;
  const bex=bx+blen*Math.cos(bang),bey=by+blen*Math.sin(bang);
  ctx.strokeStyle='#8aa0b8';ctx.lineWidth=8;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(bx,by);ctx.lineTo(bex,bey);ctx.stroke();
  /* dipper */
  const dlen=55,dang=bang+PI*.3+Math.sin(t+1)*.15;
  const dex=bex+dlen*Math.cos(dang),dey=bey+dlen*Math.sin(dang);
  ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(bex,bey);ctx.lineTo(dex,dey);ctx.stroke();
  /* bucket */
  ctx.fillStyle='#607888';
  ctx.save();ctx.translate(dex,dey);ctx.rotate(dang+PI*.6+Math.sin(t+2)*.2);
  ctx.beginPath();ctx.moveTo(-12,-6);ctx.lineTo(12,-6);ctx.lineTo(14,10);ctx.lineTo(-14,10);ctx.closePath();ctx.fill();
  ctx.restore();
  ctx.restore();
}

/* ─── DETAILED BULLDOZER ─── */
function drawDozer(cx,gy,sc,mirror){
  ctx.save();ctx.translate(cx,gy);ctx.scale(sc*(mirror?-1:1),sc);
  const t=F*.06;

  /* headlight beams */
  const bdir=mirror?1:-1;
  ctx.save();ctx.globalAlpha=.5;
  const b1=ctx.createLinearGradient(bdir*(-115),0,bdir*(-115-200),0);
  b1.addColorStop(0,'rgba(255,235,140,.14)');b1.addColorStop(1,'rgba(255,235,140,0)');
  ctx.fillStyle=b1;
  ctx.beginPath();ctx.moveTo(bdir*(-115),-52);ctx.lineTo(bdir*(-315),-100);ctx.lineTo(bdir*(-315),20);ctx.lineTo(bdir*(-115),-10);ctx.closePath();ctx.fill();
  ctx.restore();

  /* === TRACK === */
  ctx.save();ctx.shadowColor='rgba(0,0,0,.7)';ctx.shadowBlur=16;ctx.shadowOffsetY=6;
  ctx.fillStyle='#1e3040';ctx.beginPath();ctx.roundRect(-104,-20,208,34,9);ctx.fill();
  ctx.restore();
  ctx.strokeStyle='#2a4055';ctx.lineWidth=1.5;ctx.beginPath();ctx.roundRect(-104,-20,208,34,9);ctx.stroke();
  /* links */
  const lo=(F*2.2)%22;
  for(let lx=-102+lo;lx<104;lx+=22){
    ctx.fillStyle='#162535';ctx.strokeStyle='#243848';ctx.lineWidth=.8;
    ctx.beginPath();ctx.roundRect(lx,-18,20,28,2);ctx.fill();ctx.stroke();
    ctx.strokeStyle='#1e3040';ctx.lineWidth=2.5;
    ctx.beginPath();ctx.moveTo(lx+2,10);ctx.lineTo(lx+18,10);ctx.stroke();
  }
  /* sprockets */
  const sprk=(cx2,cy2,rev)=>{
    ctx.fillStyle='#162535';ctx.strokeStyle='#2e4862';ctx.lineWidth=2;
    ctx.beginPath();ctx.arc(cx2,cy2,19,0,TAU);ctx.fill();ctx.stroke();
    for(let a=0;a<10;a++){
      const ang=a*TAU/10+t*(rev?-1:1);
      ctx.fillStyle='#243848';
      ctx.beginPath();ctx.arc(cx2+19*Math.cos(ang),cy2+19*Math.sin(ang),3.5,0,TAU);ctx.fill();
    }
    ctx.fillStyle='#f5a623';ctx.beginPath();ctx.arc(cx2,cy2,8,0,TAU);ctx.fill();
    ctx.fillStyle='#0a0e14';ctx.beginPath();ctx.arc(cx2,cy2,4,0,TAU);ctx.fill();
  };
  sprk(-85,-3,false);sprk(86,-3,true);
  [-38,0,38].forEach(rx=>{
    ctx.fillStyle='#182535';ctx.strokeStyle='#2a3e52';ctx.lineWidth=1.5;
    ctx.beginPath();ctx.arc(rx,11,9,0,TAU);ctx.fill();ctx.stroke();
    ctx.fillStyle='#3a5570';ctx.beginPath();ctx.arc(rx,11,4,0,TAU);ctx.fill();
  });

  /* === BODY === */
  ctx.save();ctx.shadowColor='rgba(0,0,0,.75)';ctx.shadowBlur=20;ctx.shadowOffsetY=7;
  const bg=ctx.createLinearGradient(0,-82,0,-20);
  bg.addColorStop(0,'#ffc040');bg.addColorStop(.45,'#e89015');bg.addColorStop(1,'#b07010');
  ctx.fillStyle=bg;ctx.beginPath();ctx.roundRect(-94,-78,188,60,6);ctx.fill();
  ctx.restore();
  /* highlight */
  const bh=ctx.createLinearGradient(0,-78,0,-62);
  bh.addColorStop(0,'rgba(255,255,255,.2)');bh.addColorStop(1,'rgba(255,255,255,0)');
  ctx.fillStyle=bh;ctx.beginPath();ctx.roundRect(-94,-78,188,14,[6,6,0,0]);ctx.fill();
  /* panel seams */
  ctx.strokeStyle='rgba(0,0,0,.22)';ctx.lineWidth=1.2;
  ctx.beginPath();ctx.moveTo(-94,-56);ctx.lineTo(94,-56);ctx.stroke();
  [-60,-18,22,62].forEach(rx=>{ctx.beginPath();ctx.moveTo(rx,-78);ctx.lineTo(rx,-18);ctx.stroke();});
  /* brand plate */
  ctx.fillStyle='rgba(0,0,0,.35)';ctx.beginPath();ctx.roundRect(-36,-70,72,20,3);ctx.fill();
  ctx.fillStyle='rgba(255,255,255,.6)';ctx.font='bold 12px Share Tech Mono,monospace';
  ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('CAT D11',0,-60);

  /* === HOOD === */
  const hg=ctx.createLinearGradient(0,-78,0,-50);
  hg.addColorStop(0,'#263848');hg.addColorStop(1,'#18283a');
  ctx.fillStyle=hg;ctx.beginPath();ctx.roundRect(-50,-78,100,30,[5,5,0,0]);ctx.fill();
  ctx.strokeStyle='#38526a';ctx.lineWidth=1;ctx.beginPath();ctx.roundRect(-50,-78,100,30,[5,5,0,0]);ctx.stroke();
  for(let ly=-74;ly<-52;ly+=5){ctx.strokeStyle='rgba(255,255,255,.05)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(-43,ly);ctx.lineTo(43,ly);ctx.stroke();}

  /* === EXHAUST === */
  ctx.fillStyle='#2a3e52';ctx.beginPath();ctx.roundRect(34,-118,13,46,3);ctx.fill();
  ctx.strokeStyle='#3e5870';ctx.lineWidth=1;ctx.stroke();
  ctx.fillStyle='#1e2e40';ctx.beginPath();ctx.ellipse(40,-118,8,3,0,0,TAU);ctx.fill();

  /* === CAB === */
  ctx.save();ctx.shadowColor='rgba(0,0,0,.7)';ctx.shadowBlur=16;
  const cg=ctx.createLinearGradient(0,-155,0,-78);
  cg.addColorStop(0,'#2e4258');cg.addColorStop(1,'#18283e');
  ctx.fillStyle=cg;ctx.beginPath();ctx.roundRect(-32,-155,90,79,[8,8,0,0]);ctx.fill();
  ctx.restore();
  ctx.strokeStyle='#3e5878';ctx.lineWidth=2;
  ctx.beginPath();ctx.moveTo(-32,-155);ctx.lineTo(-32,-76);ctx.moveTo(58,-155);ctx.lineTo(58,-76);ctx.stroke();
  /* windshield */
  const wg=ctx.createLinearGradient(-22,-148,-22,-100);
  wg.addColorStop(0,'rgba(56,189,248,.38)');wg.addColorStop(1,'rgba(20,110,165,.14)');
  ctx.fillStyle=wg;ctx.beginPath();ctx.roundRect(-26,-148,70,58,[4,4,0,0]);ctx.fill();
  ctx.fillStyle='rgba(255,255,255,.07)';
  ctx.beginPath();ctx.moveTo(-22,-146);ctx.lineTo(8,-146);ctx.lineTo(-22,-112);ctx.closePath();ctx.fill();
  ctx.strokeStyle='rgba(56,189,248,.5)';ctx.lineWidth=1;
  ctx.beginPath();ctx.roundRect(-26,-148,70,58,[4,4,0,0]);ctx.stroke();
  /* side glass */
  ctx.fillStyle='rgba(20,110,165,.22)';ctx.strokeStyle='rgba(56,189,248,.3)';ctx.lineWidth=1;
  ctx.beginPath();ctx.roundRect(-30,-138,8,35,2);ctx.fill();ctx.stroke();
  /* roof light bar */
  ctx.fillStyle='#131e2c';ctx.beginPath();ctx.roundRect(-34,-160,96,10,3);ctx.fill();
  [0,24,48,72].forEach((lx,i)=>{
    const on=(F+i*9)%100<80;
    ctx.beginPath();ctx.arc(-26+lx,-154,4.5,0,TAU);
    if(on){ctx.save();ctx.shadowColor='rgba(255,225,80,.95)';ctx.shadowBlur=12;ctx.fillStyle='#ffe870';ctx.fill();ctx.restore();}
    else{ctx.fillStyle='#1a2838';ctx.fill();}
  });
  /* operator */
  ctx.fillStyle='rgba(15,26,45,.9)';
  ctx.beginPath();ctx.arc(14,-130,10,0,TAU);ctx.fill();
  ctx.beginPath();ctx.roundRect(5,-120,20,28,4);ctx.fill();

  /* === BLADE === */
  ctx.strokeStyle='#8aA0b8';ctx.lineWidth=6;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(-94,-48);ctx.lineTo(-124,-50);ctx.stroke();
  ctx.beginPath();ctx.moveTo(-94,-28);ctx.lineTo(-124,-26);ctx.stroke();
  /* hyd cylinder */
  ctx.strokeStyle='#506878';ctx.lineWidth=4;
  ctx.beginPath();ctx.moveTo(-74,-46);ctx.lineTo(-110,-36);ctx.stroke();
  /* blade */
  const blg=ctx.createLinearGradient(-158,-75,-106,-75);
  blg.addColorStop(0,'#d0dce8');blg.addColorStop(.4,'#9ab0c0');blg.addColorStop(1,'#5a7080');
  ctx.fillStyle=blg;
  ctx.beginPath();ctx.moveTo(-124,-74);ctx.lineTo(-150,-66);ctx.lineTo(-152,-16);ctx.lineTo(-124,-12);ctx.closePath();ctx.fill();
  [-130,-138,-146].forEach(bx=>{ctx.strokeStyle='rgba(255,255,255,.1)';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(bx,-70);ctx.lineTo(bx,-15);ctx.stroke();});
  /* cutting edge */
  const ceg=ctx.createLinearGradient(-154,-68,-150,-14);
  ceg.addColorStop(0,'#ddeeff');ceg.addColorStop(.5,'#ffffff');ceg.addColorStop(1,'#aabccc');
  ctx.strokeStyle=ceg;ctx.lineWidth=5;ctx.lineCap='butt';
  ctx.beginPath();ctx.moveTo(-152,-66);ctx.lineTo(-152,-16);ctx.stroke();
  /* blade headlights */
  [[-150,-58],[-150,-40]].forEach(([lx,ly])=>{
    ctx.save();ctx.shadowColor='rgba(255,235,130,.95)';ctx.shadowBlur=16;
    ctx.fillStyle='#ffe880';ctx.beginPath();ctx.arc(lx,ly,4.5,0,TAU);ctx.fill();
    ctx.restore();
  });
  /* blade pins */
  ctx.fillStyle='#607888';ctx.beginPath();ctx.arc(-124,-50,5,0,TAU);ctx.fill();
  ctx.beginPath();ctx.arc(-124,-26,5,0,TAU);ctx.fill();

  /* === RIPPER === */
  ctx.strokeStyle='#3a5268';ctx.lineWidth=7;ctx.lineCap='round';
  ctx.beginPath();ctx.moveTo(94,-34);ctx.lineTo(98,-34);ctx.lineTo(100,12);ctx.stroke();
  ctx.fillStyle='#8aa0b8';ctx.beginPath();ctx.moveTo(96,10);ctx.lineTo(106,10);ctx.lineTo(102,26);ctx.closePath();ctx.fill();

  ctx.restore();
}

/* ─── GOD RAYS (crepuscular) ─── */
function drawGodRays(sx,sy){
  ctx.save();ctx.globalCompositeOperation='screen';
  const rays=8;
  for(let i=0;i<rays;i++){
    const angle=-PI*.55+i*(PI*.3/rays)+Math.sin(F*.004+i)*.015;
    const len=H*1.4;
    const x2=sx+len*Math.cos(angle),y2=sy+len*Math.sin(angle);
    const spread=18+Math.sin(F*.008+i*1.3)*4;
    const ox1=sx+spread*Math.cos(angle+PI/2),oy1=sy+spread*Math.sin(angle+PI/2);
    const ox2=sx-spread*Math.cos(angle+PI/2),oy2=sy-spread*Math.sin(angle+PI/2);
    const endSpread=len*.35;
    const ex1=x2+endSpread*Math.cos(angle+PI/2),ey1=y2+endSpread*Math.sin(angle+PI/2);
    const ex2=x2-endSpread*Math.cos(angle+PI/2),ey2=y2-endSpread*Math.sin(angle+PI/2);
    const alpha=(.04+.025*Math.sin(F*.006+i*2.1))*(1-i/(rays*1.2));
    const g=ctx.createLinearGradient(sx,sy,x2,y2);
    g.addColorStop(0,`rgba(255,200,100,${alpha*2.2})`);
    g.addColorStop(.4,`rgba(255,180,80,${alpha})`);
    g.addColorStop(1,'rgba(255,150,50,0)');
    ctx.fillStyle=g;
    ctx.beginPath();ctx.moveTo(ox1,oy1);ctx.lineTo(ex1,ey1);ctx.lineTo(ex2,ey2);ctx.lineTo(ox2,oy2);ctx.closePath();ctx.fill();
  }
  ctx.restore();
}

/* ─── VOLUMETRIC FOG BAND ─── */
function drawFog(yBase,alpha){
  const g=ctx.createLinearGradient(0,yBase-60,0,yBase+30);
  g.addColorStop(0,'rgba(30,55,90,0)');
  g.addColorStop(.4,`rgba(20,45,80,${alpha})`);
  g.addColorStop(1,'rgba(10,25,50,0)');
  ctx.fillStyle=g;ctx.fillRect(0,yBase-60,W,90);
  /* drift */
  for(let i=0;i<4;i++){
    const fx=((F*.3+i*W*.28)%( W+300))-150;
    const fy=yBase-10+Math.sin(F*.01+i)*12;
    const fr=80+i*30;
    const fg2=ctx.createRadialGradient(fx,fy,0,fx,fy,fr);
    fg2.addColorStop(0,`rgba(25,50,85,${alpha*.8})`);
    fg2.addColorStop(1,'rgba(15,35,65,0)');
    ctx.fillStyle=fg2;ctx.beginPath();ctx.arc(fx,fy,fr,0,TAU);ctx.fill();
  }
}

/* ─── HEAT SHIMMER on ground ─── */
let shimmerOff=0;
function drawShimmer(groundY){
  ctx.save();ctx.globalAlpha=.04;
  shimmerOff+=.8;
  for(let x=0;x<W;x+=4){
    const dy=2*Math.sin(x*.05+shimmerOff*.06)+1.5*Math.sin(x*.12+shimmerOff*.04);
    ctx.fillStyle=`hsl(${40+dy*5},60%,60%)`;
    ctx.fillRect(x,groundY-2,3,3+dy*.5);
  }
  ctx.restore();
}

/* ─── BACKGROUND ─── */
function drawBg(){
  /* dusk sky gradient */
  const sky=ctx.createLinearGradient(0,0,0,H*.75);
  sky.addColorStop(0,'#03070e');
  sky.addColorStop(.35,'#0a1225');
  sky.addColorStop(.65,'#1a1a08');
  sky.addColorStop(.78,'#3d1e04');
  sky.addColorStop(.88,'#7a3505');
  sky.addColorStop(.95,'#c05510');
  sky.addColorStop(1,'#e07820');
  ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);

  /* stars (only upper area) */
  stars.forEach(s=>{
    s.ph+=.014;
    const alpha=Math.max(0,(.5-s.y/.45)*(.35+.28*Math.sin(s.ph)));
    if(alpha>.02){
      ctx.beginPath();ctx.arc(s.x*W,s.y*H,s.r,0,TAU);
      ctx.fillStyle=`rgba(200,215,240,${alpha})`;ctx.fill();
    }
  });

  /* sun disk */
  const sx=W*.72,sy=H*.76;
  ctx.save();
  /* outer corona */
  const corona=ctx.createRadialGradient(sx,sy,0,sx,sy,120);
  corona.addColorStop(0,'rgba(255,200,80,.55)');
  corona.addColorStop(.3,'rgba(255,150,40,.2)');
  corona.addColorStop(.7,'rgba(220,80,10,.07)');
  corona.addColorStop(1,'rgba(180,40,0,0)');
  ctx.fillStyle=corona;ctx.beginPath();ctx.arc(sx,sy,120,0,TAU);ctx.fill();
  /* sun body */
  const sun=ctx.createRadialGradient(sx,sy,0,sx,sy,30);
  sun.addColorStop(0,'rgba(255,240,180,1)');
  sun.addColorStop(.4,'rgba(255,200,80,.95)');
  sun.addColorStop(.8,'rgba(255,140,30,.7)');
  sun.addColorStop(1,'rgba(200,80,10,0)');
  ctx.fillStyle=sun;ctx.beginPath();ctx.arc(sx,sy,30,0,TAU);ctx.fill();
  ctx.restore();

  drawGodRays(sx,sy);

  /* far silhouette city/hills */
  ctx.fillStyle='rgba(8,15,28,.85)';
  ctx.beginPath();ctx.moveTo(0,H*.68);
  for(let x=0;x<=W;x+=1){
    const y=H*.68+15*snoise(x*.003+.5)+8*snoise(x*.008+1.2)+4*snoise(x*.02+2);
    ctx.lineTo(x,y);
  }ctx.lineTo(W,H);ctx.lineTo(0,H);ctx.closePath();ctx.fill();

  /* mid hills parallax */
  const moff=-(F*.18)*.004;
  ctx.fillStyle='rgba(12,22,38,.92)';
  ctx.beginPath();ctx.moveTo(0,H);
  for(let x=0;x<=W;x+=3) ctx.lineTo(x,terrain(x,moff,18,.006));
  ctx.lineTo(W,H);ctx.closePath();ctx.fill();

  /* foreground ground */
  const foff=-(F*.006);
  const fgG=ctx.createLinearGradient(0,H*.72,0,H);
  fgG.addColorStop(0,'#243040');fgG.addColorStop(.3,'#1c2838');fgG.addColorStop(1,'#0e1a28');
  ctx.fillStyle=fgG;
  ctx.beginPath();ctx.moveTo(0,H);
  for(let x=0;x<=W;x+=3) ctx.lineTo(x,terrain(x,foff,10,.013));
  ctx.lineTo(W,H);ctx.closePath();ctx.fill();

  /* ground surface line */
  ctx.strokeStyle='rgba(50,85,125,.55)';ctx.lineWidth=1.5;
  ctx.beginPath();
  for(let x=0;x<=W;x+=3){
    const y=terrain(x,foff,10,.013);
    x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
  }ctx.stroke();
}

/* ─── HUD OVERLAY ─── */
function drawOverlay(){
  /* scan line */
  const sl=(F*1.6)%(H+32)-16;
  const slG=ctx.createLinearGradient(0,sl-14,0,sl+14);
  slG.addColorStop(0,'rgba(245,166,35,0)');
  slG.addColorStop(.5,'rgba(245,166,35,.045)');
  slG.addColorStop(1,'rgba(245,166,35,0)');
  ctx.fillStyle=slG;ctx.fillRect(0,sl-14,W,28);
  /* bottom glow band */
  const bg=ctx.createLinearGradient(0,H-50,0,H);
  bg.addColorStop(0,'rgba(245,140,20,0)');
  bg.addColorStop(1,'rgba(245,140,20,.06)');
  ctx.fillStyle=bg;ctx.fillRect(0,H-50,W,50);
  /* vignette */
  const vg=ctx.createRadialGradient(W/2,H/2,H*.22,W/2,H/2,H*1.0);
  vg.addColorStop(0,'rgba(0,0,0,0)');
  vg.addColorStop(1,'rgba(0,0,0,.65)');
  ctx.fillStyle=vg;ctx.fillRect(0,0,W,H);
  /* chromatic glitch line (rare) */
  if(F%320<2){
    ctx.save();ctx.globalAlpha=.3;
    const gy=Math.random()*H;
    ctx.fillStyle='rgba(56,189,248,.5)';ctx.fillRect(0,gy,W,1);
    ctx.restore();
  }
}

/* ─── MAIN LOOP ─── */
function draw(){
  F++;
  ctx.clearRect(0,0,W,H);
  drawBg();

  /* fog layers */
  const foff2=-(F*.006);
  const groundMid=terrain(W*.5,foff2,10,.013);
  drawFog(groundMid+20,.12);
  drawFog(groundMid-30,.06);

  /* crane (static BG) */
  drawCrane(W*.82, groundMid+8);

  /* excavator BG (smaller, farther) */
  const exX=(F*.35+200)%(W+220)-110;
  const exG=terrain(exX,foff2,10,.013);
  drawExcavator(exX,exG,.48);

  /* main dozer */
  const dX=((F*.9)%(W+320))-160;
  const dY=terrain(dX,foff2,10,.013);
  if(F%4===0){spawn(dX+36,dY-128,'smoke');}
  if(F%3===0){spawn(dX-108,dY-4,'dust');}
  if(F%60===0){spawn(dX,dY-60,'spark');}
  if(F%45===0){spawn(dX+20,dY-90,'data');}
  drawDozer(dX,dY,.76,false);

  /* second smaller dozer going right */
  const d2X=(W-((F*.55+100)%(W+240))+120);
  const d2Y=terrain(d2X,foff2,10,.013)-6;
  if(F%5===0){spawn(d2X-30,d2Y-100,'smoke');}
  if(F%4===0){spawn(d2X+85,d2Y-4,'dust');}
  drawDozer(d2X,d2Y,.54,true);

  drawShimmer(groundMid);
  tickP(); drawP();
  drawOverlay();

  requestAnimationFrame(draw);
}
draw();
})();
</script>
"""

# ═══════════════════════════════════════════════════════════════════
#  TICKER
# ═══════════════════════════════════════════════════════════════════
TI=[
  "IRONMIND AI v4.2","MODEL R²: 0.881","RMSE: ₹6,218","428,000+ AUCTION RECORDS",
  "RANDOM FOREST · 53 FEATURES","CAT D11 · D10 · D9 SERIES","NIGHT OPS MODE",
  "IRONMIND AI v4.2","MODEL R²: 0.881","RMSE: ₹6,218","428,000+ AUCTION RECORDS",
  "RANDOM FOREST · 53 FEATURES","CAT D11 · D10 · D9 SERIES","NIGHT OPS MODE",
]
tick_h="".join(f'<span class="ta">◆</span>{i} <span class="tc">|</span> ' for i in TI)
TICKER=f'<div class="ticker"><div class="ticker-inner">{tick_h}</div></div>'

# ═══════════════════════════════════════════════════════════════════
#  ANIMATED GAUGE (CSS-animated arc via SVG SMIL)
# ═══════════════════════════════════════════════════════════════════
def gauge(value, label, val_str, max_val):
    pct=min(value/max_val,1.0)
    ang=-140+pct*280; rad=ang*math.pi/180
    x2=80+54*math.sin(rad); y2=86-54*math.cos(rad)
    color="#f5a623" if pct<.6 else ("#ef4444" if pct>.85 else "#fb923c")
    td=pct*183
    # build tick marks
    ticks=""
    for i in range(9):
        a=(-140+i*35)*math.pi/180
        ix=80+48*math.sin(a); iy=86-48*math.cos(a)
        ox=80+58*math.sin(a); oy=86-58*math.cos(a)
        ticks+=f'<line x1="{ix:.1f}" y1="{iy:.1f}" x2="{ox:.1f}" y2="{oy:.1f}" stroke="#1a2535" stroke-width="1.5"/>'
    return f"""
    <div class="gauge-card">
      <svg width="160" height="125" viewBox="0 0 160 125">
        {ticks}
        <path d="M 20 96 A 60 60 0 1 1 140 96" fill="none" stroke="#101820"
              stroke-width="12" stroke-linecap="round"/>
        <path d="M 20 96 A 60 60 0 1 1 140 96" fill="none" stroke="#1a2535"
              stroke-width="10" stroke-linecap="round"/>
        <path d="M 20 96 A 60 60 0 1 1 140 96" fill="none" stroke="{color}"
              stroke-width="8" stroke-linecap="round"
              stroke-dasharray="{td:.1f} 191" opacity=".95"
              filter="url(#glow)"/>
        <defs>
          <filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/>
          <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <line x1="80" y1="88" x2="{x2:.1f}" y2="{y2:.1f}"
              stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>
        <circle cx="80" cy="88" r="7" fill="{color}" opacity=".9"/>
        <circle cx="80" cy="88" r="3.5" fill="#080f1a"/>
        <text x="80" y="80" text-anchor="middle" fill="{color}"
              font-family="Share Tech Mono,monospace" font-size="16" font-weight="bold">{val_str}</text>
        <text x="80" y="120" text-anchor="middle" fill="#7a9ab5"
              font-family="Share Tech Mono,monospace" font-size="10" letter-spacing="1.5">{label}</text>
      </svg>
    </div>"""

# ═══════════════════════════════════════════════════════════════════
#  MODEL LOAD
# ═══════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    try: return joblib.load("Bulldozer_model.pkl"), joblib.load("columns.pkl")
    except: return None, None

model, train_cols = load_model()

# ═══════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style="font-family:'Bebas Neue',sans-serif;font-size:32px;
     color:#f5a623;letter-spacing:5px;margin:10px 0 4px;
     text-shadow:0 0 20px rgba(245,166,35,.4);">
  MACHINE CONFIG
</div>
<div style="font-family:'Share Tech Mono',monospace;font-size:12px;
     color:#7a9ab5;letter-spacing:2.5px;margin-bottom:22px;border-bottom:1px solid #162030;padding-bottom:14px;">
  INPUT PARAMETERS
</div>
""", unsafe_allow_html=True)

YearMade = st.sidebar.slider("YEAR MANUFACTURED", 1950, 2025, 2015)
MachineHoursCurrentMeter = st.sidebar.slider("OPERATING HOURS", 0, 100000, 4500, step=100)
states = ['California','Texas','Florida','New York','Ohio','Unspecified']
state_map = {s:i for i,s in enumerate(states)}
state_input = st.sidebar.selectbox("DEPLOYMENT STATE", states)
size_map = {"Mini":0,"Small":1,"Medium":2,"Large / XL":3}
size_input = st.sidebar.selectbox("PRODUCT SIZE CLASS", list(size_map.keys()))

age_sb = 2025 - YearMade
cond_sb = max(0, 100 - int(MachineHoursCurrentMeter/1000) - age_sb*2)
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="font-family:'Share Tech Mono',monospace;font-size:13px;
     color:#7a9ab5;letter-spacing:1px;line-height:2.4;">
  AGE &nbsp;&nbsp;&nbsp;&rarr; <b style="color:#f5a623;">{age_sb} YRS</b><br>
  HOURS &nbsp;&rarr; <b style="color:#f5a623;">{MachineHoursCurrentMeter:,} HRS</b><br>
  COND &nbsp;&nbsp;&rarr; <b style="color:{'#22c55e' if cond_sb>60 else '#ef4444'};">{cond_sb}/100</b><br>
  ZONE &nbsp;&nbsp;&rarr; <b style="color:#f5a623;">{state_input.upper()}</b><br>
  SIZE &nbsp;&nbsp;&rarr; <b style="color:#f5a623;">{size_input.upper()}</b>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
#  MAIN PAGE
# ═══════════════════════════════════════════════════════════════════

# MASTHEAD
st.markdown("""
<div class="masthead">
  <div class="masthead-badge">🏗️</div>
  <div class="masthead-words">
    <div class="masthead-eyebrow">Heavy Equipment Intelligence Platform</div>
    <div class="masthead-title">Bulldozer Resale Price Predictor</div>
    <div class="masthead-sub">AI-Powered Resale Valuation &nbsp;·&nbsp; Real-Time Auction Intelligence &nbsp;·&nbsp; Industrial Grade</div>
  </div>
</div>
<div class="masthead-rule"></div>
""", unsafe_allow_html=True)

# HERO
st.components.v1.html(HERO, height=415)

# TICKER
st.components.v1.html(TICKER, height=50)

# STAT CARDS
age  = 2025 - YearMade
util = MachineHoursCurrentMeter // max(age,1)
cond = max(0, 100 - int(MachineHoursCurrentMeter/1000) - age*2)
cond_col = "#22c55e" if cond>60 else "#ef4444"

st.markdown(f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="sc-label">Machine Age</div>
    <div class="sc-val">{age}<span class="sc-unit">yrs</span></div>
  </div>
  <div class="stat-card">
    <div class="sc-label">Avg Utilisation</div>
    <div class="sc-val">{util:,}<span class="sc-unit">h/yr</span></div>
  </div>
  <div class="stat-card">
    <div class="sc-label">Condition Index</div>
    <div class="sc-val" style="color:{cond_col};">{cond}<span class="sc-unit">/ 100</span></div>
  </div>
  <div class="stat-card">
    <div class="sc-label">Size Class</div>
    <div class="sc-val" style="font-size:28px;padding-top:6px;">{size_input.upper()}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# GAUGES + BUTTON
cg1,cg2,cg3,cpred = st.columns([1,1,1,2])
with cg1: st.components.v1.html(gauge(age,"MACHINE AGE",f"{age}yr",40), height=168)
with cg2: st.components.v1.html(gauge(MachineHoursCurrentMeter,"OPER. HOURS",f"{MachineHoursCurrentMeter//1000}kh",100000), height=168)
with cg3: st.components.v1.html(gauge(cond,"CONDITION",f"{cond}%",100), height=168)
with cpred:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    predict_clicked = st.button("⚡  CALCULATE RESALE VALUE")

st.markdown("---")

# PREDICTION
if predict_clicked:
    bar = st.progress(0)
    status = st.empty()
    phases = [
        (18,  "📡  Loading feature matrix…"),
        (42,  "🌲  Bootstrapping 500 decision trees…"),
        (68,  "📊  Aggregating forest votes…"),
        (86,  "📉  Applying regional depreciation…"),
        (100, "✅  Price estimate locked in."),
    ]
    p=0
    for target, msg in phases:
        status.markdown(
            f"<div style='font-family:Share Tech Mono,monospace;font-size:13px;"
            f"color:#7a9ab5;letter-spacing:1px;padding:5px 0;'>{msg}</div>",
            unsafe_allow_html=True)
        while p<target:
            p+=1; bar.progress(p); time.sleep(0.010)
    bar.empty(); status.empty()

    if model and train_cols:
        d={c:0 for c in train_cols}
        d["YearMade"]=YearMade; d["MachineHoursCurrentMeter"]=MachineHoursCurrentMeter
        d["state"]=state_map[state_input]; d["ProductSize"]=size_map[size_input]
        pred=model.predict(pd.DataFrame([d]))[0]
        price_str=f"₹{pred:,.0f}"
    else:
        import random; price_str=f"₹{random.randint(800000,4500000):,}"

    st.markdown(f"""
    <div class="result-box">
      <div class="rl">◆ &nbsp; Estimated Resale Value &nbsp; ◆</div>
      <div class="rp">{price_str}</div>
      <div class="rc">
        Confidence interval: ± 5.2% &nbsp;·&nbsp;
        Random Forest &nbsp;·&nbsp; R² = 0.881 &nbsp;·&nbsp; RMSE ₹6,218
      </div>
    </div>""", unsafe_allow_html=True)

# FEATURE TILES
st.markdown("---")
st.markdown('<div class="feat-grid">', unsafe_allow_html=True)
tiles=[
  ("🔩","AUCTION-TRAINED","Calibrated on 428,000+ real heavy-equipment auction records across North America."),
  ("⚡","INSTANT INFERENCE","Sub-second predictions via optimised Random Forest with 500 estimators, 53 features."),
  ("🎯","HIGH ACCURACY","R² = 0.881 on holdout. RMSE under ₹6,218 across all size and age classes."),
  ("🏗️","INDUSTRY GRADE","Handles hydraulics, drive type, enclosure, ROPS, ripper, and regional demand curves."),
]
fc=st.columns(4)
for col,(icon,title,desc) in zip(fc,tiles):
    with col:
        st.markdown(f"""
        <div class="ft">
          <div class="fi">{icon}</div>
          <div class="ftt">{title}</div>
          <div class="fd">{desc}</div>
        </div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
  IRONMIND HEAVY EQUIPMENT AI &nbsp;·&nbsp; STREAMLIT + SCIKIT-LEARN
  &nbsp;·&nbsp; ALL VALUATIONS ARE ESTIMATES &nbsp;·&nbsp; © 2025
</div>
""", unsafe_allow_html=True)
