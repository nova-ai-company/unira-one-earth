# Peer-reviewed articles (group 'article'); metadata filled from doi.org (Crossref/DataCite CSL-JSON) when ver='doi'.
from reg import R

A = 'article'
# ---------------- Hours and productivity (v62/audit) ----------------
R('pencavel2015', A, 'article', 'doi', pats=[r'Pencavel'], md=[r'Pencavel'], doi='10.1111/ecoj.12166',
  note='Working-paper version: IZA DP 8129 (2014), https://docs.iza.org/dp8129.pdf (the version read in the project)')
R('collewet2017', A, 'article', 'doi', pats=[r'Collewet'], md=[r'Collewet'], doi='10.1016/j.labeco.2017.03.006',
  note='Working-paper version read: IZA DP 10722, https://docs.iza.org/dp10722.pdf')
R('gubian2004', A, 'article', 'doi', pats=[r'Gubian'], md=[r'Gubian', r'DARES'], doi='10.3406/estat.2004.7233',
  note='PDF read: https://www.insee.fr/fr/statistiques/fichier/1376464/es376377b.pdf',
  prob='Title in v62/audit/hours_productivity_evidence.csv reads "des simulations ex ante aux evaluations ex post"; the DOI record (Persée) reads "des estimations ex ante aux évaluations ex post". Issue is the double issue 376-377 (DOI metadata lists 376).')
R('crepon2004', A, 'article', 'doi', pats=[r'Crepon B\., Leclair', r'Crépon, Leclair'], md=[r'Cr[ée]pon, Leclair'], doi='10.3406/estat.2004.7234',
  note='PDF read: https://www.insee.fr/fr/statistiques/fichier/1376466/es376377c.pdf')
R('asai2024', 'report', 'techreport', 'false', pats=[r'Asai K\.'], md=[r'Asai'],
  author='Asai, Kentaro and Lopes, M. C. and Tondini, A.', title='Firm-Level Effects of Reductions in Working Hours',
  institution='Paris School of Economics', year='2024', type='Working paper',
  url='https://www.parisschoolofeconomics.eu/app/uploads/2024/11/asai-kentaro-firm-level-effects-of-reductions-in-working-hours.pdf', urldate='2026-11-03',
  note='Merges Asai (2022) and Lopes \\& Tondini (2022)',
  prob='Working paper (not peer-reviewed); co-authors given as initials only.')
R('batut2023', A, 'article', 'doi', pats=[r'Batut'], md=[r'Batut'], doi='10.1111/irel.12323',
  note='Working-paper version read: IZA DP 15566, https://docs.iza.org/dp15566.pdf')
R('park2019', A, 'article', 'doi', pats=[r'Park W\. & Park Y'], md=[r'Park & Park'], doi='10.1002/pam.22136',
  note='Version read: KDI working paper via EconPapers (RePEc:zbw:kdifor:267, titled "The Impact of a Workweek Reduction on Labor Productivity")')
R('hunt1999', A, 'article', 'doi', pats=[r'Hunt J\.'], md=[r'Hunt \(?1999', r'Hunt 1999'], doi='10.1162/003355399555963',
  note='Working-paper version: NBER WP 5724 (1996), https://www.nber.org/papers/w5724')
R('crepon2002', A, 'article', 'doi', pats=[r'Crepon B\. & Kramarz', r'Crépon & Kramarz'], md=[r'Kramarz'], doi='10.1086/342807',
  note='Working-paper version: IZA DP 416')
R('chemin2009', A, 'article', 'doi', pats=[r'Chemin'], md=[r'Chemin'], doi='10.1086/605426')
R('estevao2008', A, 'article', 'doi', pats=[r'Estevao'], md=[r'Estev[ãa]o'], doi='10.1111/j.1468-0327.2008.00204.x',
  prob='Pages: DOI record gives 417-463 (as in the project); the RePEc page used as URL gives 418-463.')
R('raposo2010', A, 'article', 'doi', pats=[r'Raposo'], md=[r'Raposo', r'van Ours'], doi='10.1016/j.econlet.2009.10.001')
R('kawaguchi2017', A, 'article', 'doi', pats=[r'Kawaguchi'], md=[r'Kawaguchi'], doi='10.1016/j.jjie.2016.12.002',
  note='Earlier version: ESRI Discussion Paper 202 (2008)')
R('sanchez2013', A, 'article', 'doi', pats=[r'Sanchez R\.'], md=[r'S[áa]nchez'], doi='10.1016/j.labeco.2012.10.001')
R('rogers2004', A, 'article', 'doi', pats=[r'Rogers A\.E'], md=[r'Rogers et al'], doi='10.1377/hlthaff.23.4.202')
R('dallora2015', A, 'article', 'doi', pats=[r"Dall'Ora"], md=[r"Dall'Ora"], doi='10.1136/bmjopen-2015-008331')
R('griffiths2014', A, 'article', 'doi', pats=[r'Griffiths P\.'], md=[r'Griffiths et al'], doi='10.1097/MLR.0000000000000233',
  prob='v62/audit/hours_productivity_evidence.csv gives no volume/pages; DOI record: Medical Care 52(11):975-981.')
R('aiken2014', A, 'article', 'doi', pats=[r'Aiken L\.H\. et al'], md=[r'Aiken et al', r'RN4CAST'], doi='10.1016/S0140-6736(13)62631-8',
  prob='Project marks volume/pages "unverified"; DOI record: The Lancet 383(9931):1824-1830 (now verified).')
R('skuterud2007', A, 'article', 'doi', pats=[r'Skuterud'], md=[r'Skuterud'], doi='10.1086/511379',
  prob='Cited only second-hand (via Batut et al. 2023); not read in the project.')
R('gonzaga2003', 'other', 'misc', 'false', pats=[r'Gonzaga G\. et al'], md=[r'Gonzaga'],
  author='Gonzaga, G. and others', title='[Brazil 1988 working-time reform study]', year='2003', note='Cited second-hand in batut2023; not read',
  prob='Incomplete: no title, venue or co-authors in project files (cited via Batut et al. 2023); UNVERIFIED.')
R('varejao2005', 'other', 'misc', 'false', pats=[r'Varejao J\.'], md=[r'Varej[ãa]o'],
  author='Varejão, J.', title='[Portugal 1996 working-time reform study]', year='2005', note='Cited second-hand in batut2023; not read',
  prob='Incomplete: no title or venue in project files (cited via Batut et al. 2023); UNVERIFIED.')
R('autonomy2021iceland', 'report', 'techreport', 'false', pats=[r'Autonomy & Alda'], md=[r'Autonomy & Alda', r'Iceland\'s journey'],
  author='{Autonomy} and {Alda}', title="Going Public: Iceland's journey to a shorter working week", institution='Autonomy; Alda', year='2021',
  url='https://en.alda.is/wp-content/uploads/2021/07/ICELAND_4DW.pdf', urldate='2026-11-03')
R('autonomy2023uk', 'report', 'techreport', 'false', pats=[r'Autonomy et al\. \(2023\)'], md=[r'Autonomy et al'],
  author='{Autonomy} and others', title="The results are in: The UK's four-day week pilot", institution='Autonomy', year='2023',
  url='https://autonomy.work/wp-content/uploads/2023/02/The-results-are-in-The-UKs-four-day-week-pilot.pdf', urldate='2026-11-03',
  prob='Co-authoring organisations/individual authors not listed in project files ("Autonomy et al.").')
R('mg2015svartedalen', 'other', 'misc', 'url', pats=[r'Svartedalen'], md=[r'Svartedalen'],
  author='{Mail \\& Guardian}', title='Efficiency up, turnover down: Sweden experiments with six-hour working day', year='2015',
  url='https://mg.co.za/article/2015-09-17-efficiency-up-turnover-down-sweden-experiments-with-six-hour-working-day', urldate='2026-11-03',
  note='Press report (17 September 2015); official evaluation not located', vtok='six-hour',
  prob='Svartedalen trial: press report only; official evaluation not located (marked UNVERIFIED in v62/audit).')

# ---------------- Thresholds / decent living (v65) ----------------
R('millwardhopkins2020', A, 'article', 'doi', pats=[r'Millward-Hopkins', r'\bMH2020\b'], md=[r'Millward-Hopkins', r'\bMH2020\b', r'15\.3 GJ'],
  doi='10.1016/j.gloenvcha.2020.102168', note='Open-access copy: https://pure.iiasa.ac.at/16764/')
R('kikstra2021', A, 'article', 'doi', pats=[r'Kikstra'], md=[r'Kikstra'], doi='10.1088/1748-9326/ac1c27')
R('rao2019', A, 'article', 'doi', pats=[r'Rao N\.D\. Min J\. Mastrucci', r'Rao Min & Mastrucci'], md=[r'Rao, Min & Mastrucci', r'Rao 2019'],
  doi='10.1038/s41560-019-0497-9', prob='Primary article not fetched in the project; the 12-24 (or 11-24) GJ range in v65/thresholds came from a secondary citation and is ambiguous.')
R('grubler2018', A, 'article', 'doi', pats=[r'Grubler'], md=[r'Gr[uü]bler', r'\bLED\b scenario', r'245 EJ'], doi='10.1038/s41560-018-0172-6')
R('mcelroy2025', A, 'article', 'doi', pats=[r'McElroy'], md=[r'McElroy'], doi='10.1016/j.gloenvcha.2025.103008',
  note='Preprint read: arXiv 2411.06337')
R('rao2018', A, 'article', 'doi', pats=[r'Rao N\.D\. Min J\. \(2018\)', r'Rao & Min'], md=[r'Rao & Min'], doi='10.1007/s11205-017-1650-0',
  note='Open-access copy: https://pure.iiasa.ac.at/id/eprint/14606/')
R('gleick1996', A, 'article', 'doi', pats=[r'Gleick 1996'], md=[r'Gleick'], doi='10.1080/02508069608686494',
  prob='Cited second-hand (via WHO 2020) in v65/thresholds; not read in the project.')
R('who2007protein', 'report', 'techreport', 'false', pats=[r'WHO/FAO/UNU'], md=[r'TRS 935', r'0\.83 g'],
  author='{World Health Organization} and {Food and Agriculture Organization of the United Nations} and {United Nations University}',
  title='Protein and amino acid requirements in human nutrition', institution='World Health Organization',
  year='2007', number='935', type='WHO Technical Report Series', url='https://iris.who.int/handle/10665/43411', urldate='2026-11-03')
R('who2016workforce2030', 'report', 'techreport', 'url', pats=[r'Workforce 2030'], md=[r'WHO 2016', r'44\.5'],
  author='{World Health Organization}', title='Global strategy on human resources for health: Workforce 2030', institution='World Health Organization',
  year='2016', url='https://www.who.int/publications/i/item/9789241511131', urldate='2026-11-03', vtok='Workforce 2030')
R('who2020water', 'report', 'techreport', 'url', pats=[r'Domestic water quantity', r'WHO 2020 \(PDF'], md=[r'WHO 2020'],
  author='{World Health Organization}', title='Domestic water quantity, service level and health', edition='2nd', institution='World Health Organization',
  year='2020', url='https://www.who.int/publications/i/item/9789240015241', urldate='2026-11-03', vtok='Domestic water')
R('enerdata2024sufficiency', 'report', 'techreport', 'false', pats=[r'Enerdata'], md=[r'ODYSSEE', r'Enerdata'],
  author='{Enerdata} and {ODYSSEE-MURE}', title='Energy sufficiency in the EU: a selection of indicators (workshop slides, Rome 2024)', institution='Enerdata / ODYSSEE-MURE',
  year='2024', url='https://www.odyssee-mure.eu/private/workshop-papers/rome-2024/2_4-Energy-Sufficiency-Indicators-Enerdata.pdf', urldate='2026-11-03',
  prob='Workshop slides (grey literature); individual authors not recorded.')
R('oecd2025haag', 'report', 'book', 'false', pats=[r'Health at a Glance 2025'], md=[r'Health at a Glance'],
  author='{OECD}', title='Health at a Glance 2025', publisher='OECD', year='2025',
  url='https://www.oecd.org/en/publications/health-at-a-glance-2025_8f9e3f98-en.html', urldate='2026-11-03',
  prob='OECD pages blocked (403); the 3.9 doctors / 9.2 nurses per 1000 values come from a search snippet only (v65/thresholds.csv row 27).')

# ---------------- Ecology (v66/ecology) ----------------
R('ipcc2021wg1spm', 'report', 'incollection', 'doi', pats=[r'IPCC AR6 WG1', r'IPCC_AR6_WGI_SPM'], md=[r'IPCC AR6 WG1', r'Table SPM\.2'],
  doi='10.1017/9781009157896.001', author='{IPCC}', title='Summary for Policymakers',
  booktitle='Climate Change 2021 -- The Physical Science Basis',
  publisher='Cambridge University Press', year='2021', pages='3--32',
  url='https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf', urldate='2026-11-03',
  note='Working Group I contribution to the IPCC Sixth Assessment Report; DOI version published by Cambridge University Press in 2023')
