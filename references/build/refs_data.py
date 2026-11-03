# Official statistics and datasets. Group 'data'.
# R(key, group, bibtype, verified, pats, md, problems, **fields)
from reg import R

D = '2026-11-03'

# ---------------- Eurostat datasets (titles/DOIs checked live against Eurostat SDMX dataflow metadata) -------
EST = [
 # code, first retrieval date in manifests, extra md pattern
 ('nama_10_a64_e', D), ('nama_10_a64', D), ('lfsa_ewhun2', D), ('lfsa_ewhan2', D), ('lfsa_epgan2', D),
 ('lfsi_sla_a', D), ('lfsi_emp_a', D), ('lfsa_epgar', D), ('lfsa_igar', D), ('lfsi_long_a', D),
 ('lfsi_long_q', D), ('lfsi_long_e06', D), ('lfsi_long_e01', D), ('lfsi_long_e08', D), ('ilc_lvhl30', D),
 ('hlth_rs_prs2', D), ('hlth_rs_grd2', D), ('hlth_rs_prshp2', D), ('jvs_a_rate_r2', D), ('naio_10_cp1700', D),
 ('demo_pjan', D), ('lfst_hhnhtych', D), ('lfsa_egais', D), ('ilc_lvho02', D), ('ilc_hcmh02', D),
 ('ilc_lvph01', D), ('ilc_di01', D), ('sts_cobp_a', D), ('cens_21dwop_r3', D),
]
for code, d in EST:
    key = 'eurostat_' + code.replace('_', '')
    R(key, 'data', 'misc', 'eurostat', pats=[r'\b' + code + r'\b'], md=[r'\b' + code + r'\b'],
      estat=code, author='{Eurostat}', year='2026',
      url='https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/' + code,
      urldate=d, howpublished='Eurostat database (online data code ' + code.replace('_', r'\_') + ')',
      note='Dataset; queried through the Eurostat dissemination API with the filters recorded in the project raw\\_manifest.csv files')

# extra md patterns for generic mentions of Eurostat income deciles (v74)
R('eurostat_ilcdi01', extend=True, md=[r'Eurostat 2024 income deciles', r'income deciles \(Eurostat'])
R('eurostat_lfsiempa', extend=True, md=[r'IS 85\.8', r'Iceland 85%'])

R('eurostat_se_energy', 'data', 'misc', 'url', pats=[r'Energy_statistics_-_an_overview'],
  md=[r'81\.7 GJ', r'36,?755', r'124 GJ'],
  author='{Eurostat}', title='Energy statistics -- an overview', howpublished='Statistics Explained',
  url='https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Energy_statistics_-_an_overview',
  urldate=D, note='Data extracted September 2026 (as recorded in v65/thresholds)', vtok='Energy statistics')
R('eurostat_se_physicians', 'data', 'misc', 'url', pats=[r'Healthcare_personnel_statistics'],
  md=[r'131 (health workers )?per 10[ ,]?000', r'EU 131'],
  author='{Eurostat}', title='Healthcare personnel statistics -- physicians', howpublished='Statistics Explained',
  url='https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Healthcare_personnel_statistics_-_physicians',
  urldate=D, vtok='Healthcare personnel')
R('eurostat_database', 'data', 'misc', 'url', pats=[r'eurostat/web/main/data/database'], md=[r'eurostat/web/main/data/database'],
  author='{Eurostat}', title='Eurostat database', url='https://ec.europa.eu/eurostat/web/main/data/database', urldate=D,
  note='Generic link to the database used in the Working Paper source table', vtok='Database')

