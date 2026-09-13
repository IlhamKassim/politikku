'use strict';
(() => {
 window.ScrollCraft?.mount(document.querySelector("main"));
 const hero=document.querySelector('.hero'), city=document.querySelector('.city-plane'),copy=document.querySelector('.hero-copy'),orbit=document.querySelector('.sky-orbit'),act=document.querySelector('.chamber-act'),number=document.querySelector('.chamber-number');
 const circles=[...document.querySelectorAll('.seat-dot')].map(el=>({el,x:+el.dataset.x,y:+el.dataset.y,tx:+el.dataset.tx,ty:+el.dataset.ty}));
 const clamp=v=>Math.max(0,Math.min(1,v));let queued=false;
 function render(){queued=false;const off=window.motionPaused();const y=Math.min(scrollY,hero.offsetHeight);city.style.transform=off?'none':`translate3d(0,${y*.2}px,0)`;copy.style.transform=off?'none':`translate3d(0,${y*.07}px,0)`;orbit.style.transform=off?'none':`translate3d(0,${y*.32}px,0)`;const box=act.getBoundingClientRect();const p=off?1:clamp(-box.top/(act.offsetHeight-innerHeight));const phase=clamp(p*1.7);const smooth=phase*phase*(3-2*phase);circles.forEach((c,i)=>{const t=off?1:clamp((smooth-i/circles.length*.1)/.9);c.el.setAttribute('cx',String(c.x+(c.tx-c.x)*t));c.el.setAttribute('cy',String(c.y+(c.ty-c.y)*t));});number.style.opacity=String(clamp((p-.45)*4));}
 function schedule(){if(!queued){queued=true;requestAnimationFrame(render);}}addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule);addEventListener('motionchange',schedule);render();
 document.querySelector('#majority-toggle').addEventListener('click',e=>{const active=e.currentTarget.getAttribute('aria-pressed')!=='true';e.currentTarget.setAttribute('aria-pressed',String(active));document.querySelector('#seat-assembly').classList.toggle('show-majority',active);document.querySelector('#majority-note').textContent=active?'112 highlighted Seats. Enough for a Majority.':'112 Seats make a Majority.';});
})();
