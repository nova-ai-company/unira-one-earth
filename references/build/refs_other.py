from reg import R

R('kornai1980', 'book', 'book', True, pats=[r'Kornai'], md=[r'Kornai', r'Economics of Shortage'],
  author='Kornai, János', title='Economics of Shortage', publisher='North-Holland', address='Amsterdam', year='1980',
  note='Two volumes; details confirmed via Open Library',
  prob='Cited without page or chapter (v63/DESIGN_CLARIFICATIONS, book Ch. 4 and 9); add the chapter on shortage/queueing if a specific mechanism is quoted.')
R('penrose1946', 'article', 'article', 'doi', pats=[r'Penrose'], md=[r'Penrose'], doi='10.2307/2981392',
  prob='Constitution Art. 23 names "the Penrose rule" without a reference; this entry (Penrose 1946) was added and verified here.')
R('ilo_c029', 'other', 'misc', 'false', pats=[], md=[r'ILO Conventions 29 and 105', r'ILO conventions'],
  author='{International Labour Organization}', title='Convention No. 29 [forced labour]', year='1930',
  prob='ILO Conventions 29 and 105 are named in the constitution (Art. 7) and book Ch. 3 without full titles/URLs; NORMLEX blocked the fetcher, so titles were not confirmed.')
R('ilo_c105', 'other', 'misc', 'false', pats=[], md=[r'ILO Conventions 29 and 105'],
  author='{International Labour Organization}', title='Convention No. 105 [abolition of forced labour]', year='1957',
  prob='See ilo_c029.')
R('eu_council_qmv', 'other', 'misc', 'false', pats=[], md=[r'Council of the European Union'],
  author='{Council of the European Union}', title='Qualified majority voting rule (55% of member states representing 65% of the EU population)',
  prob='Constitution Art. 25 says the 55%/65% thresholds "follow the Council of the European Union" without a legal reference (Treaty on European Union, Art. 16(4)); the treaty text was not fetched (site blocked).')
R('statjapan2024hls', extend=True,
  prob='Date mismatch: URL and project say news of 30 October 2024 ("20241030"), but the page title reads "News Bulletin September 30, 2024"; v62/audit says the basic tabulation was released 25 Sep 2024.')
R('who_nhwa', extend=True)