# ---------------- World Bank (indicator names checked live against api.worldbank.org) -------------
WB = [('SP.POP.TOTL', r'SP\.POP\.TOTL', [r'World Bank, 8\.14 billion', r'8,?140,?897,?523']),
      ('SP.POP.1564.TO.ZS', r'SP\.POP\.1564', []),
      ('SP.POP.65UP.TO.ZS', r'SP\.POP\.65UP\.TO\.ZS(?!.*(source=40|_2050))', []),
      ('SL.EMP.TOTL.SP.ZS', r'SL\.EMP\.TOTL', []),
      ('SP.POP.DPND.OL', r'SP\.POP\.DPND\.OL(?!.*(source=40|_2050))', []),
      ('MS.MIL.TOTL.P1', r'MS\.MIL\.TOTL\.P1', [r'27\.4 ?(m|million)', r'armed forces number 27\.4']),
      ('MS.MIL.TOTL.TF.ZS', r'MS\.MIL\.TOTL\.TF', [r'0\.79% of the labour force']),
      ('MS.MIL.XPND.GD.ZS', r'MS\.MIL\.XPND', []),
      ('NY.GDP.MKTP.CD', r'NY\.GDP\.MKTP', [])]
for code, pat, md in WB:
    key = 'wb_' + code.replace('.', '').lower()
    R(key, 'data', 'misc', 'wb', pats=[pat], md=[pat] + md, wbcode=code, author='{World Bank}', year='2026',
      url='https://api.worldbank.org/v2/country/all/indicator/' + code, urldate=D,
      howpublished='World Development Indicators (indicator ' + code + ')',
      note='Dataset; accessed through the World Bank API v2')
R('wb_popproj', 'data', 'misc', 'wb', pats=[r'source=40', r'wb40_', r'Population Estimates and Projections'],
  md=[r'Population Estimates and Projections'],
  author='{World Bank}', title='Population estimates and projections (database, source 40): SP.POP.TOTL, SP.POP.65UP.TO.ZS, SP.POP.DPND.OL for 2050',
  year='2026', url='https://api.worldbank.org/v2/sources/40', urldate=D,
  note='Dataset; source last updated 2026-07-01 per World Bank API (checked in this task)')
R('wb_countrymeta', 'data', 'misc', 'url', pats=[r'api\.worldbank\.org/v2/country\?format'], md=[],
  author='{World Bank}', title='World Bank API v2: country list with aggregate/region flags', year='2026',
  url='https://api.worldbank.org/v2/country?format=json&per_page=400', urldate=D, note='Metadata file used to drop aggregates')
R('wb_dataportal', 'data', 'misc', 'url', pats=[r'data\.worldbank\.org/?$'], md=[r'\[World Bank\]\(https://data\.worldbank\.org'],
  author='{World Bank}', title='World Bank Open Data', url='https://data.worldbank.org/', urldate=D, vtok='World Bank Open Data')

# ---------------- WHO GHO / NHWA (indicator names checked live against WHO xMart REF_INDICATOR) -------------
for code, name, md in [('HWF_0001', 'Medical doctors (per 10 000 population)', []),
                       ('HWF_0002', 'Medical doctors (number)', [r'47\.4 ?(m|million)']),
                       ('HWF_0006', 'Nursing and midwifery personnel (per 10 000 population)', [r'58 per 10[ ,]?000']),
                       ('HWF_0007', 'Nursing and midwifery personnel (number)', [])]:
    R('who_gho_' + code.replace('_', '').lower(), 'data', 'misc', 'who', pats=[code], md=[code] + md,
      author='{World Health Organization}', title=name + ' [indicator ' + code + ']',
      howpublished='Global Health Observatory, National Health Workforce Accounts data (xMart public OData API)',
      year='2026', url="https://xmart-api-public.who.int/GHO/FACT?$filter=INDICATOR_CODE eq '" + code + "'", urldate=D,
      note='Dataset')
R('who_gho_refindicator', 'data', 'misc', 'who', pats=[r'REF_INDICATOR'], md=[],
  author='{World Health Organization}', title='Global Health Observatory indicator registry (REF\\_INDICATOR, HWF\\_ codes)',
  year='2026', url='https://xmart-api-public.who.int/GHO/REF_INDICATOR', urldate=D, note='Metadata used for code verification')
