"""Build prices.html: the UNIRA price calculator page (plain HTML + ES5, data inline, works offline and in older Safari).
python3 build_page.py  (after calculator.py)"""
import html
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path.insert(0, str(U / "v67" / "dashboard"))
from build_dashboard import CSS  # noqa: E402

JS = r"""
var P = __DATA__;
function $(id){return document.getElementById(id);}
function wt(u){var h=u/P.base_pay_u_per_hour, m=30*52/12;
  if(h<1/60){return Math.round(3600*h)+' seconds';}
  if(h<1){return Math.round(60*h)+' min';} if(h<30){return h.toFixed(1)+' hours';}
  if(h<m){return (h/30).toFixed(1)+' weeks';} return (h/m).toFixed(1)+' months';}
function calc(){var g=$('grp').value, e=parseFloat($('eur').value);
  if(!(e>=0)){$('res').innerHTML='Enter a price in euros.';return;}
  var t=P.products[g], u=e*t.u_per_euro;
  $('res').innerHTML='<b class="big">'+u.toFixed(u<10?2:0)+' U</b><br>about <b>'+wt(u)+'</b> of work at the base salary (5,000 U a month, 30 hours a week)'+
   (t.u_per_euro_within_allowance!==null?'<br><b>Step 1, within your essential energy allowance: '+(e*t.u_per_euro_within_allowance).toFixed(2)+' U</b> (about '+wt(e*t.u_per_euro_within_allowance)+' of work).<br>Step 2, up to 1.5 times the allowance: '+(e*t.u_per_euro_step2).toFixed(2)+' U.<br>Step 3, beyond that: the price above.':'')+
   (t.resource_surcharge_pct>0?'<br><span class="note">includes a resource surcharge of '+t.resource_surcharge_pct.toFixed(0)+'% (Article 13.6)</span>':'');}
window.onload=calc;
"""


def main():
    d = json.loads((HERE.parent / "outputs" / "prices.json").read_text())
    opts = "".join(f"<option value='{k}'{' selected' if k == 'CPA_A01' else ''}>{html.escape(v['label'])}</option>"
                   for k, v in sorted(d["products"].items(), key=lambda x: x[1]["label"]))
    ex = "".join(f"<tr><td>{html.escape(e['item'])}</td><td>{e['unit']}</td><td>€{e['illustrative_eur_today']:,.2f}</td>"
                 f"<td><b>{e['u_price']:,.1f} U</b></td><td>{e['work_time']}</td>"
                 f"<td>{(str(e['u_price_within_allowance']) + ' U (' + e['work_time_within_allowance'] + ')') if e['u_price_within_allowance'] is not None else '—'}</td></tr>" for e in d["examples"])
    sur = "".join(f"<tr><td>{html.escape(d['products'][k]['label'])}</td><td>+{d['products'][k]['resource_surcharge_pct']:.0f}%</td></tr>"
                  for k in d["resource_groups"])
    rows = "".join(f"<tr><td>{html.escape(v['label'])}</td><td>{v['hours_per_1000_eur']}</td><td>{v['u_per_euro']}</td>"
                   f"<td>{v['relative_to_today']}</td></tr>" for k, v in sorted(d["products"].items(), key=lambda x: x[1]["u_per_euro"]))
    body = f"""
<div class="wrap"><p><a href="index.html">← UNIRA home</a></p>
<header><p>UNIRA research V8.1 · Constitution Article 13</p><h1>What will things cost?</h1>
<p>In UNIRA, a price is the <b>hours of work</b> a product needs, all inputs included, times a price of one hour fixed forever
(<b>{d['hour_price_u']} U</b>). Goods that use scarce natural resources carry a <b>resource surcharge</b>. Prices never change afterwards;
productivity gains shorten working hours instead.</p></header>
<div class="panel"><h2>Price calculator</h2>
<label class="ctl">Kind of product <select id="grp" onchange="calc()">{opts}</select></label>
<label class="ctl">Today's price in euros <input id="eur" type="number" min="0" step="0.01" value="3" oninput="calc()" onchange="calc()"></label>
<div id="res"></div></div>
<h2>Everyday examples</h2>
<table><tr><th>Item</th><th>Unit</th><th>Today (illustrative)</th><th>UNIRA price</th><th>Work at the base salary</th><th>Within the essential energy allowance</th></tr>{ex}</table>
<p class="note">Euro prices are illustrative round figures for France around 2024, not official statistics. Each item is priced through its
product group, so the result is an average for that kind of product, not an exact price for one brand.</p>
<h2>Energy for needs is cheap</h2>
<p>Every person has an <b>essential energy allowance</b> for home electricity, heating, cooking and essential travel, set from measured needs.
Energy prices rise in three steps. <b>Step 1</b>, within the allowance: only the work it needs, a kilowatt-hour of electricity about
<b>0.17 U</b> (seconds of work), a litre of fuel about <b>0.8 U</b>. <b>Step 2</b>, up to 1.5 times the allowance: half the resource surcharge.
<b>Step 3</b>, beyond that: the full surcharge, because cheap energy beyond needs is used more and would break the climate limit.
<b>Energy used to grow and transport food is never surcharged</b>, so food stays cheap. If the allowance covers 80% of what households
use today, the household basket becomes only {d['basket_increase_pct_if_allowance_covers']['80%']}% dearer, instead of
{d['surcharge_raises_household_basket_pct']}% with the surcharge on everything.</p>
<h2>Resource surcharges (beyond the allowance)</h2>
<table><tr><th>Product group</th><th>Surcharge</th></tr>{sur}</table>
<p class="note">Each surcharge is the smallest that keeps the good at least as dear, compared with other goods, as it is today. Without it,
fuels would become about 80% cheaper and electricity about 65% cheaper, encouraging waste. The surcharges raise the cost of the
household basket by {d['surcharge_raises_household_basket_pct']}%; their revenue goes to the One Earth Fund. Homes are priced
separately (Article 18).</p>
<h2>All product groups</h2>
<table><tr><th>Product group</th><th>Hours of work per €1,000 today</th><th>U per €1 of today's price</th><th>Price relative to today</th></tr>{rows}</table>
<p class="note">Source: France's 2022 input–output table and hours worked (Eurostat), Leontief method (v63/io); the hour price is from the
money model (v64); code in v81/prices. Limits: France only, so hours embodied in imports are counted as if made in France; group averages,
not single products.</p></div>"""
    page = ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>UNIRA Prices</title><style>{CSS} .big{{font-size:34px}} .ctl{{display:block;margin:10px 0}} "
            ".ctl select,.ctl input{font-size:15px;margin-left:6px;max-width:100%} .panel{background:var(--card);border-radius:12px;padding:16px;margin:16px 0}"
            "</style></head><body>" + body + f"<script>{JS.replace('__DATA__', json.dumps({k: d[k] for k in ('products', 'base_pay_u_per_hour')}))}</script></body></html>")
    (HERE / "prices.html").write_text(page, encoding="utf-8")
    print("prices.html", len(page), "bytes")


if __name__ == "__main__":
    main()