R('ipcc2022wg3ch3', 'report', 'incollection', 'doi', pats=[r'IPCC AR6 WG3', r'IPCC_AR6_WGIII_Chapter03'], md=[r'IPCC AR6 WG3', r'WG3', r'C1 pathways', r'IPCC 1\.5'],
  doi='10.1017/9781009157926.005', author='{IPCC}', title='Mitigation Pathways Compatible with Long-term Goals (Chapter 3)',
  booktitle='Climate Change 2022 -- Mitigation of Climate Change',
  publisher='Cambridge University Press', year='2022', pages='295--408',
  url='https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_Chapter03.pdf', urldate='2026-11-03',
  note='Working Group III contribution to the IPCC Sixth Assessment Report; DOI version published by Cambridge University Press in 2023',
  prob='Chapter author list (Coordinating Lead Authors) not recorded in project files and not confirmed here (DOI metadata lists no authors); cited with institutional author IPCC.')
R('ipcc_ar6', extend=False, group='report', bibtype='misc', ver='false', pats=[], md=[r'IPCC AR6(?! WG)'],
  author='{IPCC}', title='Sixth Assessment Report (AR6) -- generic reference; see ipcc2021wg1spm and ipcc2022wg3ch3',
  url='https://www.ipcc.ch/assessment-report/ar6/', urldate='2026-11-03',
  prob='Working Paper source table cites "IPCC AR6" generically; replace with ipcc2021wg1spm (carbon budgets) and/or ipcc2022wg3ch3 (energy pathways).')
R('lamboll2023', A, 'article', 'doi', pats=[r'Lamboll'], md=[r'Lamboll'], doi='10.1038/s41558-023-01848-5')
R('forster2025', A, 'article', 'doi', pats=[r'Forster et al'], md=[r'Forster'], doi='10.5194/essd-17-2641-2025',
  prob='Book Ch.10 notes a "caption inconsistency" in Forster et al. 2025 Table 8; values used should state which number (table vs caption) was taken.')
R('gcp2025release', 'report', 'misc', 'url', pats=[r'Global Carbon Budget 2025'], md=[r'Global Carbon Budget'],
  author='{Global Carbon Project}', title='The Global Carbon Project releases the Global Carbon Budget 2025 at COP 30 (news release)', year='2025',
  url='https://cger.nies.go.jp/gcp/news/20251113.html', urldate='2026-11-03', vtok='Global Carbon Budget 2025',
  prob='Cited via a release page (NIES mirror) and a University of Reading news page, not the peer-reviewed Global Carbon Budget 2025 paper; the 38.1 GtCO2 fossil figure is from the secondary page only (unverified).')
R('reading2025gcb', 'other', 'misc', 'url', pats=[r'reading\.ac\.uk/news/2025'], md=[],
  author='{University of Reading}', title='Global Carbon Budget -- University of Reading 2025 (news item)', year='2025',
  url='https://www.reading.ac.uk/news/2025/Research-News/Global-Carbon-Budget-University-of-Reading-2025', urldate='2026-11-03', vtok='Global Carbon Budget')
R('leeds2023news', 'other', 'misc', 'url', pats=[r'climate\.leeds\.ac\.uk'], md=[],
  author='{Priestley Centre for Climate Futures, University of Leeds}', title='Window to avoid 1.5°C of warming rapidly closing (news item on Lamboll et al. 2023)', year='2023',
  url='https://climate.leeds.ac.uk/news/window-to-avoid-1-5c-of-warming-rapidly-closing/', urldate='2026-11-03', vtok='Window to avoid')
R('iea2023nze', 'report', 'techreport', 'false', pats=[r'IEA Net Zero Roadmap', r'NetZeroRoadmap', r'same as E06'], md=[r'Net Zero Roadmap', r'442 EJ'],
  author='{International Energy Agency}', title='Net Zero Roadmap: A Global Pathway to Keep the 1.5 °C Goal in Reach -- 2023 Update', institution='IEA', year='2023',
  url='https://iea.blob.core.windows.net/assets/9a698da4-4002-4e53-8ef3-631d8971bf84/NetZeroRoadmap_AGlobalPathwaytoKeepthe1.5CGoalinReach-2023Update.pdf', urldate='2026-11-03',
  prob='v66/ecology/evidence.csv rows E07-E09 give the URL only as "same as E06".')
R('irena2026rcs', 'report', 'techreport', 'false', pats=[r'IRENA Renewable Capacity Statistics 2026', r'IRENA \(2026\)', r'irena_renewable_capacity_statistics_2026'],
  md=[r'IRENA', r'669 GW'],
  author='{International Renewable Energy Agency}', title='Renewable Capacity Statistics 2026', institution='IRENA', year='2026',
  url='https://bdd.pseau.org/outils/ouvrages/irena_renewable_capacity_statistics_2026_2026.pdf', urldate='2026-11-03',
  prob='Read from a third-party mirror (bdd.pseau.org), not irena.org.')
R('pvmagazine2026irena', 'other', 'misc', 'url', pats=[r'pv-magazine'], md=[],
  author='{pv magazine USA}', title='Global solar additions reached record 511 GW in 2025, says IRENA', year='2026',
  url='https://pv-magazine-usa.com/2026/04/02/global-solar-additions-reached-record-511-gw-in-2025-says-irena/', urldate='2026-11-03', vtok='511 GW')
R('irena2025uae', 'report', 'techreport', 'false', pats=[r'Delivering on the UAE Consensus', r'taiyangnews'], md=[r'1,?122 GW', r'1\.12 TW'],
  author='{International Renewable Energy Agency}', title='Delivering on the UAE Consensus',
  institution='IRENA', year='2025', url='https://taiyangnews.info/business/world-must-add-1122-gw-renewables-per-year-to-meet-cop28-goal', urldate='2026-11-03',
  note='Read via TaiyangNews report (October 2025)',
  prob='Report read only through a trade-press summary (TaiyangNews); full report title/subtitle not recorded.')
R('rockstrom2025', A, 'article', 'doi', pats=[r'Rockstrom', r'Rockström'], md=[r'EAT-Lancet 2025', r'Rockstr[öo]m', r'EAT[–-]Lancet(?! 2019)'], doi='10.1016/S0140-6736(25)01201-2')
R('willett2019', A, 'article', 'doi', pats=[r'Willett'], md=[r'EAT-Lancet 2019', r'Willett'], doi='10.1016/S0140-6736(18)31788-4')
R('fao2023ab71', 'report', 'techreport', 'false', pats=[r'Analytical Brief 71'], md=[r'FAO 2023', r'1\.6 bn ha'],
  author='{Food and Agriculture Organization of the United Nations}', title='FAOSTAT Analytical Brief 71 [land statistics]',
  institution='FAO', year='2023', number='71', type='FAOSTAT Analytical Brief',
  url='https://openknowledge.fao.org/server/api/core/bitstreams/5c8b2707-1bcf-4c29-90e2-3487e583f71e/content', urldate='2026-11-03',
  prob='Title of FAOSTAT Analytical Brief 71 not recorded in the project; only "FAOSTAT Analytical Brief 71 (2023)" is in the files.')
R('fao2024land', 'report', 'techreport', 'false', pats=[r'Land statistics 2001-2022'], md=[],
  author='{Food and Agriculture Organization of the United Nations}', title='Land statistics 2001--2022', institution='FAO', year='2024',
  url='https://openknowledge.fao.org/items/ddc2584a-9d58-4cde-a9a2-789a0bb93835', urldate='2026-11-03',
  prob='Values (1573/4781 Mha) not verified in fetched text; series number not recorded.')
R('unep2024fwi', 'report', 'techreport', 'false', pats=[r'Food Waste Index Report 2024', r'Food-Waste-Index-2024', r'FAO estimate as cited in UNEP'],
  md=[r'Food Waste Index (Report )?2024', r'UNEP 2024', r'1\.05 bn t', r'19 ?% of food', r'132 kg', r'[Cc]onsumer food waste 19'],
  author='{United Nations Environment Programme}', title='Food Waste Index Report 2024',
  institution='UNEP', year='2024', url='https://www.unep.org/resources/publication/food-waste-index-report-2024', urldate='2026-11-03',
  note='Key messages PDF: https://wedocs.unep.org/bitstream/handle/20.500.11822/45275/Food-Waste-Index-2024-key-messages.pdf; read via UN News (27 March 2024) because UNEP pages are behind Cloudflare',
  prob=['UNEP pages blocked (Cloudflare 403); values read via UN News; report not opened directly.',
        'v65/thresholds.csv rows 5-6 mark the 19% and 13% figures "no (search-result quote only)" while v68/verification confirms 19% (UNEP via UN News) and 13.3% (FAO SDG 12.3.1a) -- cite fao_sdg1231 for the 13% figure, not UNEP.'])
R('unnews2024foodwaste', 'other', 'misc', 'url', pats=[r'news\.un\.org/en/node/1148036'], md=[r'UN News'],
  author='{UN News}', title='With 783 million people going hungry, a fifth of all food goes to waste', year='2024',
  url='https://news.un.org/en/node/1148036', urldate='2026-11-03', note='27 March 2024; report on UNEP Food Waste Index 2024', vtok='fifth of all food')
R('unep2021fwi', 'report', 'techreport', 'url', pats=[r'Food Waste Index Report 2021'], md=[r'Food Waste Index 2021'],
  author='{United Nations Environment Programme}', title='Food Waste Index Report 2021', institution='UNEP', year='2021',
  url='https://www.unccd.int/resources/unccd-library/food-waste-index-report-2021', urldate='2026-11-03', note='Read via UNCCD library page', vtok='Food Waste Index Report 2021')
R('irp2024gro', 'report', 'techreport', 'url', pats=[r'Global Resources Outlook 2024'], md=[r'Global Resources Outlook', r'UNEP IRP', r'106 bn t'],
  author='{International Resource Panel}', title='Global Resources Outlook 2024 (press release)', institution='United Nations Environment Programme', year='2024',
  url='https://resourcepanel.org/news-events/global-resources-outlook-2024-press-release', urldate='2026-11-03', vtok='Global Resources Outlook 2024',
  prob='Only the press release was read, not the GRO 2024 report itself.')
R('oneill2018', A, 'article', 'doi', pats=[r"O'Neill et al\. 2018"], md=[r"O'Neill et al\.? 2018", r"O'Neill 2018"], doi='10.1038/s41893-018-0021-4')
R('unep2014irp', 'report', 'misc', 'false', pats=[r'UNEP 2014 \(as cited'], md=[],
  author='{United Nations Environment Programme}', title='[IRP report recommending 6--8 t/cap material use]', year='2014',
  note='Cited second-hand in oneill2018 supplementary information',
  prob='Incomplete: title of the UNEP 2014 IRP report not recorded (cited via O\'Neill et al. 2018 SI); UNVERIFIED.')
R('bringezu2015', A, 'article', 'doi', pats=[r'Bringezu'], md=[r'Bringezu'], doi='10.3390/resources4010025',
  prob='Cited via O\'Neill et al. 2018 SI ("partial" verification in v66/ecology).')
R('dittrich2012', 'report', 'misc', 'false', pats=[r'Dittrich'], md=[r'Dittrich'],
  author='Dittrich, Monika and others', title='[Material use limit study cited via O\'Neill et al. 2018]', year='2012',
  note='Cited second-hand in oneill2018 SI',
  prob='Incomplete: title/publisher of Dittrich et al. 2012 not recorded in project files; cited via O\'Neill et al. 2018 SI; UNVERIFIED.')
R('fanning2022', A, 'article', 'doi', pats=[r'Fanning'], md=[r'Fanning'], doi='10.1038/s41893-021-00799-z')

# ---------------- Health (v66/evidence_health) ----------------
R('gbd2019rf', A, 'article', 'doi', pats=[r'GBD 2019 Risk Factors', r'GBD 2019 Risk'], md=[r'GBD 2019'], doi='10.1016/S0140-6736(20)30752-2',
  note='GBD 2019 Risk Factors Collaborators; read at https://pmc.ncbi.nlm.nih.gov/articles/PMC7566194/')
R('gbd2021rf', A, 'article', 'doi', pats=[r'GBD 2021 Risk Factors'], md=[r'GBD 2021', r'GBD 2019/2021', r'41[–-]48 ?%'], doi='10.1016/S0140-6736(24)00933-4',
  note='GBD 2021 Risk Factors Collaborators')
R('gbd2021cod', A, 'article', 'doi', pats=[r'GBD 2021 Causes of Death', r'PMC11126520'], md=[r'67\.9 million'], doi='10.1016/S0140-6736(24)00367-2',
  note='GBD 2021 Causes of Death Collaborators')
