import json,sys,urllib.request,urllib.parse
for q in sys.argv[1:]:
    u='https://api.openalex.org/works?per-page=3&search='+urllib.parse.quote(q)
    try: d=json.load(urllib.request.urlopen(u,timeout=40))
    except Exception as e: print('ERR',q,e); continue
    print('##',q)
    for w in d.get('results',[]):
        au=', '.join(a['author']['display_name'] for a in w.get('authorships',[])[:4])
        b=w.get('biblio',{}); src=((w.get('primary_location') or {}).get('source') or {}).get('display_name')
        print('  ',w.get('publication_year'),'|',au,'|',w.get('title'),'|',src,b.get('volume'),b.get('issue'),b.get('first_page'),b.get('last_page'),'|',w.get('doi'))
