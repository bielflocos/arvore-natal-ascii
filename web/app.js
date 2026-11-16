'use strict';
const canvas=document.querySelector('#scene'), ctx=canvas.getContext('2d');
const C=88,R=74,W=792,H=888,TAU=Math.PI*2;
const GREEN=[40,160,88],GOLD=[255,206,82],WHITE=[211,234,241],RED=[223,49,61],BLUE=[63,98,225];
let seed=7;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
const between=(a,b)=>a+rand()*(b-a), norm=v=>{const d=Math.hypot(...v)||1;return v.map(x=>x/d);};
const points=[];
function add(x,y,z,color,char,birth,kind=0,normal=null,ao=1){points.push({x,y,z,color,char,birth,kind,n:norm(normal||[x,.25,z]),ao});}
for(let level=0;level<30;level++){
 const y=.38+level*.105,radius=1.34*(1-(y-.3)/3.5);
 for(let branch=0;branch<11;branch++)for(let j=0;j<82;j++){
  const u=between(.08,1),a=branch*TAU/11+level*1.87+between(-.25,.25)*u,r=radius*u;
  const yy=y+.12*Math.sin(u*Math.PI)-.14*u**3+between(-.03,.03),snow=rand()<.055;
  add(r*Math.cos(a),yy,r*Math.sin(a),snow?WHITE:GREEN.map(c=>c*between(.85,1.12)),snow?'#':'vxY*+;'[Math.floor(rand()*6)],1+y*1.45,0,[Math.cos(a),.35+.35*Math.sin(u*Math.PI),Math.sin(a)],.4+.6*u);
 }
}
for(let i=0;i<650;i++){const a=rand()*TAU;add(.09*Math.cos(a),between(.02,.65),.09*Math.sin(a),[124,85,55],':',1);}
for(let i=0;i<2400;i++){const u=i/2399,y=.48+2.96*u,a=u*TAU*5.3,r=1.34*(1-(y-.3)/3.5)+.025;add(r*Math.cos(a),y-.07*Math.abs(Math.sin(a*2.5)),r*Math.sin(a),GOLD,'=',6.5+u*.5,1);}
for(let j=0;j<38;j++){
 const y=between(.55,3.3),a=j*2.39996,r=1.34*(1-(y-.3)/3.5)+.025,size=between(.043,.075);
 for(let i=0;i<75;i++){const d=norm([between(-1,1),between(-1,1),between(-1,1)]);add(r*Math.cos(a)+d[0]*size,y+d[1]*size,r*Math.sin(a)+d[2]*size,j%3?RED:GOLD,'o',7+j/60,2,d);}
}
for(let j=0;j<175;j++){const y=between(.45,3.48),a=rand()*TAU,r=1.34*(1-(y-.3)/3.5)+.04;add(r*Math.cos(a),y,r*Math.sin(a),j%4?GOLD:WHITE,'*',7.5+j/175,3);}
for(let j=0;j<7;j++){
 const a=j*TAU/7,cx=1.28*Math.cos(a),cz=1.28*Math.sin(a),w=between(.28,.46),h=between(.28,.46),d=between(.28,.46),size=[w,h,d],base=[RED,GREEN,WHITE,BLUE][j%4],ribbon=j%2?RED:GOLD;
 for(let i=0;i<1900;i++){
  const p=size.map(v=>between(-.5,.5)*v),axis=Math.floor(rand()*3);p[axis]=size[axis]*(rand()<.5?-.5:.5);const n=[0,0,0];n[axis]=Math.sign(p[axis]);
  const band=axis===1?(Math.abs(p[0])<.032||Math.abs(p[2])<.032):(Math.abs(p[1])<.025||Math.abs(p[axis===0?2:0])<.032);
  add(cx+p[0],h/2+p[1],cz+p[2],band?ribbon:base,band?'#':'+',9+j*.22,4,n,.72+.28*(p[1]/h+.5));
 }
 for(let i=0;i<160;i++){const u=i/159*TAU;add(cx+.12*Math.sin(u),h+.07*Math.abs(Math.sin(2*u)),cz+.06*Math.sin(2*u),ribbon,'*',9+j*.22,4);}
}
const snow=Array.from({length:580},()=>[rand(),rand(),rand(),rand()]);
const ground=Array.from({length:7000},()=>[between(-3.7,3.7),0,between(-3.2,3.2)]);
const light=norm([-.75,.85,-.65]),half=norm([light[0],light[1]+.2,light[2]-1]);
const chars=new Array(C*R),colors=new Array(C*R),depths=new Float32Array(C*R);
const glow=document.createElement('canvas');glow.width=W;glow.height=H;const g=glow.getContext('2d');
function project(x,y,z){const s=7/(7+z);return [Math.round(C/2+x*19*s),Math.round(60-(y*13-z*2.7)*s),7+z];}
function put(x,y,ch,c){if(x>=0&&x<C&&y>=0&&y<R){const i=y*C+x;chars[i]=ch;colors[i]=c;}}
function render(t){
 chars.fill(' ');depths.fill(Infinity);colors.fill(null);
 ground.forEach((p,i)=>{const [x,y]=project(...p);if(y>=39)put(x,y,i%3?'.':'-',[24,48,57]);});
 snow.forEach(([x,y,s,p],i)=>{const b=.3+.65*(.5+.5*Math.sin(t*1.6+p*90));put(Math.floor((x*C+Math.sin(t*.6+p*50)*1.4+C)%C),Math.floor((y*R+t*(.6+s*2.8))%R),i%4?'.':'+',WHITE.map(c=>c*b));});
 const a=t*TAU/20,co=Math.cos(a),si=Math.sin(a);
 points.forEach((p,id)=>{
  if(t<p.birth)return;
  const [x,y,z]=project(p.x*co+p.z*si,p.y,-p.x*si+p.z*co);if(x<0||x>=C||y<0||y>=R)return;
  const index=y*C+x;if(z>=depths[index])return;depths[index]=z;
  const nx=p.n[0]*co+p.n[2]*si,ny=p.n[1],nz=-p.n[0]*si+p.n[2]*co;
  const diffuse=Math.max(0,nx*light[0]+ny*light[1]+nz*light[2]),fill=Math.max(0,nx*.7+ny*.2+nz*.5);
  const spec=[1,2,4].includes(p.kind)?Math.max(0,nx*half[0]+ny*half[1]+nz*half[2])**24*160:0;
  const shade=(.16+1.25*diffuse)*p.ao,fade=Math.min(1,(t-p.birth)*2),pulse=.65+.35*Math.sin(t*3+id*1.71)**2;
  colors[index]=p.color.map((v,k)=>Math.max(0,Math.min(255,(p.kind===3?v*(1.15+.65*pulse):v*shade+fill*[5,12,24][k]+spec*[1,.91,.72][k])*fade)));
  chars[index]=p.char;
 });
 if(t>=12){const [sx,sy]=project(0,3.74,0);['    +    ','    #    ','###+###','  ###  ',' ## ## '].forEach((line,j)=>[...line].forEach((ch,i)=>{if(ch!==' ')put(sx+i-Math.floor(line.length/2),sy+j-2,ch,GOLD);}));for(let d=-6;d<-2;d++)put(sx,sy+d,'|',[91,77,42]);}
 const message='M E R R Y  C H R I S T M A S  2 0 2 6',count=Math.min(message.length,Math.max(0,Math.floor((t-13)*9)));
 for(let i=0;i<count;i++)put(Math.floor((C-message.length)/2)+i,66,message[i],[RED,GOLD,GREEN][i%3]);
 ctx.fillStyle='#030a0e';ctx.fillRect(0,0,W,H);g.clearRect(0,0,W,H);
 ctx.font=g.font='12px Consolas, monospace';ctx.textBaseline=g.textBaseline='top';
 for(let i=0;i<chars.length;i++){
  if(chars[i]===' '||!colors[i])continue;const c=colors[i].map(Math.round),x=i%C*9,y=Math.floor(i/C)*12;
  ctx.fillStyle=`rgb(${c.join(',')})`;ctx.fillText(chars[i],x,y);
  if(Math.max(...c)>155){g.fillStyle=ctx.fillStyle;g.fillText(chars[i],x,y);}
 }
 ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.55;ctx.filter='blur(3px)';ctx.drawImage(glow,0,0);ctx.globalAlpha=.22;ctx.filter='blur(9px)';ctx.drawImage(glow,0,0);ctx.restore();
 canvas.dataset.time=t.toFixed(2);
}
let paused=matchMedia('(prefers-reduced-motion: reduce)').matches,time=paused?19:0,last=performance.now(),lastDraw=0;
const pause=document.querySelector('#pause'),status=document.querySelector('#status');
function sync(){pause.textContent=paused?'Continuar':'Pausar';pause.setAttribute('aria-pressed',String(paused));}sync();render(time);
function tick(now){const dt=(now-last)/1000;last=now;if(!paused&&!document.hidden)time+=dt;if(now-lastDraw>33&&!paused&&!document.hidden){render(time);lastDraw=now;}requestAnimationFrame(tick);}requestAnimationFrame(tick);
document.addEventListener('visibilitychange',()=>{last=performance.now();});
pause.onclick=()=>{paused=!paused;sync();};
document.querySelector('#restart').onclick=()=>{time=0;paused=false;sync();render(time);};
document.querySelector('#save').onclick=()=>{const a=document.createElement('a');a.download='natal-ascii.png';a.href=canvas.toDataURL('image/png');a.click();};
document.querySelector('#share').onclick=async()=>{try{if(navigator.share)await navigator.share({title:'Natal em ASCII',url:location.href});else{await navigator.clipboard.writeText(location.href);status.textContent='Link copiado. Compartilhe a magia!';}}catch(e){if(e.name!=='AbortError')status.textContent='Copie o endereço da página para compartilhar.';}};
document.addEventListener('keydown',e=>{if(e.target instanceof HTMLButtonElement)return;if(e.code==='Space'){e.preventDefault();pause.click();}if(e.key.toLowerCase()==='r')document.querySelector('#restart').click();});