R('pega2021', A, 'article', 'doi', pats=[r'Pega et al\. Environ', r'Pega et al\. 2021'], md=[r'Pega( et al\.?)? 2021', r'WHO/ILO', r'488 m', r'745,?194'], doi='10.1016/j.envint.2021.106595')
R('who2021longhours', 'other', 'misc', 'url', pats=[r'17-05-2021-long-working-hours'], md=[],
  author='{World Health Organization} and {International Labour Organization}', title='Long working hours increasing deaths from heart disease and stroke: WHO, ILO (news release)', year='2021',
  url='https://www.who.int/news/item/17-05-2021-long-working-hours-increasing-deaths-from-heart-disease-and-stroke-who-ilo', urldate='2026-11-03', note='17 May 2021', vtok='Long working hours')
R('kivimaki2015', A, 'article', 'doi', pats=[r'Kivimaki et al\. Lancet 2015'], md=[r'Kivim[äa]ki 2015'], doi='10.1016/S0140-6736(15)60295-1')
R('kivimaki2012', A, 'article', 'doi', pats=[r'Kivimaki et al\. Lancet 2012', r'pubmed\.ncbi\.nlm\.nih\.gov/22981903'], md=[r'Kivim[äa]ki 2012'], doi='10.1016/S0140-6736(12)60994-5')
R('virtanen2013', A, 'article', 'doi', pats=[r'Virtanen'], md=[r'Virtanen'], doi='10.1136/bmj.f4746')
R('roelfs2011', A, 'article', 'doi', pats=[r'Roelfs'], md=[r'Roelfs'], doi='10.1016/j.socscimed.2011.01.005')
R('richardson2013', A, 'article', 'doi', pats=[r'Richardson et al'], md=[r'Richardson 2013'], doi='10.1016/j.cpr.2013.08.009')
R('forget2011', A, 'article', 'doi', pats=[r'Forget, Canadian Public Policy 2011'], md=[r'Forget 2011', r'Mincome'], doi='10.3138/cpp.37.3.283')
R('forget2022', A, 'article', 'doi', pats=[r'Green \(2022\) critique', r'v48y2022i4p549'], md=[r'Green \(2022\)'], doi='10.3138/cpp.2022-017',
  prob='The Green (2022) re-analysis itself is not cited; only Forget\'s reply was read. Add the original critique if it is relied on.')
R('pega2022cochrane', A, 'article', 'doi', pats=[r'Pega et al\. Cochrane', r'Pega et al\. 2022'], md=[r'Cochrane 2022'], doi='10.1002/14651858.CD011135.pub3')
R('baxter2019', A, 'article', 'doi', pats=[r'Baxter'], md=[r'Baxter'], doi='10.1136/jech-2018-210981')
R('charlson2019', A, 'article', 'doi', pats=[r'Charlson'], md=[r'Charlson'], doi='10.1016/S0140-6736(19)30934-1')
R('vanbaal2008', A, 'article', 'doi', pats=[r'van Baal'], md=[r'van Baal', r'Baal 2008'], doi='10.1371/journal.pmed.0050029',
  prob='v66/evidence_health row 41 gives life-expectancy differences "5 and 8" (Editors\' summary) vs "5 and 7" (companion commentary PMC2225433): figures differ between the two sources.')
R('plosmed2008commentary', 'other', 'misc', 'url', pats=[r'PMC2225433'], md=[],
  title='Does Preventing Obesity Lead to Reduced Health-Care Costs?', howpublished='PLoS Medicine (companion commentary to van Baal et al. 2008)', year='2008',
  url='https://pmc.ncbi.nlm.nih.gov/articles/PMC2225433/', urldate='2026-11-03', vtok='Does Preventing Obesity',
  prob='Companion commentary: authors and DOI not recorded in project files.')
R('barendregt1997', A, 'article', 'doi', pats=[r'Barendregt'], md=[r'Barendregt'], doi='10.1056/NEJM199710093371506')
R('kingston2018', A, 'article', 'doi', pats=[r'Kingston'], md=[r'Kingston'], doi='10.1093/ageing/afx201')
R('barnett2012', A, 'article', 'doi', pats=[r'Barnett et al'], md=[r'Barnett'], doi='10.1016/S0140-6736(12)60240-2')
R('french2017', A, 'article', 'doi', pats=[r'French et al'], md=[r'French 2017'], doi='10.1377/hlthaff.2017.0174')
R('rose1981', A, 'article', 'doi', pats=[r'Rose G\.'], md=[r'Rose 1981', r'prevention paradox'], doi='10.1136/bmj.282.6279.1847')
R('who_hwf_page', 'other', 'misc', 'url', pats=[r'who\.int/teams/health-workforce'], md=[r'11\.1 million', r'WHO 2030 shortfall'],
  author='{World Health Organization}', title='Health workforce (WHO team page)', url='https://www.who.int/teams/health-workforce/about/30', urldate='2026-11-03', vtok='Health workforce')
R('duncan2019', A, 'article', 'doi', pats=[r'Duncan et al'], md=[r'Duncan 2019'], doi='10.1001/jama.2019.10298')
R('peto2000', A, 'article', 'doi', pats=[r'Peto et al'], md=[r'Peto 2000'], doi='10.1136/bmj.321.7257.323')
R('vartiainen2010', A, 'article', 'doi', pats=[r'Vartiainen'], md=[r'Vartiainen'], doi='10.1093/ije/dyp330')

# ---------------- Governance / allocation (v69) ----------------
R('statssa2012census', 'report', 'misc', 'false', pats=[r'Statistics South Africa'], md=[r'Stats SA', r'South Africa 2011', r'14\.6 ?%'],
  author='{Statistics South Africa}', title='Census 2011 evaluation (presentation at the UNSD workshop, Kampala, 2012)', year='2012',
  url='https://unstats.un.org/unsd/demographic/meetings/wshops/Uganda/2012/docs/South%20Africa.pdf', urldate='2026-11-03')
R('wb2020pppblog', 'other', 'misc', 'url', pats=[r'revised-2011-ppps-and-new-2017-ppps'], md=[],
  author='{World Bank}', title="How do the revised 2011 PPPs and new 2017 PPPs affect the World Bank's global poverty estimates? A first look", howpublished='World Bank Data Blog', year='2020',
  url='https://blogs.worldbank.org/en/opendata/how-do-revised-2011-ppps-and-new-2017-ppps-affect-world-banks-global-poverty-estimates', urldate='2026-11-03', vtok='revised 2011 PPPs',
  prob='Blog authors not recorded in project files.')
R('chen2010', A, 'article', 'doi', pats=[r'Chen & Ravallion'], md=[r'Chen & Ravallion'], doi='10.1162/qjec.2010.125.4.1577',
  prob='Cited second-hand via the World Bank Data Blog (v69 row 4).')
R('serajuddin2015', 'report', 'techreport', 'false', pats=[r'Serajuddin'], md=[r'Serajuddin', r'2 years late'],
  author='Serajuddin, Umar and Uematsu, Hiroki and Wieser, Christina and Yoshida, Nobuo and Dabalen, Andrew', title='Data Deprivation: Another Deprivation to End', institution='World Bank', year='2015', type='Policy Research Working Paper', number='7252',
  url='http://documents1.worldbank.org/curated/en/700611468172787967/txt/WPS7252.txt', urldate='2026-11-03',
  ver2=True, prob='Project cites only "Serajuddin et al. 2015, Data Deprivation"; full title and author list confirmed here from the World Bank text file.')
R('brown2017fd', 'other', 'misc', 'false', pats=[r'Brown, Ravallion & van de Walle, IMF'], md=[],
  author='Brown, Caitlin and Ravallion, Martin and van de Walle, Dominique', title='[Article on proxy-means-test targeting in Africa]', howpublished='Finance \\& Development (IMF), December 2017', year='2017',
  url='https://www.imf.org/external/pubs/ft/fandd/2017/12/brown.htm', urldate='2026-11-03',
  prob='F&D article title not recorded; IMF site returns 403; given names of authors taken from brown2018 DOI record.')
R('brown2018', A, 'article', 'doi', pats=[r'summarising J\. Dev\. Econ\. 2018'], md=[], doi='10.1016/j.jdeveco.2018.05.004')
R('who2026nhwa', 'report', 'techreport', 'url', pats=[r'9789240122925'], md=[r'NHWA'],
  author='{World Health Organization}', title='National health workforce accounts: health workforce levels and trends 2026', institution='World Health Organization', year='2026',
  url='https://www.who.int/publications/i/item/9789240122925', urldate='2026-11-03', vtok='health workforce levels')
R('dang2023', A, 'article', 'doi', pats=[r'Dang et al\. 2023'], md=[], doi='10.1038/s41597-023-01971-0')
R('iea2023grids', 'report', 'misc', 'false', pats=[r'IEA \(2023\) as reported by CNBC'], md=[r'5[–-]15 years'],
  author='{International Energy Agency}', title='[IEA 2023 grids report as reported by CNBC]', year='2023', note='Read via cnbc2023grids',
  prob='IEA report itself not cited by title in project files; only CNBC coverage was read.')
R('cnbc2023grids', 'other', 'misc', 'url', pats=[r'cnbc\.com/2023/10/17'], md=[],
  author='{CNBC}', title='World must add or replace 50 million miles of transmission lines: IEA', year='2023',
  url='https://www.cnbc.com/2023/10/17/world-must-add-or-replace-50-million-miles-of-transmission-lines-iea.html', urldate='2026-11-03', vtok='transmission lines')
R('reinikka2004', A, 'article', 'doi', pats=[r'Reinikka & Svensson 2004 QJE'], md=[r'Reinikka'], doi='10.1162/0033553041382120')
R('reinikka2004power', 'report', 'techreport', 'url', pats=[r'Reinikka & Svensson, World Bank'], md=[],
  author='Reinikka, Ritva and Svensson, Jakob', title='The Power of Information: Evidence from a Newspaper Campaign to Reduce Capture', institution='World Bank', year='2004',
  url='https://gsdrc.org/document-library/the-power-of-information-evidence-from-a-newspaper-campaign-to-reduce-capture/', urldate='2026-11-03', note='Read via GSDRC summary', vtok='Power of Information',
  prob=['Working-paper series/number not recorded (only a GSDRC summary was read); a published version exists (Reinikka & Svensson 2005, Journal of the European Economic Association 3(2-3):259-267, doi:10.1162/jeea.2005.3.2-3.259, verified here) and should be cited instead.',
        'Leakage figure differs: v69/evidence.csv rows 15-16 give 80% captured before the campaign (and 13% received 1991-95, i.e. 87% not received), while WORKING_PAPER_02 §9/Art.13 and the constitution say "87% -> under 20%". State which statistic is meant.'])
R('andersen2022', A, 'article', 'doi', pats=[r'Andersen, Johannesen'], md=[r'Andersen, Johannesen'], doi='10.1086/717455')
R('olken2007', A, 'article', 'doi', pats=[r'Olken 2007'], md=[r'Olken', r'Indonesia.{0,60}(audit|missing|road)', r'(audit|missing).{0,60}Indonesia'], doi='10.1086/517935',
  note='Working-paper version: NBER WP 11753, https://www.nber.org/papers/w11753',
  prob='v69 row 18 (baseline missing expenditure ~24%) is marked unverified; only the NBER abstract (8 pp reduction) was verified.')
R('avis2018', A, 'article', 'doi', pats=[r'Avis, Ferraz'], md=[r'Avis', r'Ferraz'], doi='10.1086/699209',
  note='Read via J-PAL evaluation summary: https://www.povertyactionlab.org/print/pdf/node/2327',
  prob='WORKING_PAPER_02 Art.14 attributes the Brazil audit effect to "Ferraz & Finan"; the study used is Avis, Ferraz & Finan (2018). The paper gives "8-13%" while the evidence row gives 7.9% (12.7% with multiple audits).')
R('dreze2015', 'other', 'misc', 'false', pats=[r'Dreze & Khera 2015'], md=[r'Dr[èe]ze & Khera'],
  author='Drèze, J. and Khera, R.', title='[Article on PDS leakage estimates]', howpublished='Economic and Political Weekly', year='2015',
  note='Figures read via Table 1 in ideasforindia2025pds',
  prob='EPW article title, volume and pages not recorded in project files (only "Dreze & Khera 2015 EPW"); official title not recorded.')
R('ideasforindia_pds', 'other', 'misc', 'url', pats=[r'declining-pds-leakages'], md=[r'PDS'],
  title='Declining PDS leakages: A look at the numbers', howpublished='Ideas for India',
  url='https://www.ideasforindia.in/topics/poverty-inequality/declining-pds-leakages-a-look-at-the-numbers.html', urldate='2026-11-03', vtok='Declining PDS',
  prob=['Ideas for India article: author(s) and year not recorded in project files.',
        'Underlying studies Khera 2024b, Das et al. 2024 and Puri & Pingali 2025 (v69 row 21) are cited only via this article; no full references.'])
R('eca2024inbrief', 'report', 'techreport', 'url', pats=[r'European Court of Auditors', r'audit-in-brief-2023', r'^ECA\|'], md=[r'European Court of Auditors', r'\bECA\b'],
  author='{European Court of Auditors}', title='2023 EU audit in brief', institution='European Court of Auditors',
  url='https://op.europa.eu/webpub/eca/audit-in-brief-2023/en/', urldate='2026-11-03', vtok='audit in brief',
  prob='Publication year not recorded (covers the 2023 EU budget).')
