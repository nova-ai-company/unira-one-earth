import sys,subprocess,re,json,concurrent.futures as cf,html
urls=[l.strip() for l in open(sys.argv[1]) if l.strip()]
def chk(u):
    try:
        p=subprocess.run(['curl','-sL','-m','25','-A','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15','-r','0-60000','-w','\n__CODE__%{http_code} %{content_type}',u],capture_output=True,timeout=40)
        b=p.stdout.decode('utf-8','replace'); code=b.rsplit('__CODE__',1)[-1]
        t=re.search(r'<title[^>]*>(.*?)</title>',b,re.S|re.I)
        return u,code,html.unescape(re.sub(r'\s+',' ',t.group(1)).strip())[:160] if t else ''
    except Exception as e: return u,'ERR',str(e)[:80]
with cf.ThreadPoolExecutor(10) as ex: res=list(ex.map(chk,urls))
json.dump(res,open(sys.argv[2],'w'),indent=0)
for r in res: print(' | '.join(r))
