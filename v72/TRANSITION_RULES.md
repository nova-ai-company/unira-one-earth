# UNIRA transition rules — draft for the author's decision (2026-11-03)

**Principles kept:**
- voluntary joining;
- no seizure of homes and no forced relocation;
- the money cap (rule 18);
- needs-based allocation;
- rights are never reduced.

**Evidence:** `evidence/evidence.md` (61 findings on German reunification, EU enlargement, the euro, debt relief, land reforms, wealth taxes and household debt).
**Model:** `joining/run.py`.

## What the models show
- **86% of humanity (146 regions) gains materially by joining**: Ethiopia +170%, Nigeria +136%, India +72%, Indonesia +54%, Brazil +11%. China is about neutral (+2%).
- **14% (33 rich regions) loses materially by 6–12%**, in energy use only (France −6%, USA and Japan −12%). They keep comfortable levels, and their health care and housing are unchanged. Joining is worthwhile for them if peace, security, the 30-hour week and a stable climate are worth more than that loss.
- **A union of only the gaining regions works on its own resources, at about half speed.** By year 15 it closes 20% of the energy gap, 15% of the health gap and 25% of the housing gap by year 30, against 52%, 34% and 40% for the whole world. That still beats the best market world (14%, 4%, 10%). **UNIRA can start with willing regions and grow.**

## Draft rules

**T1. Voluntary, staged joining.**
1. A region joins by referendum.
2. Joining has three stages:
    - **observer:** shares data and builds the safeguard institutions of Articles 13–17;
    - **associate:** receives needs-based transfers and adopts the 30-hour week;
    - **full member:** adopts the U and the full rules.
3. Each stage has published entry criteria.

*Evidence:* the EU grew from 6 to 27 members through staged, rule-based accession. Net transfers of 1.9–4.0% of recipient output cost donors only 0.3–0.4% of theirs.

**T2. Wages and prices: no single "political" exchange rate.**
1. At full membership, wages move directly onto the UNIRA scale (5,000 U base × multiplier).
2. Prices of essentials are set from the work and resources they embody (V6.4), the same everywhere.
3. Living standards are therefore set by physical allocation by need, not by an exchange rate.

*Evidence:* German monetary union converted wages and prices 1:1 at a political rate. Within months East German output fell to about half the 1989 level and more than 3 million jobs were lost. UNIRA avoids converting a whole economy at one invented rate.

**T3. Savings converted at "basket parity", small savings protected, cap phased in over 10 years (author decision 2026-11-03).**
1. Existing savings convert to U so that they buy the same essential basket locally (food, housing, energy) after the change as before.
2. Savings up to the money cap convert in full and stay with their owner.
3. **Savings above the cap are transferred directly to the One Earth entity** (author decision; rule 18).
4. The cap phases in over **10 years**: it starts high and falls each year to its steady level (about 1.4 years of base salary).
5. **Homes are not money and are never transferred** (T4).
6. **Anti-flight rule:** the cap applies to wealth held on the day a region votes to join. Transfers abroad after the vote count as held.

*Risk noted:* direct transfer is legally and politically harder than compensation in bonds. Wealthy holders may try to move wealth out before a vote (France lost 843 wealthy taxpayers in 2006; Norway at least 30 in 2022). The anti-flight rule and the 10-year phase-in reduce this risk but do not remove it.

*Evidence:* Germany protected small savings at 1:1 (up to 2,000–6,000 marks by age) and converted the rest at 2:1. Taiwan compensated landowners with 70% bonds and 30% shares, which worked. Japan paid in money that inflation eroded (under 1,000 yen per unit against a market value of about 20,000), which was unjust.

**T4. Homes are never seized.**
1. Homes people live in are kept.
2. The two-home maximum (rule 11) applies to new purchases.
3. Homes beyond two may be sold to the regional pool at the fixed price within a transition period (e.g. 10 years), paid in U or bonds, or passed on under P1.
4. Mortgages convert to zero-interest U credit at basket parity, repaid from salary.

*Evidence:* Iceland (2014) and Hungary (2014) converted or reduced household mortgages without systemic collapse.

**T5. Enterprises: compensation, not restitution.**
1. Enterprises become cooperative or public enterprises under UNIRA rules: owner pay capped at 5× base, and surplus to the region.
2. Owners receive their share in U, under the same money-cap rules as savings (T3). Any excess goes to the One Earth entity over the 10-year phase-in.
3. Old property claims from past regimes are settled by compensation, never by giving property back.

*Evidence:* Germany's 1990 "restitution before compensation" principle tied up property and slowed investment. The Treuhand privatisation agency closed with a DM 256 bn deficit.

**T6. No public debts (author decision 2026-11-03).**
1. At full membership, **all public debts of member regions are cancelled.** Inside one world entity, debts between regions would be the entity owing money to itself.
2. **Ordinary savers and pensioners are protected.** Government bonds held by households, pension funds and banks on behalf of savers are treated as those people's savings under T3: kept up to the money cap, the rest to the One Earth entity. Pension promises are replaced by UNIRA's needs-based retirement income (rule 15).
3. **Debts owed to creditors outside UNIRA** are paid by the One Earth entity on a negotiated schedule until the creditors' regions join. This avoids asset seizures and trade blockades against new members. When the whole world has joined, no public debt remains anywhere.

*Evidence:* debt relief for heavily indebted poor countries (USD 76 bn + 43 bn) let them spend 7.3% of output on poverty reduction against 1.9% on debt service. UNCTAD reports that about 3.3 billion people live in countries that spend more on interest than on health or education (REPORTED_NEEDS_RECHECK). Unilateral defaults on outside creditors have historically triggered litigation and asset seizures, which is why external debts are honoured until creditors join.

**T7. Right to leave, and the money cap.**
1. A region may leave by democratic decision, with a negotiated settlement.
2. Every person has the right to emigrate.
3. A person who emigrates keeps their money up to the cap. Wealth above the cap has already been transferred under T3. (Author decision 2026-11-03: the right to leave is confirmed.)

*Evidence:* wealth taxes leak when the wealthy can move their wealth out: France lost 843 wealthy taxpayers in 2006 (net €2.8 bn), and Norway saw at least 30 leave in 2022. A bond schedule protects the cap without trapping people.

**T8. Protect production during the change.**
1. New members keep their productive capacity running through transitional support from the union.
2. Trade with non-member regions continues at negotiated prices.

*Evidence:* in East Germany only 8% of workers were in firms that could cover their costs after the 1990 conversion. The lesson is to protect production, not let a currency shock destroy it.

## Author decisions (2026-11-03)
1. Money cap phase-in: **10 years**.
2. Savings above the cap: **transferred directly to the One Earth entity**.
3. Regions may leave: **yes**, by democratic vote.
4. Energy, travel and data are **always metered per unit** (Article 21).
5. **No public debts:** all member regions' public debts are cancelled; savers and pensioners are protected; outside creditors are paid on a schedule until they join (T6).

## Distribution inside rich regions (V7.4, `v74/distribution`)
National averages hide who gains. At the **lowest** UNIRA salary (base worker saving the maximum 50%), a person consumes about 86% of today's average. By Eurostat 2024 income deciles, **half of the population of France, Germany, Italy, Spain and the EU27 is already better off at that level** (40% in Poland). **The poorest tenth gains +146% to +258%.** Free health care, education and guaranteed housing come on top and are not counted. Fixed prices also end household price shocks such as the 2022 energy-price crisis.