R('ti2006gcr', 'report', 'book', 'url', pats=[r'TI Global Corruption Report 2006'], md=[],
  author='{Transparency International}', title='Global Corruption Report 2006: Corruption and Health', publisher='Transparency International', year='2006',
  url='https://www.transparency.org/en/publications/global-corruption-report-2006-corruption-and-health', urldate='2026-11-03', vtok='Global Corruption Report 2006',
  prob='No figure taken (row marked n/a, unverified).')
R('globalfund2024recoveries', 'report', 'techreport', 'false', pats=[r'Global Fund Recoveries'], md=[],
  author='{The Global Fund}', title='Recoveries report as of 31 December 2024 (Board document BM53-14)', institution='The Global Fund',
  url='https://archive.theglobalfund.org/media/gbpcqrog/archive_bm53-14-recoveries-31-december-2024_report_en.pdf', urldate='2026-11-03',
  prob='No figure taken (row n/a, unverified); publication year not recorded.')
R('chen2019bpea', A, 'article', 'doi', pats=[r'Chen, Chen, Hsieh', r'Chen et al\. 2019 BPEA'], md=[r'Chen et al\.? 2019', r'1\.7 percentage points'], doi='10.1353/eca.2019.0001')
R('caixin2017liaoning', 'other', 'misc', 'url', pats=[r'caixinglobal\.com/2017-01-18'], md=[r'Liaoning'],
  author='{Caixin Global}', title='Liaoning Government Admits False Growth Data from 2011-14', year='2017',
  url='https://www.caixinglobal.com/2017-01-18/liaoning-government-admits-false-growth-data-from-2011-14-101046468.html', urldate='2026-11-03', vtok='Liaoning')
R('bofit2017', 'other', 'misc', 'url', pats=[r'BOFIT'], md=[r'BOFIT'],
  author='{BOFIT (Bank of Finland Institute for Emerging Economies)}', title='Officials reveal falsification of statistical reporting in two Chinese provinces', howpublished='BOFIT Weekly Review 24/2017', year='2017',
  url='https://www.bofit.fi/en/monitoring/weekly/2017/vw201724_4/', urldate='2026-11-03', vtok='falsification')
R('monasterio_ipea1818', 'report', 'techreport', 'url', pats=[r'Monasterio'], md=[r'Monasterio'],
  author='Monasterio, Leonardo', title='O FPM e a Estranha Distribuição da População dos Pequenos Municípios Brasileiros', institution='IPEA', type='Texto para Discussão', number='1818',
  url='https://ideas.repec.org/p/ipe/ipetds/1818.html', urldate='2026-11-03', vtok='FPM',
  prob='Year of IPEA TD 1818 and author given name not recorded in project files.')
R('rbe_fpm', A, 'misc', 'url', pats=[r'Elasticity of population', r'scielo\.br/j/rbe'], md=[],
  title='Elasticity of population (mis)reporting in Brazilian municipalities: A census tale', howpublished='Revista Brasileira de Economia',
  url='https://www.scielo.br/j/rbe/a/Js8zBWXCLTtxcYH5z7CPQkn/?lang=en', urldate='2026-11-03', vtok='Elasticity of population',
  prob='Authors, year, volume, pages and DOI not recorded in project files.')
R('weitzman1980', A, 'article', 'doi', pats=[r'Weitzman'], md=[r'Weitzman'], doi='10.2307/3003414',
  prob='Cited as theory only (no figure taken; row unverified in v69).')
R('berliner1957', 'book', 'book', 'false', pats=[r'Berliner 1957'], md=[r'Berliner'],
  author='Berliner, Joseph S.', title='Factory and Manager in the USSR', publisher='Harvard University Press', year='1957', address='Cambridge, MA', ver2=True,
  prob='Cited only as background ("Berliner 1957") in v69; no page or claim; bibliographic details confirmed here via Open Library.')
R('banerjee2020', A, 'article', 'doi', pats=[r'Banerjee, Duflo'], md=[r'Bihar', r'19[–-]24 ?%'], doi='10.1257/app.20180302')
R('muralidharan2016', A, 'article', 'doi', pats=[r'Muralidharan'], md=[r'Muralidharan', r'Smartcards'], doi='10.1257/aer.20141346',
  note='Working-paper version: NBER WP 19999')
R('bjorkman2009', A, 'article', 'doi', pats=[r'Bjorkman'], md=[r'Bj[öo]rkman'], doi='10.1162/qjec.2009.124.2.735')
R('donato3ie', 'report', 'techreport', 'false', pats=[r'3ie replication plan'], md=[],
  author='Donato', title='[Revised replication plan for Björkman and Svensson (2009)]', institution='International Initiative for Impact Evaluation (3ie)', year='2018',
  url='https://3ieimpact.org/sites/default/files/2018-12/donato_revised_replication_plan.pdf', urldate='2026-11-03',
  prob='Author given name and exact title of the 3ie replication plan are not recorded (only "Donato").')
R('lewisfaupel2016', A, 'article', 'doi', pats=[r'Lewis-Faupel'], md=[r'Lewis-Faupel'], doi='10.1257/pol.20140258',
  note='Working-paper version: NBER WP 20344')
R('stripes2021covax', 'other', 'misc', 'url', pats=[r'stripes\.com/covid'], md=[r'COVAX'],
  author='{Stars and Stripes / Associated Press}', title="Covax promised 2 billion vaccine doses to help the world's neediest in 2021. It won't deliver even half that.", year='2021',
  url='https://www.stripes.com/covid/2021-12-11/covax-delivers-well-below-promised-2billion-vaccine-doses-3936003.html', urldate='2026-11-03', vtok='Covax')
R('soares2007ipc', 'report', 'techreport', 'false', pats=[r'Soares, Ribas'], md=[r'Bolsa Fam'],
  author='Soares and Ribas and Osório', title='[Evaluation of Bolsa Família targeting, IPC Evaluation Note 1]', institution='International Poverty Centre (UNDP/IPEA)', type='IPC Evaluation Note', number='1',
  url='https://repositorio.ipea.gov.br/bitstream/11058/15288/1/en_IPCEvaluationNote1.pdf', urldate='2026-11-03',
  prob='Title, year and full author names of IPC Evaluation Note 1 not recorded in project files (only surnames).')

# ---------------- Housing / construction (v66/construction, v70) ----------------
R('globalabc2026gsr', 'report', 'techreport', 'doi', pats=[r'Global Status Report for Buildings and Construction 2025', r'GSR 2025-2026', r'mUPr9hKVkn', r'global-status-report-buildings-and-construction-2025'],
  md=[r'GSR 2025', r'Global Status Report', r'3\.4 bn m', r'GlobalABC'],
  doi='10.59117/20.500.11822/49531', author='{United Nations Environment Programme} and {Global Alliance for Buildings and Construction}',
  title='Building fast. Falling short. As climate risks rise and cities grow, we must rethink how we build to create better lives for all -- Global Status Report for Buildings and Construction 2025/26',
  institution='United Nations Environment Programme', year='2026',
  url='https://build-up.ec.europa.eu/system/files/2026-06/mUPr9hKVkn_15_06_2026_152610.pdf', urldate='2026-11-03',
  prob=['v66/construction/evidence.csv took GSR figures from press (Jamaica Gleaner, Anadolu) because the primary PDF returned 403; v68 later read the report via a BUILD UP mirror. The 77% residential share is from a search snippet only.',
        'The 3.4 bn m2/yr is a NET stock increase (v68 item 6), but early v66/v67 text calls it "today\'s world rate" of building -- wording should say net increase.'])
R('gleaner2026', 'other', 'misc', 'url', pats=[r'jamaica-gleaner'], md=[],
  author='{The Gleaner}', title='Earth Today: Construction boom threatens climate goals', year='2026',
  url='https://jamaica-gleaner.com/article/news/20260521/earth-today-construction-boom-threatens-climate-goals', urldate='2026-11-03', note='21 May 2026', vtok='Earth Today',
  prob='Exact headline taken from the URL slug; page title shows only "Earth Today".')
R('aa2026construction', 'other', 'misc', 'false', pats=[r'aa\.com\.tr', r'Anadolu Agency'], md=[],
  author='{Anadolu Agency}', title='Global construction boom outpacing climate gains in building sector, report warns', year='2026',
  url='https://www.aa.com.tr/en/greenline/climate-change/global-construction-boom-outpacing-climate-gains-in-building-sector-report-warns/1830385', urldate='2026-11-03',
  prob='Headline taken from the URL slug (page title only "Greenline").')
R('globalabc2017gsr', 'report', 'techreport', 'false', pats=[r'GSR 2017', r'global-status-report-2018'], md=[],
  author='{United Nations Environment Programme}', title='Global Status Report 2017 [buildings and construction]', institution='UNEP', year='2017',
  url='https://www.unep.org/resources/report/global-status-report-2018', urldate='2026-11-03',
  prob=['Value (230 bn m2 additions to 2056) from a search snippet only (unverified).', 'Edition mismatch: cited as "GSR 2017" but the URL points to the 2018 report page.'])
R('rt2024', 'other', 'misc', 'url', pats=[r'rt\.fi/en', r'RT \(Confederation', r'^RT 2024'], md=[r'Finland precast', r'RT 2024'],
  author='{Rakennusteollisuus RT (Confederation of Finnish Construction Industries)}', title='A new way to measure the productivity of the construction value chain shows the time spent on work', year='2024',
  url='https://rt.fi/en/tiedotteet-ja-uutiset/2024/09/uusi-tapa-mitata-rakentamisen-arvoketjun-tuottavuutta-kertoo-tyohon-kaytetyn-ajan/', urldate='2026-11-03', vtok='productivity of the construction')
R('heeren2019', A, 'article', 'doi', pats=[r'Heeren & Fishman'], md=[r'Heeren'], doi='10.1038/s41597-019-0021-x',
  note='Data: https://github.com/nheeren/material_intensity_db (data/buildings.csv); medians computed in the project')
R('leden2022', 'report', 'techreport', 'doi', pats=[r'Le Den'], md=[r'KU Leuven', r'Ramboll'], doi='10.5281/zenodo.6397514',
  institution='Ramboll; Aalborg University (BUILD); KU Leuven', year='2022',
  url='https://vbn.aau.dk/ws/files/518613236/Towards_embodied_carbon_benchmarks_for_buildings_in_Europe.pdf', urldate='2026-11-03')
R('bpie2022', 'other', 'misc', 'url', pats=[r'bpie\.eu'], md=[],
  author='{BPIE (Buildings Performance Institute Europe)}', title="New report sets out a framework for benchmarking and limiting buildings' embodied carbon",
  url='https://www.bpie.eu/?p=5768', urldate='2026-11-03', vtok='embodied carbon',
  prob='Year of the BPIE news item not recorded.')
R('deetman2020', A, 'article', 'doi', pats=[r'Deetman et al\. 2020'], md=[r'Deetman'], doi='10.1016/j.jclepro.2019.118658',
  prob='Cited in project files only as "Deetman et al. 2020" (BUMA README in v66/data/raw); the README confirms this DOI. The README also cites a companion paper on residential buildings (Marinova, Deetman, van der Voet & Daioglou 2020, J. Cleaner Production, doi:10.1016/j.jclepro.2019.119146), which may be the more precise source for the residential floor-space inputs -- consider citing it.')
R('wbcsd2021', 'report', 'techreport', 'false', pats=[r'WBCSD'], md=[r'WBCSD', r'Arup'],
  author='{World Business Council for Sustainable Development} and {Arup}', title='Net-zero buildings: Where do we stand?', institution='WBCSD', year='2021',
  url='https://archive.wbcsd.org/contentwbc/download/12446/185553/1', urldate='2026-11-03')
R('asman2020', A, 'article', 'doi', pats=[r'Asman'], md=[r'Asman', r'Malaysia'], doi='10.1088/1755-1315/476/1/012086',
  note='Repository copy: https://eprints.ums.edu.my/id/eprint/26510')
R('telloayala2023', A, 'article', 'doi', pats=[r'Tello-Ayala'], md=[r'Tello-Ayala', r'bahareque'], doi='10.3389/fbuil.2023.1150826')
R('escamilla2018', 'other', 'misc', 'false', pats=[r'Escamilla'], md=[r'Escamilla'],
  author='Escamilla and others', title='[LCA of bamboo vs concrete/brick buildings, cited via Tello-Ayala et al. 2023]', year='2018', note='Cited second-hand',
  prob='Incomplete: Escamilla et al. 2018 cited only via Tello-Ayala et al. 2023; title/venue not recorded; no first names or venue.')
R('rincon2023', A, 'article', 'doi', pats=[r'MDPI Sustainability 15\(24\)'], md=[r'MDPI 2023', r'Guadua'], doi='10.3390/su152416893',
  prob='Project cites "MDPI Sustainability 15(24):16893" without authors; DOI record gives Rincón, Montoya & Archila (2023). Values (~107 vs ~298 kgCO2e/m2) came from a search snippet only (403).')