R('who_nhwa', 'data', 'misc', 'url', pats=[], md=[r'National Health Workforce Accounts'],
  author='{World Health Organization}', title='National Health Workforce Accounts (NHWA) data portal', year='2026',
  urldate=D, note='Named in the book (Ch. 1) as the source of the HWF indicators accessed via the xMart API',
  prob='No URL for the NHWA portal recorded in project files; cite the indicator entries who_gho_hwf000x instead.')

# ---------------- ILOSTAT (dataflow names checked live against sdmx.ilo.org) -------------
R('ilostat_eap', 'data', 'misc', 'ilo', pats=[r'EAP_2EAP_SEX_AGE_NB'], md=[r'EAP_2EAP'],
  author='{International Labour Organization}', title='Labour force by sex and age -- ILO modelled estimates, Nov. 2025 (EAP\\_2EAP\\_SEX\\_AGE\\_NB\\_A)',
  howpublished='ILOSTAT', year='2025', url='https://rplumber.ilo.org/data/indicator/?id=EAP_2EAP_SEX_AGE_NB_A', urldate=D, note='Dataset')
R('ilostat_emp_age', 'data', 'misc', 'ilo', pats=[r'EMP_2EMP_SEX_AGE_NB'],
  md=[r'ILO modelled estimates', r'ILO modelled', r'3\.53 bn employed'],
  author='{International Labour Organization}', title='Employment by sex and age -- ILO modelled estimates, Nov. 2025 (EMP\\_2EMP\\_SEX\\_AGE\\_NB\\_A)',
  howpublished='ILOSTAT', year='2025', url='https://rplumber.ilo.org/data/indicator/?id=EMP_2EMP_SEX_AGE_NB_A', urldate=D, note='Dataset')
R('ilostat_hours', 'data', 'misc', 'ilo', pats=[r'HOW_TEMP_SEX_NB'], md=[r'40\.7 h'],
  author='{International Labour Organization}', title='Average weekly hours actually worked per employed person by sex (HOW\\_TEMP\\_SEX\\_NB\\_A)',
  howpublished='ILOSTAT', year='2026', url='https://rplumber.ilo.org/data/indicator/?id=HOW_TEMP_SEX_NB_A', urldate=D, note='Dataset')
R('ilostat_emp_eco', 'data', 'misc', 'ilo', pats=[r'EMP_2EMP_SEX_ECO_NB'],
  md=[r'294 ?(m|million)', r'294\.4'],
  author='{International Labour Organization}', title='Employment by sex and economic activity -- ILO modelled estimates, Nov. 2025 (EMP\\_2EMP\\_SEX\\_ECO\\_NB), construction aggregate',
  howpublished='ILOSTAT SDMX API', year='2025', url='https://sdmx.ilo.org/rest/data/ILO,DF_EMP_2EMP_SEX_ECO_NB,1.0/.A..SEX_T.ECO_AGGREGATE_CON', urldate=D, note='Dataset')
R('ilostat_dic_refarea', 'data', 'misc', 'false', pats=[r'ilo_dic_ref_area|metadata/dic/\?var=ref_area'], md=[],
  author='{International Labour Organization}', title='ILOSTAT reference-area dictionary (aggregate labels)', howpublished='ILOSTAT',
  url='https://rplumber.ilo.org/metadata/dic/?var=ref_area&format=.csv&lang=en', urldate=D, note='Metadata file')

# ---------------- FAO / OWID / UN -------------
R('fao_fbs', 'data', 'misc', 'false', pats=[r'FoodBalanceSheets_E_All_Data', r'FAOSTAT Food Balance'],
  md=[r'FAO [Ff]ood [Bb]alance [Ss]heets', r'3,?017 kcal', r'92 g/person'],
  author='{Food and Agriculture Organization of the United Nations}', title='FAOSTAT Food Balance Sheets (2010--), bulk download',
  howpublished='FAOSTAT', url='https://bulks-faostat.fao.org/production/FoodBalanceSheets_E_All_Data.zip', urldate=D, note='Dataset')
R('owid_calories', 'data', 'misc', 'url', pats=[r'daily-per-capita-caloric-supply'], md=[r'3,?006 kcal'],
  author='{Our World in Data}', title='Daily supply of calories per person (grapher daily-per-capita-caloric-supply; data from FAO Food Balance Sheets)',
  url='https://ourworldindata.org/grapher/daily-per-capita-caloric-supply', urldate=D, note='Dataset; republication of FAO data', vtok='calorie')
