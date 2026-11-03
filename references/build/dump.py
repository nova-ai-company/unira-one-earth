import csv,sys
files=sys.argv[1:]
for f in files:
    rows=list(csv.DictReader(open(f,encoding='utf-8')))
    for i,r in enumerate(rows,2):
        cit=r.get('citation') or ''
        url=r.get('url') or r.get('url_or_doi') or r.get('source_url') or ''
        claim=r.get('finding') or r.get('quantity') or r.get('indicator') or r.get('item') or r.get('estimate_as_stated') or ''
        val=r.get('value') or r.get('value_as_stated') or r.get('claimed_value') or ''
        unit=r.get('unit','')
        ver=r.get('verified_in_fetched_text') or r.get('status') or ''
        ec=r.get('evidence_class','')
        print(f"{f}:{i}|{cit}|{url}|{(r.get('topic') or r.get('domain') or '')}::{claim[:110]}={val[:40]} {unit}|V:{ver[:40]}")