R('saint2023', A, 'article', 'doi', pats=[r'Saint et al'], md=[r'Saint 2023', r'sandbag'], doi='10.1007/s11367-023-02170-0',
  prob='Paywalled; 189/174 kgCO2e/m2 values from a snippet only (unverified).')
R('tno2025', 'report', 'techreport', 'false', pats=[r'TNO 2025', r'TNO-2025-R10710'], md=[r'TNO'],
  author='{TNO}', title='Climate change impact and cost of Compressed Earth Blocks in Kenya (report TNO 2025 R10710)', institution='TNO', year='2025', number='TNO 2025 R10710',
  url='https://publications.tno.nl/publication/34644101/2WOD2kmS/TNO-2025-R10710.pdf', urldate='2026-11-03', prob='Individual authors not recorded.')
R('maxfordham2021', 'report', 'techreport', 'false', pats=[r'Max Fordham'], md=[r'Max Fordham', r'Nepal'],
  author='{Max Fordham}', title='Carbon evaluation of compressed stabilised earth blocks (CSEB) in Nepal: summary (for Build up Nepal)', institution='Max Fordham LLP', year='2021',
  url='https://www.buildupnepal.com/wp-content/uploads/2022/08/carbon-evaluation-of-compressed-stabilised-earth-blocks-cseb-in-nepal-summary.pdf', urldate='2026-11-03')
R('dormohamadi', 'other', 'misc', 'false', pats=[r'Dormohamadi'], md=[],
  author='Dormohamadi and others', title='[Iranian fired-brick LCA cited via TNO 2025]', note='Cited second-hand',
  prob='Incomplete: Dormohamadi et al. cited only via TNO 2025 R10710; no year/title/venue.')
R('leti2020', 'report', 'misc', 'false', pats=[r'LETI 2020'], md=[r'LETI'],
  author='{LETI (London Energy Transformation Initiative)}', title='[LETI embodied carbon targets, cited via Tello-Ayala et al. 2023]', year='2020', prob='Incomplete: LETI 2020 cited only via Tello-Ayala et al. 2023.')
R('riba2019', 'report', 'misc', 'false', pats=[r'RIBA 2019'], md=[r'RIBA'],
  author='{Royal Institute of British Architects}', title='[RIBA 2030 Climate Challenge targets, cited via Tello-Ayala et al. 2023]', year='2019', prob='Incomplete: RIBA 2019 cited only via Tello-Ayala et al. 2023.')
R('unep2023materials', 'report', 'techreport', 'doi', pats=[r'Building Materials and the Climate', r'UNEP 2023 \(via Designing'], md=[r'UNEP 2023', r'UNEP \(2023\)', r'50[–-]75 ?%'],
  doi='10.59117/20.500.11822/43293', author='{United Nations Environment Programme} and {Yale Center for Ecosystems + Architecture}',
  title='Building Materials and the Climate: Constructing a New Future', institution='United Nations Environment Programme', year='2023',
  prob='Read only via a Designing Buildings wiki summary (UNEP PDF 403). DOI record title reads "Building Material and the Climate" (singular).')
R('designingbuildings_unep', 'other', 'misc', 'url', pats=[r'designingbuildings'], md=[],
  author='{Designing Buildings Wiki}', title='UNEP report on building materials and the climate', url='https://www.designingbuildings.co.uk/wiki/UNEP_report_on_building_materials_and_the_climate', urldate='2026-11-03', vtok='UNEP report')
R('istructe2023', A, 'misc', 'false', pats=[r'IStructE'], md=[],
  title='Renovation not demolition: saving carbon (private residence case study)', howpublished='The Structural Engineer, 101(2)', year='2023',
  url='https://www.istructe.org/journal/volumes/volume-101-(2023)/issue-2/renovation-not-demolition-saving-carbon-private/', urldate='2026-11-03',
  prob='Authors and pages not recorded; page blocked (403); 111 vs 199 kgCO2e/m2 from a snippet only.')
R('gertler2025', 'report', 'techreport', 'doi', pats=[r'Gertler'], md=[r'NBER 34560', r'[Ss]lum (upgrading|renewal)', r'in-situ'], doi='10.3386/w34560', institution='National Bureau of Economic Research', type='NBER Working Paper', number='34560',
  url='https://www.nber.org/papers/w34560', urldate='2026-11-03')
R('unhabitat2020', 'report', 'misc', 'false', pats=[r'UN-Habitat 2020'], md=[],
  author='{UN-Habitat}', title='[UN-Habitat 2020 report on slum population, cited via NBER conference slides]', year='2020',
  url='https://conference.nber.org/conf_papers/f226003/f226003.slides.pdf', urldate='2026-11-03',
  prob='Incomplete: UN-Habitat 2020 source cited only via NBER conference slides (snippet, unverified); no title.')
R('csep_housing', 'other', 'misc', 'url', pats=[r'CSEP'], md=[r'CSEP'],
  author='{Centre for Social and Economic Progress (CSEP)}', title="India's housing paradox: Empty houses and housing shortages (policy brief)",
  url='https://csep.org/policy-brief/indias-housing-paradox-empty-houses-and-housing-shortages/', urldate='2026-11-03', vtok='housing paradox',
  prob='CSEP policy brief: author(s) and year not recorded.')
R('gan2019', 'report', 'techreport', 'doi', pats=[r'Gan Li et al'], md=[r'21\.4 ?%'], doi='10.3386/w26585', institution='National Bureau of Economic Research', type='NBER Working Paper', number='26585',
  url='https://www.nber.org/papers/w26585.pdf', urldate='2026-11-03',
  prob='Project cites "Gan Li et al., NBER WP 26585" without title; DOI record: Gan, He, Si & Yi (2019) "Relocating or Redefined: A New Perspective on Urbanization in China".')
R('caixin2018vacancy', 'other', 'misc', 'url', pats=[r'caixinglobal\.com/2018-11-09'], md=[],
  author='{Caixin Global}', title="A Fifth of China's Housing Is Empty. That's 50 Million Homes", year='2018',
  url='https://www.caixinglobal.com/2018-11-09/a-fifth-of-chinas-housing-is-empty-thats-50-million-homes-101344928.html', urldate='2026-11-03', vtok='Fifth of China')
R('portugalnews2022', 'other', 'misc', 'url', pats=[r'theportugalnews'], md=[],
  author='{The Portugal News}', title='12% of homes vacant in Portugal', year='2022',
  url='https://theportugalnews.com/news/2022-12-26/12-of-homes-vacant-in-portugal/73270', urldate='2026-11-03', vtok='Portugal News',
  prob='Snippet only (unverified); original Pordata source not cited.')
R('potter2014', 'report', 'misc', 'false', pats=[r'Potter, Two Million Houses'], md=[r'Korea,? 1990', r'Two Million'],
  author='Potter', title='Two Million Houses (paper presented at RC21 conference 2014)', year='2014',
  url='https://www.rc21.org/en/wp-content/uploads/2014/12/F1-Potter.pdf', urldate='2026-11-03',
  prob=['Author given name and exact paper title not recorded ("Potter, Two Million Houses (RC21 2014)").', 'Underlying source Kang et al. 1999 cited only via Potter.'])
R('kang1999', 'other', 'misc', 'false', pats=[r'Kang et al\. 1999'], md=[], author='Kang and others', title='[Korean housing statistics, cited via Potter 2014]', year='1999',
  prob='Incomplete: Kang et al. 1999 cited only via Potter (RC21 2014).')
R('fernando_bri', 'other', 'misc', 'false', pats=[r'Sri Lanka BRI'], md=[],
  author='Fernando', title='[Sri Lanka Building Research Institute table on owner-driven reconstruction labour]',
  url='https://dl-iesl.nsf.gov.lk/bitstreams/5ed76fca-82ba-4de5-9f0d-40900d08c702/download', urldate='2026-11-03',
  prob=['Incomplete and unreadable: Sri Lanka BRI (Fernando) table could not be read; Manjia et al. 2011 (Cameroon task norms) not fetched. No value used.'])

# ---------------- Consumption / security (v71) ----------------
R('ericsson2017', 'other', 'misc', 'false', pats=[r'Ericsson Mobility Report'], md=[r'Ericsson'],
  author='{Ericsson}', title='Shifting mobile data consumption with data plans (Ericsson Mobility Report article)', year='2017',
  url='https://www.ericsson.com/en/reports-and-papers/mobility-report/articles/shifting-mobile-data-consumption-data-plans', urldate='2026-11-03')
R('lambrecht2006', A, 'article', 'doi', pats=[r'Lambrecht'], md=[r'Lambrecht'], doi='10.1509/jmkr.43.2.212')
R('vieira2026', A, 'article', 'doi', pats=[r'ajae\.70040', r'Lopez Barrera'], md=[r'inverted U'], doi='10.1002/ajae.70040',
  prob=['Author order differs: project cites "Lopez Barrera, Vieira & Ferreira"; DOI record lists Vieira, Lopez Barrera & Dias Paes Ferreira. Read only via a Texas A&M press release.',
        'Volume/pages not yet assigned in the DOI record (early view).'])
R('tamu2026foodwaste', 'other', 'misc', 'false', pats=[r'stories\.tamu\.edu'], md=[],
  author='{Texas A\\&M AgriLife}', title='Texas A\\&M AgriLife study reveals why food waste rises, falls as incomes grow (press release)', year='2026',
  url='https://stories.tamu.edu/news/2026/04/30/texas-am-agrilife-study-reveals-why-food-waste-rises-falls-as-incomes-grow/', urldate='2026-11-03')
R('wrap2020lockdown', 'report', 'techreport', 'url', pats=[r'WRAP'], md=[r'WRAP', r'lockdown'],
  author='{WRAP}', title='Citizens and food during lockdown', institution='WRAP', year='2020',
  url='https://www.wrap.ngo/resources/report/citizens-and-food-during-lockdown', urldate='2026-11-03', vtok='Citizens and food')
R('adworld2020nielsen', 'other', 'misc', 'url', pats=[r'adworld\.ie', r'Nielsen via'], md=[r'181 ?%', r'Ireland grocery'],
  author='{Adworld.ie}', title='Panic Buying Triggers 23% Growth in Retail Sales Says Nielsen', year='2020',
  url='https://www.adworld.ie/2020/03/27/panic-buying-triggers-23-growth-in-retail-sales-says-nielsen/', urldate='2026-11-03', vtok='Panic Buying')
R('shah2012', A, 'article', 'doi', pats=[r'Shah, Mullainathan'], md=[r'Mullainathan'], doi='10.1126/science.1222426')
R('nettle2017', A, 'article', 'doi', pats=[r'Nettle'], md=[r'Nettle'], doi='10.1017/S0140525X16000947')
R('deaton2009', A, 'article', 'false', pats=[r'Deaton & Dreze'], md=[r'Deaton'],
  author='Deaton, A. and Drèze, J.', title='Nutrition in India: Facts and Interpretations', journal='Economic and Political Weekly', volume='44', number='7', pages='42--65', year='2009',
  url='https://econpapers.repec.org/paper/cdecdewps/170.htm', urldate='2026-11-03',
  prob=['Title not recorded in project files (only "EPW 44(7):42-65"); the URL points to CDE working paper 170 titled "Nutrition in India: Facts and Interpretations" (title used here); the EPW article title was not checked.',
        'v71 row 18 marked unverified (calorie figures from search snippet).'])
R('hall2019', A, 'article', 'doi', pats=[r'Hall et al\. 2019'], md=[r'Hall 2019', r'ultra-processed'], doi='10.1016/j.cmet.2019.05.008')
R('haushofer2016', A, 'article', 'doi', pats=[r'Haushofer'], md=[r'Haushofer', r'GiveDirectly'], doi='10.1093/qje/qjw025')
R('evans2017', A, 'article', 'doi', pats=[r'Evans & Popova'], md=[r'Evans & Popova', r'temptation goods'], doi='10.1086/689575',
  prob='Pooled effect -0.18 SD is "search-only" (unverified) in v71 row 21.')
R('sorrell2009', A, 'article', 'doi', pats=[r'Sorrell'], md=[r'Sorrell'], doi='10.1016/j.enpol.2008.11.026')
R('itf2016rebound', 'report', 'misc', 'false', pats=[r'OECD/ITF 2016'], md=[],
  author='{OECD International Transport Forum}', title='[Meta-analysis of road-transport direct rebound, 2016]', year='2016',
  url='https://search.ub.tum.de/vufind/Record/DE-604.BV047934003', urldate='2026-11-03',
  prob='Incomplete: OECD/ITF 2016 meta-analysis has no title/authors in project files; 12%/32% values search-only (unverified).')
R('gibraltar2018eed', 'report', 'techreport', 'false', pats=[r'Gibraltar'], md=[r'flat-rate heating', r'30 ?% more than metered'],
  author='{HM Government of Gibraltar}', title='Implementing Article 9(3) of the Energy Efficiency Directive: guidance note', institution='HM Government of Gibraltar', year='2018',
  url='https://www.gibraltar.gov.gi/new/sites/default/files/HMGoG_Documents/20180501-Implementing_Article_9-3_EED_GuidanceNote.pdf', urldate='2026-11-03',
  prob='Secondary source (Gibraltar government guidance citing unnamed EU studies) for the "about 30%" metering saving used in Article 21; primary EU study not cited.')