R('owid_protein', 'data', 'misc', 'url', pats=[r'daily-per-capita-protein-supply'], md=[],
  author='{Our World in Data}', title='Daily supply of protein per person (grapher daily-per-capita-protein-supply; data from FAO Food Balance Sheets)',
  url='https://ourworldindata.org/grapher/daily-per-capita-protein-supply', urldate=D, note='Dataset; republication of FAO data', vtok='protein')
R('owid_energy', 'data', 'misc', 'false', pats=[r'owid-energy-data', r'Our World in Data energy'],
  md=[r'Our World in Data energy', r'from Our World in Data'],
  author='{Our World in Data}', title='Energy dataset (owid-energy-data.csv; compiled from Energy Institute, Ember and EIA data)',
  url='https://github.com/owid/energy-data', urldate=D,
  note='Dataset; downloaded from https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv; marked for recheck in the project')
R('owid_mder', 'data', 'misc', 'url', pats=[r'minimum-requirement-calories'], md=[r'MDER', r'1,?836 kcal'],
  author='{Our World in Data}', title='Minimum dietary energy requirement (grapher minimum-requirement-calories; data from FAO Suite of Food Security Indicators 2025)',
  url='https://ourworldindata.org/grapher/minimum-requirement-calories', urldate=D, note='Dataset; republication of FAO data', vtok='energy')
R('owid_pupilteacher', 'data', 'misc', 'url', pats=[r'pupil-teacher-ratio-for-primary'], md=[r'25\.7 (vs|pupils)'],
  author='{Our World in Data}', title='Pupil-qualified teacher ratio in primary education (data from UNESCO Institute for Statistics)',
  url='https://ourworldindata.org/grapher/pupil-teacher-ratio-for-primary-education-by-country', urldate=D, note='Dataset; republication of UNESCO UIS data', vtok='teacher')
R('owid_ucdp_deaths', 'data', 'misc', 'url', pats=[r'deaths-in-state-based-conflicts-by-region'], md=[r'\bUCDP\b'],
  author='{Our World in Data}', title='Deaths in state-based armed conflicts, by region (data from Uppsala Conflict Data Program)',
  url='https://ourworldindata.org/grapher/deaths-in-state-based-conflicts-by-region', urldate=D, note='Dataset; republication of UCDP data', vtok='conflict')
R('owid_gbd_conflict', 'data', 'misc', 'false', pats=[r'deaths-from-conflict-and-terrorism'], md=[],
  author='{Our World in Data}', title='Deaths from conflict and terrorism (data from IHME Global Burden of Disease)',
  url='https://ourworldindata.org/grapher/deaths-from-conflict-and-terrorism', urldate=D,
  note='Dataset; values NOT retrieved in the project (non-redistributable)')
R('unsd_m49', 'data', 'misc', 'url', pats=[r'unstats\.un\.org/unsd/methodology/m49'], md=[r'\bM49\b'],
  author='{United Nations Statistics Division}', title='Standard country or area codes for statistical use (M49): overview',
  url='https://unstats.un.org/unsd/methodology/m49/overview/', urldate=D, vtok='M49')
R('unwpp2024', 'data', 'misc', 'false', pats=[r'WPP2024', r'World Population Prospects 2024', r'population\.un\.org/wpp'],
  md=[r'UN WPP 2024', r'World Population Prospects 2024', r'UN 2024 projection', r'9\.66 billion', r'UN WPP 2050'],
  author='{United Nations, Department of Economic and Social Affairs, Population Division}',
  title='World Population Prospects 2024: Demographic indicators, medium variant (WPP2024\\_Demographic\\_Indicators\\_Medium.csv.gz)',
  year='2024', url='https://population.un.org/wpp/', urldate=D, note='Dataset; CSV downloaded from population.un.org/wpp/assets')
