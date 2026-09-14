
let state={data:null,active:null,logs:JSON.parse(localStorage.getItem('thesisdesk.logs')||'{}'),custom:JSON.parse(localStorage.getItem('thesisdesk.custom')||'[]')};
const $=s=>document.querySelector(s), esc=s=>String(s??'').replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[m]));
async function boot(){state.data=await fetch('data/trades.json').then(r=>r.json()); state.data.trades.push(...state.custom); state.active=state.data.trades[0].id; render();}
function allTrades(){return state.data.trades}
function activeTrade(){return allTrades().find(t=>t.id===state.active)}
function tabs(){ $('#tabs').innerHTML=allTrades().map(t=>`<div class="trade-tab ${t.id===state.active?'active':''}" onclick="state.active='${t.id}';render()"><b>${esc(t.name)}</b><span class="muted">${esc(t.direction)}</span><br><span class="pill">${esc(t.status)}</span></div>`).join('') }
function lineChart(points,key,target=null){
 if(!points||!points.length)return '<div class="muted">No series yet. Add data in data/trades.json.</div>';
 const W=900,H=280,pad=34, vals=points.map(p=>+p[key]).filter(Number.isFinite); if(target!=null) vals.push(target);
 let min=Math.min(...vals),max=Math.max(...vals); if(max===min){max+=1;min-=1} let span=max-min; min-=span*.08; max+=span*.08;
 const X=i=>pad+i*(W-pad*2)/Math.max(1,points.length-1), Y=v=>H-pad-(v-min)*(H-pad*2)/(max-min);
 const path=points.map((p,i)=>`${i?'L':'M'} ${X(i)} ${Y(+p[key])}`).join(' ');
 const ticks=[0,.25,.5,.75,1].map(f=>{let v=min+(max-min)*f;return `<text x="0" y="${Y(v)+4}" fill="#88939f" font-size="11">${v<1?v.toFixed(3):v.toFixed(2)}</text><line class="axis" x1="${pad}" y1="${Y(v)}" x2="${W-pad}" y2="${Y(v)}"/>`}).join('');
 const tgt=target==null?'':`<line class="targetline" x1="${pad}" y1="${Y(target)}" x2="${W-pad}" y2="${Y(target)}"/><text x="${W-pad-2}" y="${Y(target)-6}" text-anchor="end" fill="#9ba6b2" font-size="11">target ${target}</text>`;
 return `<svg viewBox="0 0 ${W} ${H}">${ticks}${tgt}<path class="chartline" d="${path}"/>${points.map((p,i)=>`<circle class="dot" cx="${X(i)}" cy="${Y(+p[key])}" r="3"><title>${esc(p.date)}: ${p[key]}</title></circle>`).join('')}<text x="${pad}" y="${H-4}" fill="#88939f" font-size="11">${esc(points[0].date)}</text><text x="${W-pad}" y="${H-4}" text-anchor="end" fill="#88939f" font-size="11">${esc(points.at(-1).date)}</text></svg>`
}
function render(){
 tabs(); const t=activeTrade(); let s=state.data.series[t.id]||[];
 let chartTitle=t.id==='xmr-zec'?'XMR market cap ÷ ZEC market cap':'NIL price (USD)';
 let chart=t.id==='xmr-zec'?lineChart(s,'ratio',1):lineChart(s,'price',.10);
 const logs=state.logs[t.id]||[];
 $('#content').innerHTML=`
 <div class="topline"><div><div class="sub">${esc(t.symbol)} · ${esc(t.horizon)}</div><div class="big">${esc(t.name)}</div><p class="muted">${esc(t.target)}</p></div><div><span class="pill">${esc(t.status)}</span><div class="sub" style="margin-top:7px">Conviction ${esc(t.conviction)}/10</div></div></div>
 <div class="toolbar"><button onclick="openLog()">+ Log update</button><button onclick="exportTrade()">Export JSON</button><button onclick="document.querySelector('#sources').scrollIntoView()">Sources</button></div>
 <div class="grid">
  <section class="card span8"><h3>${chartTitle}</h3>${chart}<div class="sub">Seed data through Sep 11, 2026. Edit data/trades.json or wire a live provider later.</div></section>
  <section class="card span4"><h3>Thesis</h3><p>${esc(t.thesis)}</p></section>
  <section class="card span12"><h3>Dashboard</h3><div class="metrics">${(t.metrics||[]).map(m=>`<div class="metric"><div class="k">${esc(m.name)}</div><div class="v">${esc(m.value)}</div><div class="d">${esc(m.asof)}</div></div>`).join('')}</div></section>
  <section class="card span6"><h3>What makes this work</h3><ul class="good">${(t.bull_case||[]).map(x=>`<li>${esc(x)}</li>`).join('')}</ul></section>
  <section class="card span6"><h3>Falsification conditions</h3><ul class="bad">${(t.falsifiers||[]).map(x=>`<li>${esc(x)}</li>`).join('')}</ul></section>
  <section class="card span12"><h3>Levels & actions</h3><table><thead><tr><th>Zone</th><th>Metric</th><th>Level</th><th>Action</th></tr></thead><tbody>${(t.levels||[]).map(x=>`<tr><td>${esc(x.label)}</td><td>${esc(x.metric)}</td><td><b>${esc(x.value)}</b></td><td>${esc(x.action)}</td></tr>`).join('')}</tbody></table></section>
  <section class="card span8"><h3>Decision log</h3><div>${logs.length?logs.slice().reverse().map(l=>`<div class="logrow"><div>${esc(l.text)}</div><div class="logmeta">${esc(l.time)} · conviction ${esc(l.conviction)}/10 · ${esc(l.action)}</div></div>`).join(''):'<p class="muted">No updates yet. Log what changed, whether it strengthens/weakens the thesis, and what you did.</p>'}</div></section>
  <section id="sources" class="card span4"><h3>Primary sources</h3>${(t.sources||[]).map(x=>`<div class="source" style="margin:8px 0"><a target="_blank" href="${esc(x.url)}">${esc(x.label)}</a></div>`).join('')}</section>
 </div>`;
}
function openLog(){let t=activeTrade(); $('#logConv').value=t.conviction; $('#logModal').classList.add('show')}
function saveLog(){let id=state.active; (state.logs[id]??=[]).push({time:new Date().toISOString(),text:$('#logText').value.trim(),conviction:+$('#logConv').value,action:$('#logAction').value}); localStorage.setItem('thesisdesk.logs',JSON.stringify(state.logs)); $('#logText').value='';$('#logModal').classList.remove('show');render()}
function exportTrade(){let t=activeTrade();let blob=new Blob([JSON.stringify({...t,logs:state.logs[t.id]||[]},null,2)],{type:'application/json'});let a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=t.id+'.json';a.click()}
function addTrade(){let name=prompt('Trade name (e.g. BTC > Gold)');if(!name)return;let id='trade-'+Date.now();let t={id,name,symbol:name,status:'OPEN',direction:'Custom thesis',target:'Define target',horizon:'Define horizon',conviction:5,thesis:'Write the thesis.',bull_case:['Add evidence/catalyst.'],falsifiers:['Add a condition that proves you wrong.'],levels:[],metrics:[],sources:[]};state.custom.push(t);state.data.trades.push(t);localStorage.setItem('thesisdesk.custom',JSON.stringify(state.custom));state.active=id;render()}
boot();