R('cats2017', A, 'article', 'doi', pats=[r'Cats, Susilo'], md=[r'Tallinn'], doi='10.1007/s11116-016-9695-5')
R('connexion_dunkirk', 'other', 'misc', 'url', pats=[r'connexionfrance'], md=[r'Dunkirk'],
  author='{The Connexion}', title='Free buses prove successful in French town of Dunkirk',
  url='https://connexionfrance.com/news/free-buses-prove-successful-in-french-town-of-dunkirk/426645', urldate='2026-11-03', vtok='Dunkirk',
  prob='Year of the Connexion article not recorded; underlying VIGS evaluation not cited directly.')

# ---------------- Transition history (v72) ----------------
for k, slug, t in [('wiki_eastgermanmark', 'East_German_mark', 'East German mark'), ('wiki_treuhand', 'Treuhandanstalt', 'Treuhandanstalt'),
                   ('wiki_euenlargement', 'Enlargement_of_the_European_Union', 'Enlargement of the European Union'),
                   ('wiki_isf', 'Solidarity_tax_on_wealth', 'Solidarity tax on wealth'),
                   ('wiki_policelist', 'List_of_countries_and_dependencies_by_number_of_police_officers', 'List of countries and dependencies by number of police officers'),
                   ('wiki_costarica_art12', 'Article_12_of_the_Constitution_of_Costa_Rica', 'Article 12 of the Constitution of Costa Rica'),
                   ('wiki_panama', 'Panamanian_Public_Forces', 'Panamanian Public Forces'),
                   ('wiki_iceland_military', 'Military_of_Iceland', 'Defence of Iceland')]:
    R(k, 'other', 'misc', 'url', pats=[r'wikipedia\.org/wiki/' + slug + r'\b'], md=[],
      author='{Wikipedia contributors}', title=t, howpublished='Wikipedia, The Free Encyclopedia',
      url='https://en.wikipedia.org/wiki/' + slug, urldate='2026-11-03', vtok=t,
      prob='Wikipedia is a tertiary source: replace with the primary source it cites before publication.')
R('wiki_iceland_military', extend=True, prob='URL Military_of_Iceland now redirects to "Defence of Iceland".')
R('brainard1991', A, 'article', 'doi', pats=[r'Brookings Papers on Economic Activity 1:1991', r'BPEA 1:1991'], md=[r'BPEA 1991', r'half the 1989 level', r'8 ?% of workers'],
  doi='10.2307/2534637', url='https://www.brookings.edu/wp-content/uploads/1991/01/1991a_bpea_editors_summary.pdf', urldate='2026-11-03',
  note="Editors' summary of Akerlof, Rose, Yellen and Hessenius, East Germany in from the cold, in the same issue",
  prob='The underlying paper (Akerlof, Rose, Yellen & Hessenius 1991, BPEA 1991(1)) is not itself cited; only the editors\' summary was read.')
R('iab1998topics29', 'report', 'techreport', 'false', pats=[r'IAB Topics 29'], md=[r'IAB'],
  author='{Institut für Arbeitsmarkt- und Berufsforschung (IAB)}', title='IAB Topics No. 29', institution='IAB', year='1998', number='29',
  url='https://doku.iab.de/topics/1998/topics29.pdf', urldate='2026-11-03', prob='Title and authors of IAB Topics 29 not recorded in project files.')
R('ghdi_treuhand', 'other', 'misc', 'url', pats=[r'closing-the-treuhandanstalt'], md=[r'256 ?bn', r'256\.4'],
  author='{German History in Documents and Images}', title='Closing the Treuhandanstalt [Trusteeship Agency] (December 30, 1994)',
  url='https://germanhistorydocs.org/en/a-new-germany-1990-2023/closing-the-treuhandanstalt-trusteeship-agency-december-30-1994', urldate='2026-11-03', vtok='Treuhandanstalt')
R('ghdi_property', 'other', 'misc', 'url', pats=[r'unification-and-property-issues'], md=[r'restitution before compensation'],
  author='{German History in Documents and Images}', title='Unification and Property Issues (June 15, 1990)',
  url='https://germanhistorydocs.org/en/a-new-germany-1990-2023/unification-and-property-issues-june-15-1990', urldate='2026-11-03', vtok='Property Issues')
R('foothill_restitution', 'other', 'misc', 'false', pats=[r'foothill\.edu'], md=[],
  author='{Foothill College}', title='German unification study: restitution', url='https://foothill.edu/german-unification-study/restitution.html', urldate='2026-11-03',
  prob='URL now returns 404; figure (over 1 million claims) from a search snippet only.')
R('ec2006com48', 'report', 'misc', 'false', pats=[r'COM\(2006\)48'], md=[],
  author='{European Commission}', title='Communication COM(2006) 48 [on transitional arrangements for free movement of workers after the 2004 enlargement]', year='2006',
  url='https://ecer.minbuza.nl/nl/-/8-februari-vragen-en-antwoorden-over-vrij-werknemersverkeer-met-de-tien-nieuwe-lidstaten', urldate='2026-11-03',
  prob='COM(2006)48 read only via search snippets and a Dutch government Q&A page; official title not recorded.')
R('ec2024panorama', 'report', 'misc', 'url', pats=[r'Panorama 2024'], md=[r'0\.4 ?% of national GDP'],
  author='{European Commission, DG REGIO}', title='Enlargement 2004: cohesion policy 20 years later (Panorama)', year='2024',
  url='https://ec.europa.eu/regional_policy/whats-new/panorama/2024/05/05-08-2024-enlargement-2004-cohesion-policy-20-years-later_en', urldate='2026-11-03', vtok='Panorama')
R('paih_poland80', 'other', 'misc', 'url', pats=[r'trade\.gov\.pl'], md=[r'51 ?% ?(→|->)'],
  author='{Polish Investment \\& Trade Agency}', title="Poland's GDP is already 80% of the EU average",
  url='https://www.trade.gov.pl/en/news/polands-gdp-is-already-80-of-the-eu-average', urldate='2026-11-03', vtok='80%',
  prob='Poland convergence figures differ by source: ~51% of EU average at accession (trade.gov.pl) vs 44% in 1995 and 81% in 2025 (Notes from Poland); WP §11 combines them as "51% -> 81%" (different sources and years).')
R('notesfrompoland2026', 'other', 'misc', 'url', pats=[r'notesfrompoland'], md=[],
  author='{Notes from Poland}', title="Poland's wealth gap to EU average narrows to record low level", year='2026',
  url='https://notesfrompoland.com/2026/03/26/polands-wealth-gap-to-eu-average-narrows-to-record-low-level/', urldate='2026-11-03', vtok='wealth gap')
R('pie2019cohesion', 'report', 'techreport', 'false', pats=[r'PIE Cohesion', r'Polish Economic Institute'], md=[r'PIE 2019', r'1\.9[–-]4\.0 ?%'],
  author='{Polish Economic Institute}', title='Cohesion report (Raport Spójność / Cohesion)', institution='Polish Economic Institute', year='2019',
  url='https://pie.net.pl/wp-content/uploads/2019/09/PIE-Raport_Cohesion-Spojnosc-EN-red..pdf', urldate='2026-11-03',
  prob=['Exact report title not recorded.', 'Underlying source Piketty (2018) is cited only via PIE 2019; no full reference.'])
R('baltictimes_cohesion', 'other', 'misc', 'false', pats=[r'Baltic Times'], md=[],
  author='{The Baltic Times}', title='[Article on cohesion-fund caps]', url='https://www.baltictimes.com/news/articles/29817', urldate='2026-11-03',
  prob='Title/year not recorded; page blocked; snippet only (unverified).')
R('ecb2007mb', 'report', 'techreport', 'false', pats=[r'ECB Monthly Bulletin'], md=[r'ECB'],
  author='{European Central Bank}', title='Monthly Bulletin, May 2007, pp. 63--72 (article/box on the euro cash changeover and inflation)', institution='ECB', year='2007', pages='63--72',
  url='https://www.ecb.europa.eu/pub/pdf/other/pp63-72_mb200705en.pdf', urldate='2026-11-03', prob='Article title within the Monthly Bulletin not recorded.')
R('bdp2002', 'report', 'techreport', 'false', pats=[r'Banco de Portugal'], md=[],
  author='{Banco de Portugal}', title='Economic Bulletin 2002 (article on the euro changeover and prices)', institution='Banco de Portugal', year='2002',
  url='https://www.bportugal.pt/sites/default/files/anexos/papers/ab200208_e.pdf', urldate='2026-11-03', prob='Article title and authors not recorded.')
R('nbs2007biatec', 'report', 'misc', 'false', pats=[r'BIATEC'], md=[],
  author='{Národná banka Slovenska}', title='BIATEC 2007, issue 5 (article on euro changeover and perceived inflation)', year='2007',
  url='https://nbs.sk/_img/Documents/BIATEC/BIA07_05/2_7.pdf', urldate='2026-11-03', prob='Article title and authors not recorded.')
R('imf2019hipc', 'report', 'techreport', 'false', pats=[r'HIPC and MDRI Statistical Update', r'IMF Statistical Update 2019', r'ppea2019028'], md=[r'HIPC', r'76 bn', r'7\.3 ?% vs 1\.9'],
  author='{International Monetary Fund}', title='Heavily Indebted Poor Countries (HIPC) Initiative and Multilateral Debt Relief Initiative (MDRI) -- Statistical Update', institution='IMF', year='2019',
  url='https://www.imf.org/-/media/files/publications/pp/2019/ppea2019028.pdf', urldate='2026-11-03',
  prob='IMF site now returns 403; recorded URL ends in ".pdf.md" (a converted copy).')
R('imf2023hipcfactsheet', 'other', 'misc', 'false', pats=[r'IMF HIPC factsheet'], md=[],
  author='{International Monetary Fund}', title='Debt relief under the Heavily Indebted Poor Countries (HIPC) Initiative (factsheet)', year='2023',
  url='https://www.imf.org/en/About/Factsheets/Sheets/2023/Debt-relief-under-the-heavily-indebted-poor-countries-initiative-HIPC', urldate='2026-11-03')
R('cruces2013', A, 'article', 'doi', pats=[r'Cruces & Trebesch'], md=[r'Cruces'], doi='10.1257/mac.5.3.85',
  note='Working-paper version read: CESifo WP 3604 (2011), https://www.cesifo.org/DocDL/cesifo1_wp3604.pdf')
R('vonluckner2024', 'report', 'techreport', 'doi', pats=[r'Graf von Luckner'], md=[r'327 restructurings'], doi='10.3386/w32599', institution='National Bureau of Economic Research', type='NBER Working Paper', number='32599',
  url='https://www.nber.org/papers/w32599', urldate='2026-11-03', prob='~45% average haircut is from a search snippet only (unverified).')
R('ilo1971japan', A, 'article', 'false', pats=[r'International Labour Review 1971', r'09602\(1971'], md=[r'ILO 1971'],
  author='{International Labour Office}', title='[Article on land reform in Japan]', journal='International Labour Review', volume='103', number='4', pages='393--413', year='1971',
  url='https://webapps.ilo.org/public/libdoc/ilo/P/09602/09602(1971-103-4)393-413.pdf', urldate='2026-11-03',
  prob='Author and title of the 1971 International Labour Review article not recorded in project files.')
R('thirdbit2026', 'other', 'misc', 'url', pats=[r'third-bit'], md=[],
  author='{The Third Bit}', title='Land to the Landless (essay)', year='2026', url='https://third-bit.com/2026/05/09/land-reform', urldate='2026-11-03', vtok='Land',
  prob='Non-academic blog essay used for the "~30% of farmland changed hands" figure; replace with a primary source.')
R('narain1964', 'other', 'misc', 'url', pats=[r'Narain'], md=[],
  author='Narain, K. V.', title='Prosperity through free economy: a case study of Taiwan', year='1964', howpublished='Republished by Indian Liberals',
  url='https://indianliberals.in/primary-works/prosperity-through-free-enterprise-a-case-study-of-taiwan-by-kv-narain-november-9-1964/', urldate='2026-11-03', vtok='TAIWAN',
  prob='Title differs: URL slug says "free enterprise", page title says "free economy". Original publication venue not recorded.')
R('kimlee2025', 'report', 'techreport', 'false', pats=[r'Kim & Lee'], md=[r'Kim & Lee'],
  author='Kim and Lee', title='[Working paper on the 1950 South Korean land reform]', institution='Chinese University of Hong Kong, Department of Economics', year='2025',
  url='https://www.econ.cuhk.edu.hk/wp-content/uploads/2025/04/Kim_Lee_Working_Paper_Land_Reform-1.pdf', urldate='2026-11-03',
  prob='Incomplete: authors\' given names and title of the Kim & Lee (2025) working paper not recorded.')