R('iamc_commondefs', 'data', 'misc', 'false', pats=[r'IAMconsortium/common-definitions'], md=[],
  author='{IAMC (Integrated Assessment Modeling Consortium)}', title='common-definitions: IMAGE 3.2 native region to country mapping (IMAGE\\_v3.2.yaml)',
  url='https://github.com/IAMconsortium/common-definitions', urldate=D, note='Dataset (CC0-1.0), GitHub repository')
R('oecd_healthgrad', 'data', 'misc', 'false', pats=[r'DSD_HEALTH_REAC_EMP@DF_GRAD'], md=[r'OECD graduates', r'OECD ratios'],
  author='{OECD}', title='OECD Health Statistics: health graduates (dataflow DSD\\_HEALTH\\_REAC\\_EMP@DF\\_GRAD)',
  url='https://sdmx.oecd.org/public/rest/data/OECD.ELS.HD,DSD_HEALTH_REAC_EMP@DF_GRAD,/all', urldate=D, note='Dataset (SDMX CSV)')
R('deetman_buma', 'data', 'misc', 'false', pats=[r'SPDeetman/BUMA'], md=[r'\bIMAGE\b'],
  author='Deetman, S. and others', title='BUMA: building material model -- model inputs (IMAGE population, residential floor space per capita, rural population share)',
  url='https://github.com/SPDeetman/BUMA', urldate=D, note='Dataset (MIT licence), GitHub repository accompanying deetman2020')

# ---------------- National official statistics -------------
R('insee2026ecrt', 'data', 'misc', 'url', pats=[r'insee\.fr/fr/statistiques/87330(39|71|75)'],
  md=[r'\bINSEE\b.*38\.9', r'38\.9 (usual )?(weekly )?h', r'1,?656 h', r'ECRT 2026', r'insee\.fr/fr/statistiques/8733071'],
  author='{INSEE}', title='Emploi, chômage, revenus du travail -- Édition 2026 (Insee Références): fiches « Évolution de l\'emploi », « Durée du travail », « Temps partiel »',
  year='2026', url='https://www.insee.fr/fr/statistiques/8733071?sommaire=8733125', urldate=D,
  note='Published 2026-07-02; fiches 8733039, 8733071 and 8733075; data file ECRT2026\\_F17.xlsx', vtok='Emploi, chômage, revenus du travail')

R('insee2024compta', 'data', 'misc', 'url', pats=[r'insee\.fr/fr/statistiques/8193933'], md=[r'2,?822\.5'],
  author='{INSEE}', title='Les comptes de la Nation en 2023 (Insee Première no. 1997)', year='2024',
  url='https://www.insee.fr/fr/statistiques/8193933?sommaire=8068749', urldate=D, note='Published 2024-05-31; first (provisional) vintage', vtok='Les comptes de la Nation en 2023')

R('insee2025log2022', 'data', 'misc', 'url', pats=[r'insee\.fr/fr/statistiques/8581193'], md=[r'136,?957'],
  author='{INSEE}', title='Logement en 2022 -- Chiffres détaillés (Département de Paris; unité urbaine de Paris)', year='2025',
  url='https://www.insee.fr/fr/statistiques/8581193?geo=DEP-75', urldate=D, note='Published 2025-06-26; census RP2022; also geo=UU2020-00851', vtok='Logement en 2022')

R('insee2026dc_paris', 'data', 'misc', 'url', pats=[r'insee\.fr/fr/statistiques/2011101\?geo=COM-75056'], md=[r'28\.2 ?/ ?2\.6'],
  author='{INSEE}', title='Dossier complet -- Commune de Paris (75056)', year='2026',
  url='https://www.insee.fr/fr/statistiques/2011101?geo=COM-75056', urldate=D, note='Published 2026-08-27; rolling page (RP2023)', vtok='Commune de Paris')

