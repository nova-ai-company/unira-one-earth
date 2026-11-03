import urllib.request,re,json,html,time
codes="nama_10_a64_e nama_10_a64 lfsa_ewhun2 lfsa_ewhan2 lfsa_epgan2 lfsi_sla_a lfsi_emp_a lfsa_epgar lfsa_igar lfsi_long_a lfsi_long_q lfsi_long_e06 lfsi_long_e01 lfsi_long_e08 ilc_lvhl30 hlth_rs_prs2 hlth_rs_grd2 hlth_rs_prshp2 jvs_a_rate_r2 naio_10_cp1700 demo_pjan lfst_hhnhtych lfsa_egais ilc_lvho02 ilc_hcmh02 ilc_lvph01 ilc_di01 sts_cobp_a cens_21dwop_r3".split()
out={}
for c in codes:
    try:
        x=urllib.request.urlopen("https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/"+c,timeout=60).read().decode()
        name=re.search(r'<c:Name xml:lang="en">([^<]*)',x); doi=re.search(r'doi">(10\.2908/[^&<]*)',x)
        upd=re.search(r'<c:AnnotationTitle>([^<]*)</c:AnnotationTitle><c:AnnotationType>UPDATE_DATA',x)
        out[c]={'name':html.unescape(name.group(1)) if name else None,'doi':doi.group(1) if doi else None,'update':upd.group(1) if upd else None}
    except Exception as e: out[c]={'error':str(e)}
    print(c,out[c],flush=True)
json.dump(out,open(__file__.replace('estat.py','estat.json'),'w'),indent=1)