R('hull_formula', 'other', 'misc', 'false', pats=[r'modeldiplomat'], md=[r'Hull'],
  author='{Model Diplomat}', title='Hull Formula -- Definition \\& Meaning (glossary)', url='https://modeldiplomat.com/learn/glossary/hull-formula', urldate='2026-11-03',
  prob='Hull formula (1938) cited via a glossary website/search snippets only; cite the 1938 Hull note or a legal treatise.')
R('unga1803', 'other', 'misc', 'false', pats=[r'libros\.uchile'], md=[r'Res(olution)?\.? 1803'],
  author='{United Nations General Assembly}', title='Resolution 1803 (XVII)', year='1962',
  url='https://libros.uchile.cl/files/presses/1/monographs/287/submission/proof/279/', urldate='2026-11-03',
  prob='UNGA Res 1803 (XVII) cited via a search snippet of an unrelated book page; cite the UN document (A/RES/1803(XVII)) directly.')
R('moneyvox_isf', 'other', 'misc', 'false', pats=[r'moneyvox'], md=[],
  author='{MoneyVox}', title="Impôts : près de 5 000 redevables de l'ISF ont quitté la France en 10 ans", url='https://www.moneyvox.fr/actu/72314/impots-pres-de-5-000-redevables-de-isf-ont-quitte-la-france-en-10-ans', urldate='2026-11-03',
  prob='Snippet only; DGFiP primary source not cited; year not recorded.')
R('swissinfo_norway', 'other', 'misc', 'url', pats=[r'swissinfo'], md=[r'Norway (saw|lost)'],
  author='{SWI swissinfo.ch}', title='Rich Norwegians flee to low-tax Switzerland as wealth levy bites',
  url='https://www.swissinfo.ch/eng/business/rich-norwegians-flee-to-low-tax-switzerland-as-wealth-levy-bites/48140438', urldate='2026-11-03', vtok='Rich Norwegians',
  prob='Year not recorded (article reports 2022 departures, citing Dagens Næringsliv).')
R('brusselsreport2024', 'other', 'misc', 'url', pats=[r'brusselsreport'], md=[],
  author='{Brussels Report}', title="The failure of Norway's wealth tax hike as a warning signal", year='2024',
  url='https://www.brusselsreport.eu/2024/09/11/the-failure-of-norways-wealth-tax-hike-as-a-warning-signal/', urldate='2026-11-03', vtok='Norway',
  prob='Opinion outlet; consider a primary statistical source.')
R('wir2026', 'report', 'techreport', 'false', pats=[r'World Inequality Report 2026', r'WIR 2026'], md=[r'World Inequality Report', r'WIR 2026'],
  author='{World Inequality Lab}', title='World Inequality Report 2026', institution='World Inequality Lab',
  note='Read only via secondary summaries (sharing.org; c4scourses.in)',
  prob=['World Inequality Report 2026: primary report not read (secondary summaries only); editors/authors and publication date not recorded.', 'Top-1% share (~37%) from search snippet only (unverified).'])
R('sharing2026wir', 'other', 'misc', 'url', pats=[r'sharing\.org'], md=[],
  author="{Share The World's Resources}", title='Just 0.001% hold three times the wealth of poorest half of humanity, report finds',
  url='https://sharing.org/information-centre/reports/just-0-001-hold-three-times-the-wealth-of-poorest-half-of-humanity-report-finds/', urldate='2026-11-03', vtok='0.001%',
  prob='Publication year not recorded.')
R('c4s_wir2026', 'other', 'misc', 'false', pats=[r'c4scourses'], md=[],
  author='{C4S Courses}', title='World Inequality Report 2026 (summary)', url='https://c4scourses.in/national-affairs/world-inequality-report-2026/', urldate='2026-11-03',
  prob='Coaching-site summary; not citable in a scientific paper.')
R('iif2026debt', 'other', 'misc', 'url', pats=[r'hurriyetdailynews'], md=[r'64\.6 tn'],
  author='{Hürriyet Daily News}', title='Global debt hits record high of $348 trillion in 2025: Report (on IIF Global Debt Monitor)', year='2026',
  url='https://www.hurriyetdailynews.com/amp/global-debt-hits-record-high-of-348-trillion-in-2025-report-219339', urldate='2026-11-03', vtok='348 trillion',
  prob='IIF Global Debt Monitor read only via press coverage; 308% debt-to-GDP from snippet only.')
R('iceland2014a', 'other', 'misc', 'false', pats=[r'2014-03-26-Debt-Relief'], md=[r'Iceland \(2014\)'],
  author='{Government of Iceland}', title='Debt relief will reach 100,000 households (news, 26 March 2014)', year='2014',
  url='https://www.stjornarradid.is/frettir/grein/2014-03-26-Debt-Relief-Will-Reach-100-000-Households/', urldate='2026-11-03')
R('iceland2014b', 'other', 'misc', 'false', pats=[r'2014-11-10-Improved-equity'], md=[],
  author='{Government of Iceland}', title='Improved equity and debt position of 56,000 households (news, 10 November 2014)', year='2014',
  url='https://www.stjornarradid.is/frettir/grein/2014-11-10-Improved-equity-and-debt-position-of-56-000-households/', urldate='2026-11-03')
R('hungary2015fx', 'other', 'misc', 'url', pats=[r'kormany\.hu'], md=[r'forint'],
  author='{Hungarian Ministry for National Economy}', title='Law on conversion of forex loans and fair banks enters into force (news, 3 February 2015)', year='2015',
  url='https://2015-2019.kormany.hu/en/ministry-for-national-economy/news/law-on-conversion-of-forex-loans-and-fair-banks-enters-into-force', urldate='2026-11-03', vtok='Ministry')
R('bloomberg2015hungary', 'other', 'misc', 'false', pats=[r'bloomberg\.com'], md=[],
  author='{Bloomberg}', title="Hungary's Orban makes world's best trade on Swiss franc loans", year='2015',
  url='https://www.bloomberg.com/news/2015-01-16/hungary-s-orban-makes-world-s-best-trade-on-swiss-franc-loans.html', urldate='2026-11-03',
  prob='Paywalled/blocked; 3.3 tn HUF from snippet only.')
R('unctad2024debt', 'report', 'misc', 'false', pats=[r'UNCTAD'], md=[r'UNCTAD', r'3\.3 billion'],
  author='{UNCTAD}', title='[UNCTAD report: people living in countries spending more on interest than on health or education]',
  prob='Incomplete and unverified: the UNCTAD "3.3 billion people" figure (WP Appendix T6, book Ch. 6 and 15, v72/TRANSITION_RULES.md) has no title, year or URL in project files and is marked REPORTED_NEEDS_RECHECK.')

# ---------------- Peace force (v76) ----------------
R('unpk2025factsheet', 'report', 'misc', 'false', pats=[r'Fact Sheet, 30 September 2025', r'peacekeeping_fact_sheet_september_2025', r'UN Fact Sheet Sep'], md=[r'59,?376', r'59,000 uniformed', r'Fact Sheets? Sep'],
  author='{United Nations Peacekeeping}', title='Peacekeeping fact sheet, 30 September 2025', year='2025',
  url='https://peacekeeping.un.org/sites/default/files/peacekeeping_fact_sheet_september_2025_english.pdf', urldate='2026-11-03')
R('unpk_funding', 'other', 'misc', 'url', pats=[r'how-we-are-funded'], md=[r'USD 5\.6 bn', r'1,?428'],
  author='{United Nations Peacekeeping}', title='How we are funded', url='https://peacekeeping.un.org/en/how-we-are-funded', urldate='2026-11-03', vtok='How we are funded')
R('unpk2015factsheet', 'report', 'misc', 'false', pats=[r'pk_factsheet_03_15', r'Fact Sheet, 31 March 2015'], md=[r'106,?595', r'March 2015'],
  author='{United Nations Peacekeeping}', title='Peacekeeping fact sheet, 31 March 2015', year='2015',
  url='https://minusca.unmissions.org/sites/default/files/pk_factsheet_03_15_e.pdf', urldate='2026-11-03', note='Read from the MINUSCA mission website copy')
R('pew2016peacekeeping', 'other', 'misc', 'url', pats=[r'Pew Research'], md=[r'Pew'],
  author='{Pew Research Center}', title='UN peacekeeping at new highs after post-Cold War surge and decline', year='2016',
  url='https://www.pewresearch.org/short-reads/2016/03/02/un-peacekeeping-at-new-highs-after-post-cold-war-surge-and-decline/', urldate='2026-11-03', vtok='peacekeeping',
  prob='Pew (about 108,000 by April 2015) and the UN fact sheet (106,595 at 31 March 2015) give different "peak" figures; the constitution uses 106,595.')
R('hultman2013', A, 'article', 'doi', pats=[r'Hultman'], md=[r'Hultman', r'reduce violence against civilians'], doi='10.1111/ajps.12036')
R('walter2021', A, 'article', 'doi', pats=[r'Walter, Howard'], md=[r'Walter, Howard'], doi='10.1017/S000712342000023X')
R('hasc2010haiti', 'other', 'misc', 'url', pats=[r'armedservices\.house\.gov'], md=[r'Haiti'],
  author='{House Armed Services Committee}', title='Skelton praises U.S. Armed Forces on Haiti earthquake relief effort (press release)', year='2010',
  url='https://democrats-armedservices.house.gov/2010/2/skelton-praises-u-s--armed-forces-on-haiti-earthquake-relief-effort', urldate='2026-11-03', vtok='Haiti')
R('whitehouse2005tsunami', 'other', 'misc', 'url', pats=[r'georgewbush-whitehouse'], md=[r'tsunami'],
  author='{The White House}', title='U.S. Military Delivers Aid to Tsunami Victims (release, 7 January 2005)', year='2005',
  url='https://georgewbush-whitehouse.archives.gov/news/releases/2005/01/20050107-12.html', urldate='2026-11-03', vtok='Tsunami')
R('insarag2023turkiye', 'other', 'misc', 'url', pats=[r'insarag\.org'], md=[r'T[üu]rkiye'],
  author='{INSARAG}', title='After-Action Review: Türkiye \\& Syria (earthquakes 2023)', url='https://insarag.org/aar-turkiye/', urldate='2026-11-03', vtok='AAR')
R('echo_ucpm', 'other', 'misc', 'url', pats=[r'civil-protection-humanitarian-aid\.ec\.europa\.eu'], md=[r'Civil Protection Mechanism'],
  author='{European Commission, DG ECHO}', title='EU Civil Protection Mechanism', url='https://civil-protection-humanitarian-aid.ec.europa.eu/what/civil-protection/eu-civil-protection-mechanism_en', urldate='2026-11-03', vtok='civil protection')
R('ec_resceu', 'other', 'misc', 'url', pats=[r'union-civil-protection-mechanism-resceu'], md=[r'rescEU'],
  author='{European Commission}', title='Union Civil Protection Mechanism (rescEU) -- EU funding programme', url='https://commission.europa.eu/funding-tenders/find-funding/eu-funding-programmes/union-civil-protection-mechanism-resceu_en', urldate='2026-11-03', vtok='rescEU')
R('alnap2022sohs', 'report', 'techreport', 'false', pats=[r'ALNAP'], md=[r'ALNAP'],
  author='{ALNAP}', title='The State of the Humanitarian System 2022', institution='ALNAP/ODI', year='2022',
  note='Read via Global Policy blog (J. Parker, 4 October 2022): https://www.globalpolicyjournal.com/blog/04/10/2022/humanitarian-system-edge-abyss-where-next',
  prob='ALNAP SOHS 2022 read only via a blog post; report not consulted.')
R('globalpolicy2022', 'other', 'misc', 'url', pats=[r'globalpolicyjournal'], md=[],
  author='Parker, J.', title='The Humanitarian System is on the Edge of the Abyss. Where next?', howpublished='Global Policy (blog)', year='2022',
  url='https://www.globalpolicyjournal.com/blog/04/10/2022/humanitarian-system-edge-abyss-where-next', urldate='2026-11-03', vtok='Humanitarian System')
R('police_minimum_snippets', 'other', 'misc', 'false', pats=[r'BusinessTech / Indian press'], md=[r'222 per'],
  author='{BusinessTech and Indian press}', title='[Press reports of a "UN recommended minimum" of 222 police per 100,000]', urldate='2026-11-03',
  prob='"UN recommended minimum" of 220-222 police per 100,000: no URL and no primary UN source; likely a myth -- do not use.')
R('sipri2026milex', 'report', 'techreport', 'false', pats=[r'SIPRI Fact Sheet', r'2604_milex'], md=[r'SIPRI', r'2,?887', r'2\.5 ?% of world'],
  author='{Stockholm International Peace Research Institute}', title='Trends in World Military Expenditure, 2025 (SIPRI Fact Sheet, April 2026)', institution='SIPRI', year='2026', type='SIPRI Fact Sheet',
  url='https://www.sipri.org/sites/default/files/2026-04/2604_milex_2025.pdf', urldate='2026-11-03',
  prob='SIPRI fact sheets have named authors; they are not recorded in project files.')