R('insee2026dc_vallauris', 'data', 'misc', 'url', pats=[r'insee\.fr/fr/statistiques/2011101\?geo=COM-06155'], md=[r'Vallauris'],
  author='{INSEE}', title='Dossier complet -- Commune de Vallauris (06155)', year='2026',
  url='https://www.insee.fr/fr/statistiques/2011101?geo=COM-06155', urldate=D, note='Published 2026-08-27; rolling page (RP2023)', vtok='Commune de Vallauris')

R('rte_bilan2023', 'data', 'misc', 'url', pats=[r'bilan-electrique-2023'], md=[r'\bRTE\b'],
  author='{RTE (Réseau de transport d\'électricité)}', title='Bilan électrique 2023 (Synthèse; Consommation; Production)',
  url='https://analysesetdonnees.rte-france.com/bilan-electrique-2023/synthese', urldate=D, vtok='Bilan électrique 2023')

R('sdes_maprimerenov', 'data', 'misc', 'url', pats=[r'tableau-de-suivi-de-la-renovation-energetique'], md=[r'MaPrimeR[ée]nov'],
  author='{SDES (Ministère de la Transition écologique)}', title='Tableau de suivi de la rénovation énergétique dans le secteur résidentiel',
  url='https://www.statistiques.developpement-durable.gouv.fr/tableau-de-suivi-de-la-renovation-energetique-dans-le-secteur-residentiel', urldate=D, vtok='Tableau de suivi')

R('gla2026empty', 'data', 'misc', 'url', pats=[r'empty-homes-london'], md=[r'105,?138'],
  author='{London Assembly Research Unit}', title='Empty homes in London', year='2026',
  url='https://www.london.gov.uk/who-we-are/what-london-assembly-does/london-assembly-research-unit-publications/empty-homes-london', urldate=D,
  note='Published 8 June 2026', vtok='Empty homes in London')

R('mhclg2025lt615', 'data', 'misc', 'false', pats=[r'Live_Table_615'], md=[r'Table 615', r'93,?602'],
  author='{Ministry of Housing, Communities and Local Government}', title='Live Table 615: vacant dwellings by local authority district, England (sheet All\\_vacants)', year='2025',
  url='https://assets.publishing.service.gov.uk/media/6a2bf816e50716856ed4afdd/Live_Table_615.ods', urldate=D, note='November 2025 edition')
R('gla2026hil', 'data', 'misc', 'false', pats=[r'Housing%20in%20London%202025'], md=[r'Housing in London 2025'],
  author='{Greater London Authority}', title='Housing in London 2025', year='2026',
  url='https://www.london.gov.uk/sites/default/files/2026-01/Housing%20in%20London%202025%20report%20%28002%29.pdf', urldate=D)
R('nychpd_nychvs2023', 'data', 'misc', 'false', pats=[r'2023-nychvs-selected-initial-findings'], md=[r'NYCHVS', r'1\.41 ?%'],
  author='{NYC Department of Housing Preservation and Development}', title='2023 New York City Housing and Vacancy Survey: Selected initial findings',
  url='https://www.nyc.gov/assets/hpd/downloads/pdfs/about/2023-nychvs-selected-initial-findings.pdf', urldate=D)
R('nyc_fastfacts', 'data', 'misc', 'false', pats=[r'fast-facts-about-housing-in-nyc'], md=[],
  author='{City of New York}', title='Fast facts about housing in NYC (Tenant Protection)',
  url='https://www.nyc.gov/content/tenantprotection/pages/fast-facts-about-housing-in-nyc', urldate=D,
  note='Page returned only a JavaScript shell in the v62 audit; figures confirmed from nychpd_nychvs2023')
R('tmg2026tokyo', 'data', 'misc', 'false', pats=[r'jyuuseishinkikakubukai_tokyonojutakujijo'], md=[r'896,?500'],
  author='{Tokyo Metropolitan Government, Bureau of Housing Policy}', title='東京の住宅事情 [Housing conditions in Tokyo] (subcommittee material, 24 April 2026)', year='2026',
  url='https://www.juutakuseisaku.metro.tokyo.lg.jp/documents/d/juutakuseisaku/jyuuseishinkikakubukai_tokyonojutakujijo_260424', urldate=D,
  note='Data: 2023 Housing and Land Survey')
