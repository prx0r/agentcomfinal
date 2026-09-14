const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const money = (n, d=2) => Number(n).toLocaleString(undefined,{style:'currency',currency:'USD',maximumFractionDigits:d});
const num = (n,d=2) => Number(n).toLocaleString(undefined,{maximumFractionDigits:d});
const xmr = (n,d=6) => `${num(n,d)} XMR`;
const hash = (n) => n>=1e9?`${num(n/1e9,2)} GH/s`:n>=1e6?`${num(n/1e6,2)} MH/s`:n>=1e3?`${num(n/1e3,2)} kH/s`:`${num(n,0)} H/s`;
async function api(path, options={}) { const r=await fetch(path,{headers:{'Content-Type':'application/json',...(options.headers||{})},...options}); if(!r.ok) throw new Error(`${r.status} ${await r.text()}`); return r.json(); }
function nav(){return `<div class="nav"><div class="wrap nav-inner"><a class="brand" href="/"><b>XMR</b>BOT</a><div class="links"><a href="/terminal">Terminal</a><a href="/mine">Mine</a><a href="/ask">Ask</a><a href="/docs">API</a></div><div class="label"><span class="status-dot"></span>LOCAL-FIRST</div></div></div>`}
function footer(){return `<div class="footer"><div class="wrap">XMRBOT · MONERO FOR HUMANS, AGENTS AND COMPUTERS · NO CUSTODY · SEEDS STAY LOCAL</div></div>`}
async function renderNetworkMetrics(){const n=await api('/v1/network'); const set=(id,v)=>{const e=$(`#${id}`);if(e)e.textContent=v}; set('m-hashrate',hash(n.estimated_hashrate_hs));set('m-difficulty',num(n.difficulty,0));set('m-hashprice',money(n.hashprice_usd_per_khs_day,4));set('m-emission',xmr(n.daily_emission_xmr,2));set('m-price',money(n.xmr_usd,0));set('m-height',num(n.height,0)); const src=$('#network-source'); if(src)src.textContent=`source: ${n.source} · confidence ${Math.round(n.confidence*100)}%`; return n;}
function lineChart(el, rows, key){ if(!el||!rows.length)return; const vals=rows.map(r=>Number(r[key])); const min=Math.min(...vals),max=Math.max(...vals),range=max-min||1; const pts=vals.map((v,i)=>`${(i/(vals.length-1||1))*100},${95-((v-min)/range)*85}`).join(' '); el.innerHTML=`<svg viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="${pts}" fill="none" stroke="#ff6600" stroke-width="1.6" vector-effect="non-scaling-stroke"/><line x1="0" y1="95" x2="100" y2="95" stroke="#293038" stroke-width=".5"/></svg><div class="sub">min ${num(min,4)} · max ${num(max,4)}</div>`;}
window.XMR={api,money,num,xmr,hash,nav,footer,renderNetworkMetrics,lineChart};
