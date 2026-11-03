import json,sys,urllib.request,os,time,concurrent.futures as cf
S=os.path.dirname(os.path.abspath(__file__)); cache=os.path.join(S,'csl.json')
C=json.load(open(cache)) if os.path.exists(cache) else {}
C={k:v for k,v in C.items() if 'error' not in v}
def get(doi):
    for t in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request('https://doi.org/'+doi,headers={'Accept':'application/vnd.citationstyles.csl+json','User-Agent':'UNIRA-bib/1.0'}),timeout=40)
            return doi,json.loads(r.read().decode('utf-8'))
        except Exception as e:
            err=str(e); time.sleep(3*(t+1))
    return doi,{'error':err}
dois=[l.strip() for l in open(sys.argv[1]) if l.strip()]
todo=[d for d in dois if d not in C]
with cf.ThreadPoolExecutor(4) as ex:
    for d,m in ex.map(get,todo): C[d]=m
json.dump(C,open(cache,'w'))
for d in dois:
    m=C[d]
    if 'error' in m: print('ERR',d,m['error']); continue
    au='; '.join(a.get('family',a.get('literal','')) for a in m.get('author',[]))[:80]
    y=(m.get('issued',{}).get('date-parts') or [[None]])[0][0]
    ct=m.get('container-title'); ct=ct[0] if isinstance(ct,list) and ct else ct
    print(d,'|',y,'|',au,'|',str(m.get('title'))[:90],'|',str(ct)[:40],m.get('volume'),m.get('issue'),m.get('page'))
