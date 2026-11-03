"""Build explorer.html: an interactive UNIRA simulator.
Plain HTML + ES5 JavaScript, no libraries, data embedded -> works offline and in older Safari.
Results are looked up from grids.json, computed by the tested Python models (build_grids.py)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "v67" / "dashboard"))
from build_dashboard import CSS  # noqa: E402

JS = r"""
var G = __GRIDS__;
function $(id){return document.getElementById(id);}
function val(id){return $(id).value;}
function fmtYear(y){return (y===null||y===undefined)?'not within 30 years':'year '+y;}
function y1(){
  var reg=val('y1region'), emp=parseInt(val('y1emp'),10), th=val('y1theta'), av=val('y1avoid'), rho=parseFloat(val('y1rho'));
  $('y1empv').innerHTML=emp+'%';
  var r=null;
  for(var i=0;i<G.year1.length;i++){var x=G.year1[i]; if(x.region===reg&&x.employment===emp&&x.theta===th&&x.avoidable===av&&x.rho===rho){r=x;break;}}
  if(!r){$('y1out').innerHTML='No result for this combination.';return;}
  var closed = r.gain<=0;
  $('y1out').innerHTML='<b class="big">'+(closed?'0%':r.gain.toFixed(1)+'%')+'</b><br>extra output per hour still needed in year 1'+(closed?' &mdash; <b>the gap is closed</b>':'');
  var tot=r.theta_share+r.mob_share+r.avoid_share, parts=[['Productivity response',r.theta_share,'c3'],['New workers',r.mob_share,'c1'],['Less market-specific work',r.avoid_share,'c2']];
  var svg='<svg viewBox="0 0 700 120" role="img" aria-label="How the hours gap is covered">', x0=10, w=600;
  for(var j=0;j<parts.length;j++){var pw=Math.min(parts[j][1],100-Math.max(0,x0-10)/w*100)/100*w; if(pw<0)pw=0;
    svg+='<rect x="'+x0+'" y="20" width="'+pw+'" height="34" class="b'+parts[j][2]+'"><title>'+parts[j][0]+': '+parts[j][1]+'%</title></rect>';
    svg+='<text x="'+(x0+2)+'" y="76" class="s">'+parts[j][0]+'</text><text x="'+(x0+2)+'" y="92" class="s">'+parts[j][1].toFixed(0)+'%</text>'; x0+=pw;}
  svg+='<line x1="'+(10+w)+'" x2="'+(10+w)+'" y1="12" y2="62" class="refl"/><text x="'+(10+w-4)+'" y="10" text-anchor="end" class="s">whole gap (100%)</text></svg>';
  $('y1bar').innerHTML=svg+'<p class="note">Share of the hours lost under a 30-hour week that each source covers'+(tot>100?' (together they cover more than the gap)':'')+'.</p>';
}
function wd(){
  var sys=val('wsys'), e=parseFloat(val('wenergy')), gov=val('wgov'), hg=parseFloat(val('whousing'));
  $('wgov').disabled=(sys!=='unira'); if(sys!=='unira'){gov='perfect';}
  var r=null;
  for(var i=0;i<G.world.length;i++){var x=G.world[i]; if(x.system===sys&&x.energy_build===e&&x.governance===gov&&x.housing_growth===hg){r=x;break;}}
  if(!r){$('wout').innerHTML='No result.';return;}
  $('wout').innerHTML='<table><tr><th></th><th>Share of the world shortfall closed</th><th>Everyone reaches the comfortable level</th></tr>'+
   '<tr><td>Energy (40 GJ per person)</td><td><b>'+r.energy_y15+'%</b> by year 15</td><td>'+fmtYear(r.energy_all_by)+'</td></tr>'+
   '<tr><td>Health workers (131 per 10,000)</td><td><b>'+r.health_y15+'%</b> by year 15</td><td>'+fmtYear(r.health_all_by)+'</td></tr>'+
   '<tr><td>Homes (27 m2 per person)</td><td><b>'+r.housing_y30+'%</b> by year 30</td><td>'+fmtYear(r.housing_all_by)+'</td></tr></table>'+
   '<p class="note">Peak world final energy: '+r.peak_energy_ej+' EJ (today about 409 EJ in the model). Negative values mean the gap grows.</p>';
  var x0=50,x1=640,y0=20,yb=220, sx=function(t){return x0+t/30*(x1-x0);}, sy=function(v){v=Math.max(-40,Math.min(100,v));return yb-(v+40)/140*(yb-y0);};
  var svg='<svg viewBox="0 0 700 260" role="img" aria-label="Shortfall closed over 30 years">';
  var ticks=[-40,0,50,100]; for(var k=0;k<ticks.length;k++){svg+='<line x1="'+x0+'" x2="'+x1+'" y1="'+sy(ticks[k])+'" y2="'+sy(ticks[k])+'" class="gridl"/><text x="'+(x0-6)+'" y="'+(sy(ticks[k])+4)+'" text-anchor="end" class="s">'+ticks[k]+'%</text>';}
  for(var t=0;t<=30;t+=5){svg+='<text x="'+sx(t)+'" y="'+(yb+18)+'" text-anchor="middle" class="s">'+t+'</text>';}
  var names=['Energy','Health workers','Homes'], cls=['c1','c2','c3'];
  for(var s=0;s<3;s++){var d='';for(var q=0;q<r.series.length;q++){d+=(q?'L':'M')+sx(r.series[q][0])+','+sy(r.series[q][s+1]);}
    svg+='<path d="'+d+'" class="ln l'+cls[s]+'"/>'; var last=r.series[r.series.length-1]; svg+='<text x="'+(x1+4)+'" y="'+(sy(last[s+1])+4+(s-1)*12)+'" class="s t'+cls[s]+'">'+names[s]+'</text>';}
  svg+='<text x="'+((x0+x1)/2)+'" y="'+(yb+36)+'" text-anchor="middle" class="s">years from start</text></svg>';
  $('wchart').innerHTML=svg;
}
window.onload=function(){y1();wd();};
"""

EXTRA_CSS = """
.big{font-size:40px;line-height:1.1}.ctl{display:block;margin:10px 0}.ctl select,.ctl input{font-size:15px;margin-left:6px}
.bc1{fill:var(--acc)}.bc2{fill:var(--g2)}.bc3{fill:var(--g3)}.refl{stroke:var(--mut);stroke-dasharray:4 4}
.gridl{stroke:var(--line)}.ln{fill:none;stroke-width:2.4}.lc1{stroke:var(--acc)}.lc2{stroke:var(--g2)}.lc3{stroke:var(--g3)}
.tc1{fill:var(--acc)}.tc2{fill:var(--g2)}.tc3{fill:var(--g3)} svg text{font-size:12px} .panel{background:var(--card);border-radius:12px;padding:16px;margin:16px 0}
"""


def main():
    grids = (HERE / "grids.json").read_text()
    body = """