R('powell2011', A, 'article', 'doi', pats=[r'Powell & Thyne'], md=[r'Powell & Thyne'], doi='10.1177/0022343310397436')
R('defenseone2016coups', 'other', 'misc', 'url', pats=[r'defenseone'], md=[],
  author='Collins', title='Military Coups Have Become Less Common, But More Successful', howpublished='Defense One', year='2016',
  url='https://www.defenseone.com/ideas/2016/07/military-coups-have-become-less-common-more-successful/130141/', urldate='2026-11-03', vtok='Military Coups',
  prob='Author given name not recorded ("Collins/Quartz").')
R('belkin2003', A, 'article', 'doi', pats=[r'Belkin'], md=[r'Belkin'], doi='10.1177/0022002703258197')
R('debruin2018', A, 'article', 'doi', pats=[r'De Bruin'], md=[r'De Bruin'], doi='10.1177/0022002717692652')
R('powell2012', A, 'article', 'doi', pats=[r'Powell \(2012\)'], md=[r'Powell \(?2012'], doi='10.1177/0022002712445732',
  prob='Marked unverified in v76/peace_force (no URL); DOI now confirmed here, but the claim itself was not checked against the text.')

# ---------------- Migration (v76) ----------------
R('unhcr2026gt', 'report', 'techreport', 'false', pats=[r'Global Trends: Forced Displacement in 2025', r'UNHCR Global Trends 2025', r'global-trends-report-2025'], md=[r'UNHCR Global Trends', r'117\.8 million', r'14\.7 million'],
  author='{UNHCR}', title='Global Trends: Forced Displacement in 2025', institution='UNHCR', year='2026',
  url='https://asile.ch/wp-content/uploads/2026/07/global-trends-report-2025.pdf', urldate='2026-11-03', note='Published June 2026; read from asile.ch mirror',
  prob='Read from a third-party mirror (asile.ch), not unhcr.org.')
R('unhcr2025gt', 'report', 'techreport', 'false', pats=[r'Global Trends: Forced Displacement in 2024', r'UNHCR Global Trends 2024', r'global-trends-report-2024'], md=[r'123\.2 million'],
  author='{UNHCR}', title='Global Trends: Forced Displacement in 2024', institution='UNHCR', year='2025',
  url='https://www.developmentaid.org/api/frontend/cms/file/2025/06/global-trends-report-2024.pdf', urldate='2026-11-03', note='Published June 2025; read from developmentaid.org mirror',
  prob='Read from a third-party mirror (developmentaid.org), not unhcr.org.')
R('idmc2025grid', 'report', 'techreport', 'false', pats=[r'IDMC Global Report on Internal Displacement 2025', r'IDMC GRID 2025', r'idmc-grid-2025'], md=[r'IDMC', r'GRID 2025', r'45\.8 million'],
  author='{Internal Displacement Monitoring Centre}', title='2025 Global Report on Internal Displacement (GRID 2025)', institution='IDMC', year='2025',
  url='https://datospaz.unidadvictimas.gov.co/archivos/datosPaz/especiales/idmc-grid-2025-global-report-on-internal-displacement.pdf', urldate='2026-11-03',
  prob='Read from a third-party mirror (Colombian Unidad para las Víctimas), not internal-displacement.org.')
R('idmc2026grid', 'report', 'techreport', 'false', pats=[r'IDMC GRID 2026'], md=[r'GRID 2026'],
  author='{Internal Displacement Monitoring Centre}', title='2026 Global Report on Internal Displacement (GRID 2026)', institution='IDMC', year='2026',
  prob='No URL; 29.9 million figure from a secondary summary only (unverified).')
R('wb2021groundswell', 'report', 'misc', 'url', pats=[r'Groundswell'], md=[r'Groundswell', r'216 million'],
  author='{World Bank}', title='Climate change could force 216 million people to migrate within their own countries by 2050 (press release on Groundswell Part 2)', year='2021',
  url='https://www.worldbank.org/en/news/press-release/2021/09/13/climate-change-could-force-216-million-people-to-migrate-within-their-own-countries-by-2050', urldate='2026-11-03', vtok='Groundswell',
  prob='Only the press release was read; cite the Groundswell Part 2 report (Clement et al. 2021) for the figures.')
R('undesa2020migration', 'report', 'techreport', 'false', pats=[r'International Migration 2020 Highlights'], md=[r'281 million'],
  author='{United Nations, Department of Economic and Social Affairs, Population Division}', title='International Migration 2020 Highlights', institution='United Nations', year='2020',
  url='https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2020_international_migration_highlights.pdf', urldate='2026-11-03')
R('undesa2024ims', 'data', 'misc', 'url', pats=[r'International Migrant Stock 2024'], md=[r'304 million'],
  author='{United Nations, Department of Economic and Social Affairs, Population Division}', title='International Migrant Stock 2024', year='2024',
  url='https://www.un.org/development/desa/pd/content/international-migrant-stock', urldate='2026-11-03', vtok='International Migrant Stock',
  prob='304 million (2024) from a search summary only (unverified).')
R('wb2023wdr', 'report', 'book', 'url', pats=[r'WDR 2023'], md=[r'WDR 2023'],
  author='{World Bank}', title='World Development Report 2023: Migrants, Refugees, and Societies', publisher='World Bank', year='2023',
  url='https://www.worldbank.org/en/publication/wdr2023', urldate='2026-11-03', vtok='World Development Report 2023')
R('clemens2008', 'report', 'techreport', 'false', pats=[r'Clemens, Montenegro'], md=[r'Clemens, Montenegro', r'Place premium'],
  author='Clemens, M. and Montenegro, C. and Pritchett, L.', title='The Place Premium: Wage Differences for Identical Workers across the US Border', institution='Center for Global Development', year='2008', type='Working Paper', number='148',
  url='https://www.cgdev.org/publication/place-premium-wage-differences-identical-workers-across-us-border-working-paper-148', urldate='2026-11-03',
  prob='Given names of the authors not recorded in project files (surnames/initials only); CGD page now blocked (403).')
R('clemens2014', 'report', 'techreport', 'false', pats=[r'Clemens 2014'], md=[r'Clemens \(?2014'],
  author='Clemens, M.', title='Does Development Reduce Migration?', institution='Center for Global Development', year='2014', type='Working Paper', number='359',
  url='https://www.cgdev.org/publication/does-development-reduce-migration-working-paper-359', urldate='2026-11-03', prob='CGD page now blocked (403).')
R('clemens2020', 'report', 'techreport', 'false', pats=[r'Clemens 2020'], md=[r'Clemens 2020', r'migration hump', r'Emigration Life Cycle'],
  author='Clemens, M.', title='The Emigration Life Cycle', institution='IZA Institute of Labor Economics', year='2020', type='IZA Discussion Paper', number='13614',
  url='https://docs.iza.org/dp13614.pdf', urldate='2026-11-03', prob='Subtitle and author given names of IZA DP 13614 not recorded in project files ("The Emigration Life Cycle" only).')
R('peaceaccords_mozambique', 'other', 'misc', 'url', pats=[r'peaceaccords\.nd\.edu'], md=[r'Mozambique'],
  author='{Peace Accords Matrix, University of Notre Dame}', title='Refugees: General Peace Agreement for Mozambique', url='https://peaceaccords.nd.edu/provision/refugees-general-peace-agreement-for-mozambique', urldate='2026-11-03', vtok='Mozambique')
R('unpk_onumoz', 'other', 'misc', 'url', pats=[r'onumozS'], md=[r'ONUMOZ'],
  author='{United Nations Peacekeeping}', title='ONUMOZ (United Nations Operation in Mozambique): background', url='https://peacekeeping.un.org/sites/default/files/past/onumozS.htm', urldate='2026-11-03', vtok='ONUMOZ')

# ---------------- v68 verification items ----------------
R('sgr2022military', 'report', 'techreport', 'false', pats=[r'Parkinson S\.', r'SGRCEOBS'], md=[r'SGR/CEOBS', r'5\.5 ?% of global'],
  author='Parkinson, S. and Cottrell, L.', title="Estimating the Military's Global Greenhouse Gas Emissions", institution='Scientists for Global Responsibility (SGR) and Conflict and Environment Observatory (CEOBS)', year='2022',
  url='https://ceobs.org/wp-content/uploads/2022/11/SGRCEOBS-Estimating_Global_MIlitary_GHG_Emissions_Nov22_rev.pdf', urldate='2026-11-03',
  prob='Authors given as initials only in project files.')
R('legi_ide2026', 'other', 'misc', 'false', pats=[r'Arrêté du 20 février 2026'], md=[r'4,?620 h'],
  author='{République française}', title="Arrêté du 20 février 2026 relatif au diplôme d'État d'infirmier (NOR ESRS2601184A)", year='2026',
  url='https://www.fhf.fr/sites/default/files/2026-02/Arr%C3%AAt%C3%A9%20r%C3%A9ing%C3%A9nierie%20formation%20IDE.pdf', urldate='2026-11-03', note='Read via FHF copy')
R('legi_ide2009', 'other', 'misc', 'false', pats=[r'JORFTEXT000020961044'], md=[],
  author='{République française}', title="Arrêté du 31 juillet 2009 relatif au diplôme d'État d'infirmier", year='2009',
  url='https://www.legifrance.gouv.fr/loda/id/JORFTEXT000020961044', urldate='2026-11-03', prob='Légifrance not readable by the fetcher (JS shell); text not checked.')
R('an2024q108', 'other', 'misc', 'false', pats=[r'QANR5L17QOSD108', r'question orale n°108'], md=[r'question 108'],
  author='{Assemblée nationale}', title='Question orale sans débat n° 108 (17e législature) et réponse du Gouvernement [durée du DES de médecine générale]',
  url='https://www.assemblee-nationale.fr/dyn/17/questions/QANR5L17QOSD108.pdf', urldate='2026-11-03', prob='Date of the question/answer not recorded.')
R('legi_deas2021', 'other', 'misc', 'false', pats=[r'Arrêté du 10 juin 2021'], md=[r'1,?540 h'],
  author='{République française}', title="Arrêté du 10 juin 2021 relatif à la formation conduisant au diplôme d'État d'aide-soignant", year='2021',
  note='Read as reproduced in CHRU Strasbourg IFAS programme 2026-2027 (chru2026ifas)', prob='Arrêté read only as reproduced in a training-institute programme.')
R('chru2026ifas', 'other', 'misc', 'false', pats=[r'chru-strasbourg'], md=[],
  author='{CHRU de Strasbourg, IFAS}', title='Fiches programmes aide-soignant 2026--2027', year='2026',
  url='https://formation.chru-strasbourg.fr/wp-content/uploads/sites/2/2026/06/fiches-programmes-as-2026-2027.pdf', urldate='2026-11-03')
R('who2025sown', 'report', 'techreport', 'false', pats=[r"State of the World's Nursing 2025", r'a4173924-a18f'], md=[r'SOWN', r'25\.3'],
  author='{World Health Organization}', title="State of the world's nursing 2025", institution='World Health Organization', year='2025',
  url='https://iris.who.int/server/api/core/bitstreams/a4173924-a18f-49b6-8bd1-9c2a4a098980/content', urldate='2026-11-03')
R('iea2026wei', 'report', 'techreport', 'false', pats=[r'World Energy Investment 2026', r'WorldEnergyInvestment2026'], md=[r'World Energy Investment 2026', r'WEI 2026', r'20 ?% to developing'],
  author='{International Energy Agency}', title='World Energy Investment 2026', institution='IEA', year='2026',
  url='https://www.iea.org/files/64594543-cf6e-4fd9-8238-d3cae35daf48/WorldEnergyInvestment2026.pdf', urldate='2026-11-03')
R('iea2025wei', 'report', 'techreport', 'false', pats=[r'World Energy Investment 2025', r'WorldEnergyInvestment2025'], md=[r'WEI 2025'],
  author='{International Energy Agency}', title='World Energy Investment 2025', institution='IEA', year='2025',
  url='https://www.iea.org/files/1c136349-1c31-4201-9ed7-1a7d532e4306/WorldEnergyInvestment2025.pdf', urldate='2026-11-03')
R('oecd2026oda', 'other', 'misc', 'url', pats=[r'OECD preliminary ODA', r'hellenicaid'], md=[r'0\.26 ?%', r'174\.3', r'development aid'],
  author='{OECD}', title='Preliminary official development assistance (ODA) levels in 2025 (press release of 9 April 2026, as reproduced by Hellenic Aid, Greek Ministry of Foreign Affairs)', year='2026',
  url='https://hellenicaid.mfa.gr/en/preliminary-official-development-assistance-oda-levels-in-2025/', urldate='2026-11-03', vtok='Preliminary Official Development Assistance',
  prob='ODA figure conflict: earlier text used ~0.33% of GNI; v68 verification corrected it to 0.26% (2025 preliminary; 0.34% in 2024). Check every place that still says 0.33%. OECD page itself blocked (403).')