R('statjapan2024hls', 'data', 'misc', 'url', pats=[r'stat\.go\.jp/english/info/news/20241030'], md=[r'9\.002', r'13\.8 ?%'],
  author='{Statistics Bureau of Japan}', title='2023 Housing and Land Survey: Basic tabulation on dwellings and households (news bulletin, 30 October 2024)', year='2024',
  url='https://www.stat.go.jp/english/info/news/20241030.html', urldate=D, vtok='Statistics Bureau')

R('mhclg2026ehs', 'data', 'misc', 'url', pats=[r'english-housing-survey-2024-to-2025'], md=[r'7,?480', r'English Housing Survey'],
  author='{Ministry of Housing, Communities and Local Government}', title='English Housing Survey 2024 to 2025: headline findings on housing quality and energy efficiency, Chapter 2: Energy efficiency', year='2026',
  url='https://www.gov.uk/government/statistics/chapters-for-english-housing-survey-2024-to-2025-headline-findings-on-housing-quality-and-energy-efficiency/chapter-2-energy-efficiency',
  urldate=D, note='Published 29 January 2026; Annex Tables 2.2 and 2.14', vtok='Energy efficiency')

R('destatis_dwellings', 'data', 'misc', 'url', pats=[r'destatis\.de/EN/Themes/Society-Environment/Housing/Tables/liste-dwellings'], md=[r'49\.5 m'],
  author='{Statistisches Bundesamt (Destatis)}', title='Dwelling stock (table, as at 16 July 2026)', year='2026',
  url='https://www.destatis.de/EN/Themes/Society-Environment/Housing/Tables/liste-dwellings.html', urldate=D, vtok='Dwelling')
R('uscensus_chars', 'data', 'misc', 'url', pats=[r'census\.gov/construction/chars'], md=[],
  author='{U.S. Census Bureau}', title='Characteristics of New Housing: highlights',
  url='https://www.census.gov/construction/chars/highlights.html', urldate=D, vtok='Characteristics')
for y, path, ttl in [('2014', '201401/t20140120_502515', 'National Real Estate Development and Sales in 2013'), ('2016', '201601/t20160120_1307100', 'National Real Estate Development and Sales in 2015'),
                     ('2022', '202201/t20220118_1826502', 'National Real Estate Development and Sales in 2021'), ('2024', '202402/t20240201_1947107', 'Investment in Real Estate Development in 2023'),
                     ('2025', '202501/t20250124_1958446', 'Investment in Real Estate Development in 2024'), ('2026', '202601/t20260120_1962353', 'Investment in Real Estate Development for 2025')]:
    R('nbs' + y + 'realestate', 'data', 'misc', 'url', pats=[path], md=[],
      author='{National Bureau of Statistics of China}', title=ttl + ' (press release)', year=y,
      url='https://www.stats.gov.cn/english/PressRelease/' + path + '.html', urldate=D,
      vtok='Real Estate')
R('nbs2011csy', 'data', 'misc', 'url', pats=[r'ndsj/2011/html/O1502e'], md=[r'China Statistical Yearbook 2011', r'CSY 2011'],
  author='{National Bureau of Statistics of China}', title='China Statistical Yearbook 2011, Table 15-2', year='2011',
  url='https://www.stats.gov.cn/sj/ndsj/2011/html/O1502e.htm', urldate=D, vtok='')
R('nbs2012csy', 'data', 'misc', 'url', pats=[r'ndsj/2012/html/J1035e'], md=[r'China Statistical Yearbook 2012', r'CSY 2012'],
  author='{National Bureau of Statistics of China}', title='China Statistical Yearbook 2012, Table 10-35', year='2012',
  url='https://www.stats.gov.cn/sj/ndsj/2012/html/J1035e.htm', urldate=D, vtok='')
R('pib2025pmayg', 'data', 'misc', 'false', pats=[r'doc2025924644801'], md=[r'PMAY-G'],
  author='{Press Information Bureau, Government of India}', title='Sapno Ka Ghar (factsheet on Pradhan Mantri Awas Yojana -- Gramin)', year='2025',
  url='https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/sep/doc2025924644801.pdf', urldate=D, note='September 2025')