<div class="wrap"><header><p>UNIRA research · interactive simulator · results from the tested open models</p>
<h1>Explore UNIRA yourself</h1>
<p>Change the assumptions and see the results. Every number comes from the same Python models used in the research,
computed in advance for each combination. Nothing is invented in your browser.</p></header>

<h2>1. A 30-hour week from year 1</h2>
<div class="panel">
<label class="ctl">Region <select id="y1region" onchange="y1()"><option value="FR">France</option><option value="EU27_2020">European Union (pooled as one entity)</option></select></label>
<label class="ctl">Employment rate, ages 20-64 (France 75.4% in 2025): <span id="y1empv"></span><br>
<input id="y1emp" type="range" min="76" max="92" step="2" value="88" oninput="y1()" onchange="y1()" style="width:100%"></label>
<label class="ctl">How much shorter hours raise productivity <select id="y1theta" onchange="y1()"><option value="low">low (evidence low end)</option><option value="central" selected>central</option><option value="high">high (evidence high end)</option></select></label>
<label class="ctl">Reduction of market-specific work (advertising, speculation...) <select id="y1avoid" onchange="y1()"><option value="modest">modest</option><option value="moderate" selected>moderate</option><option value="deep">deep</option></select></label>
<label class="ctl">Productivity of new workers in year 1 <select id="y1rho" onchange="y1()"><option value="0.75" selected>75% of experienced workers</option><option value="1">100%</option></select></label>
<div id="y1out"></div><div id="y1bar"></div>
</div>

<h2>2. The world over 30 years</h2>
<div class="panel">
<label class="ctl">Economic system <select id="wsys" onchange="wd()"><option value="market">Reformed market economy</option><option value="cooperative_market">Very cooperative market economy</option><option value="unira" selected>UNIRA (needs-first allocation)</option></select></label>
<label class="ctl">Clean energy built each year <select id="wenergy" onchange="wd()"><option value="3.9">0.67 TW (2025 record pace)</option><option value="7" selected>1.2 TW (central)</option><option value="10.5">1.8 TW (high)</option></select></label>
<label class="ctl">How well the One Earth allocator works (UNIRA only) <select id="wgov" onchange="wd()"><option value="perfect">Perfectly</option><option value="strong" selected>Strong safeguards</option><option value="none">Typical failures, no safeguards</option><option value="worst">Worst governance ever observed</option></select></label>
<label class="ctl">Growth of home building each year <select id="whousing" onchange="wd()"><option value="0">0% (today's capacity)</option><option value="0.05">5%</option><option value="0.1" selected>10%</option></select></label>
<div id="wout"></div><div id="wchart"></div>
</div>

<h2>About these results</h2>
<p class="note">The simulator shows physical feasibility under stated assumptions, not a forecast. Assumptions marked as such in the research
(take-up of work, behaviour, governance quality) are uncertain. See the working paper, the research notes and the open code for every source and limitation.</p>
</div>
"""
    page = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>UNIRA Simulator</title><style>{CSS}{EXTRA_CSS}</style></head><body>{body}"
            f"<script>{JS.replace('__GRIDS__', grids)}</script></body></html>")
    (HERE / "explorer.html").write_text(page, encoding="utf-8")
    print("explorer.html", len(page), "bytes")


if __name__ == "__main__":
    main()
