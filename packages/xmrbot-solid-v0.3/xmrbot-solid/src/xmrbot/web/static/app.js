const $ = (s) => document.querySelector(s);
const $$ = (s) => [...document.querySelectorAll(s)];
const money = (n, d=2) => Number(n).toLocaleString(undefined,{style:'currency',currency:'USD',maximumFractionDigits:d});
const num = (n,d=2) => Number(n).toLocaleString(undefined,{maximumFractionDigits:d});
const xmr = (n,d=6) => `${num(n,d)} XMR`;
const hash = (n) => n>=1e9?`${num(n/1e9,2)} GH/s`:n>=1e6?`${num(n/1e6,2)} MH/s`:n>=1e3?`${num(n/1e3,2)} kH/s`:`${num(n,0)} H/s`;
const esc = (s='') => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
async function api(path, options={}) { const r=await fetch(path,{headers:{'Content-Type':'application/json',...(options.headers||{})},...options}); if(!r.ok) throw new Error(`${r.status} ${await r.text()}`); return r.json(); }
function shell(){return `<div class="utility"><div class="wrap utility-inner"><div class="left"><span><span class="status-dot"></span>NO CUSTODY</span><span>SEEDS STAY LOCAL</span><a href="/llms.txt">LLMS.TXT</a></div><div class="right"><a href="https://www.getmonero.org/downloads/" rel="noreferrer">OFFICIAL MONERO DOWNLOADS ↗</a><a href="/docs">OPENAPI</a></div></div></div><header class="masthead"><div class="wrap masthead-inner"><a class="brand" href="/"><img src="/static/mark.svg" alt=""><span>XMRBOT<small>MONERO INTELLIGENCE SYSTEM</small></span></a><nav class="navlinks" aria-label="Primary"><a href="/terminal">Terminal</a><a href="/mine">Mining</a><a href="/ask">Resources</a><a href="/blog">Blog</a><a href="/recipes">Recipes</a><a class="machine" href="/v1/site/map">Agents</a></nav></div></header>`}
function pagebar(section='SYSTEM'){return `<div class="pagebar"><div class="wrap"><div class="breadcrumb">XMRBOT / ${esc(section.toUpperCase())}</div><div class="pagebar-note"><b>■</b> MACHINE-READABLE · API + MCP</div></div></div>`}
function footer(){return `<footer class="footer"><div class="wrap"><div class="footer-grid"><div><div class="footer-brand">XMRBOT</div><p>Monero intelligence, mining economics and agent-native resources. Independent project; not affiliated with the Monero Project.</p></div><div><a href="/terminal">Terminal</a><a href="/mine">Mining calculator</a><a href="/blog">Research blog</a><a href="/recipes">Content recipes</a></div><div><a href="/v1/tools">Tool catalog</a><a href="/v1/site/map">Machine site map</a><a href="/llms.txt">LLM guide</a><a href="/docs">OpenAPI</a></div></div><div class="footer-note">NO CUSTODY · NO SEED COLLECTION · METHODOLOGY-LINKED METRICS · TRUST-CRITICAL EXECUTION STAYS LOCAL</div></div></footer>`}
function mountShell(section){ const n=$('#nav'),f=$('#footer'),p=$('#pagebar');if(n)n.innerHTML=shell();if(p)p.innerHTML=pagebar(section);if(f)f.innerHTML=footer(); }
async function renderNetworkMetrics(){const n=await api('/v1/network'); const set=(id,v)=>{const e=$(`#${id}`);if(e)e.textContent=v}; set('m-hashrate',hash(n.estimated_hashrate_hs));set('m-difficulty',num(n.difficulty,0));set('m-hashprice',money(n.hashprice_usd_per_khs_day,4));set('m-emission',xmr(n.daily_emission_xmr,2));set('m-price',money(n.xmr_usd,0));set('m-height',num(n.height,0));set('m-reward',xmr(n.reward_xmr,3)); const src=$('#network-source'); if(src)src.textContent=`${n.source} · confidence ${Math.round(n.confidence*100)}%`; return n;}
function lineChart(el, rows, key){ if(!el||!rows.length)return; const vals=rows.map(r=>Number(r[key])); const min=Math.min(...vals),max=Math.max(...vals),range=max-min||1; const pts=vals.map((v,i)=>`${(i/(vals.length-1||1))*100},${95-((v-min)/range)*85}`).join(' '); el.innerHTML=`<svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-label="metric line chart"><polyline points="${pts}" fill="none" stroke="#ff6600" stroke-width="1.5" vector-effect="non-scaling-stroke"/><line x1="0" y1="95" x2="100" y2="95" stroke="#46505a" stroke-width=".5"/></svg><div class="sub">LOW ${num(min,4)} · HIGH ${num(max,4)}</div>`;}
function inlineMd(text){return esc(text).replace(/`([^`]+)`/g,'<code>$1</code>').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>').replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g,'<a href="$2" rel="noreferrer">$1</a>')}
function markdown(md=''){
  const lines=String(md).replace(/\r/g,'').split('\n');let out='',inList=false,inCode=false,code=[];
  const closeList=()=>{if(inList){out+='</ul>';inList=false}};
  for(const raw of lines){
    if(raw.startsWith('```')){closeList();if(inCode){out+=`<pre>${esc(code.join('\n'))}</pre>`;code=[];inCode=false}else inCode=true;continue}
    if(inCode){code.push(raw);continue}
    if(/^###\s+/.test(raw)){closeList();out+=`<h3>${inlineMd(raw.replace(/^###\s+/,''))}</h3>`;continue}
    if(/^##\s+/.test(raw)){closeList();out+=`<h2>${inlineMd(raw.replace(/^##\s+/,''))}</h2>`;continue}
    if(/^#\s+/.test(raw)){closeList();out+=`<h2>${inlineMd(raw.replace(/^#\s+/,''))}</h2>`;continue}
    if(/^[-*]\s+/.test(raw)){if(!inList){out+='<ul>';inList=true}out+=`<li>${inlineMd(raw.replace(/^[-*]\s+/,''))}</li>`;continue}
    if(!raw.trim()){closeList();continue}
    closeList();out+=`<p>${inlineMd(raw)}</p>`;
  }
  closeList();if(inCode)out+=`<pre>${esc(code.join('\n'))}</pre>`;return out;
}
function fmtDate(v){if(!v)return 'UNPUBLISHED';return new Date(v).toLocaleDateString(undefined,{year:'numeric',month:'short',day:'2-digit'}).toUpperCase()}
window.XMR={api,money,num,xmr,hash,esc,shell,pagebar,footer,mountShell,renderNetworkMetrics,lineChart,markdown,fmtDate};