R('hdb2020ar', 'data', 'misc', 'false', pats=[r'AR2020KS'], md=[],
  author='{Housing \\& Development Board}', title='Annual Report 2019/2020: Key statistics', year='2020',
  url='https://assets.hdb.gov.sg/about-us/news-and-publications/annual-report/2020/ebook/AR2020KS.pdf', urldate=D,
  note='PDF not fetchable; values from search snippet only')
R('mospi_housing', 'data', 'misc', 'false', pats=[r'mospi\.gov\.in'], md=[r'TG-12', r'18\.78'],
  author='{Ministry of Statistics and Programme Implementation}', title='Statistical Year Book India, chapter 28: Housing (citing the Technical Group on Urban Housing Shortage, TG-12)',
  url='https://mospi.gov.in/sites/default/files/Statistical_year_book_india_chapters/HOUSING%20-%20WRITEUP.pdf', urldate=D)
R('loksabha2013vacant', 'data', 'misc', 'false', pats=[r'eparlib\.nic\.in'], md=[],
  author='{Lok Sabha (Ministry of Housing and Urban Poverty Alleviation)}', title='Answer on vacant census houses, 2011', year='2013',
  url='https://eparlib.nic.in/bitstream/123456789/643554/1/142992.pdf', urldate=D, note='DNS failure in project; snippet only')
R('statec2025census', 'data', 'misc', 'url', pats=[r'statistiques\.public\.lu'], md=[r'Luxembourg.{0,80}(car|commut|transit|public transport)'],
  author='{STATEC}', title='Recensement de la population 2021: transports (RP2021, release 18)', year='2025',
  url='https://statistiques.public.lu/en/actualites/2025/rp2021-transports-18.html', urldate=D, vtok='Car Dependency')

R('arcep2011obs', 'data', 'misc', 'false', pats=[r'obs-marches-t1-2011'], md=[r'ARCEP'],
  author='{ARCEP}', title='Observatoire des marchés des communications électroniques, 1er trimestre 2011', year='2011',
  url='https://www.arcep.fr/fileadmin/reprise/observatoire/1-2011/obs-marches-t1-2011.pdf', urldate=D)
R('arcep2013obs', 'data', 'misc', 'false', pats=[r'obs-march-t12013'], md=[],
  author='{ARCEP}', title='Observatoire des marchés des communications électroniques, 1er trimestre 2013', year='2013',
  url='https://www.arcep.fr/fileadmin/reprise/observatoire/1-2013/obs-march-t12013.pdf', urldate=D)
R('arcep2015obs', 'data', 'misc', 'false', pats=[r'obs-marches-t1_2015'], md=[],
  author='{ARCEP}', title='Observatoire des marchés des communications électroniques, 1er trimestre 2015', year='2015',
  url='https://www.arcep.fr/fileadmin/reprise/observatoire/1-2015/obs-marches-t1_2015.pdf', urldate=D)
R('arcep2024marche2023', 'data', 'misc', 'false', pats=[r'marche-communications-electroniques-france-2023'], md=[r'7 minutes a day', r'14 GB'],
  author='{ARCEP}', title='Le marché des communications électroniques en France en 2023 (résultats provisoires)',
  url='https://www.arcep.fr/cartes-et-donnees/nos-publications-chiffrees/observatoire-des-marches-des-communications-electroniques-en-france/marche-communications-electroniques-france-2023-resultats-provisoires.html', urldate=D)
R('fao_sdg1231', 'data', 'misc', 'url', pats=[r'1231-global-food-losses'], md=[r'12\.3\.1', r'13\.3 ?%', r'supply-chain loss'],
  author='{Food and Agriculture Organization of the United Nations}', title='SDG indicator 12.3.1a: Global food losses (SDG data portal)',
  url='https://www.fao.org/sustainable-development-goals-data-portal/data/indicators/1231-global-food-losses/en', urldate=D, vtok='12.3.1')
