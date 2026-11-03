# UNIRA ROADMAP — FROM V6.1 TO CREDIBLE EMPIRICAL TESTS

## Phase 0: handover and reproducibility (immediate)
- Inventory all historical files; verify scripts actually execute and outputs reproduce; reconcile contradictory version claims.
- Define canonical Git repository, license, data dictionary, model contract, scenario YAML/JSON, tests and CI.
- Audit primary-source URLs, year/geography definitions, citations and source licensing.

## Phase 1: V6.2 France sector hours and output (highest priority)
- Retrieve official INSEE/Eurostat total hours worked by industry for all employed people, employees/self-employed, part-time/full-time, matched with value added, gross output, workforce and occupation/skill mix.
- Build year-aligned sectors and full-time-equivalent definitions; identify baseline actual effective hours and 30h annual equivalents by sector.
- Report arithmetic productivity requirements with confidence/measurement limitations; account for recruitment, automation, reduced unnecessary output, essential-service coverage and transition costs.
- Deliver source-linked tidy CSVs, validation tests, reproducible Python and a clearly bounded report.

## Phase 2: V6.3–V6.5 France physical supply-use and needs
- Align INSEE/Eurostat supply-use and input-output tables with RTE energy balances, ADEME material/carbon datasets, agriculture, health and housing indicators.
- Define comfort baskets with measurable housing size/quality, diet/nutrition, energy, healthcare, mobility and time use; consult normative standards and household preference evidence.
- Convert sector monetary tables to physically meaningful commodities where possible, explicitly recording non-convertible service outputs and uncertainty.

## Phase 3: V6.6–V6.8 integrated comparison
- Run (A) observed economy, (B) reform counterfactual, (C) UNIRA under matched assets/skills/demographics/climate shocks.
- Enforce binding 30h labour and investment lead times; implement scarcity prioritisation and accessibility/consent constraints.
- Couple physical model to reconciled monetary accounts; test 5,000 U purchasing power, 25,000 U salary cap, 1,000 U child benefits with 15,000 U means-test, disability guarantee, essential public services, investment and public funds.
- Evaluate sensitivity to productivity, behaviour, resource quality, transport, migration, climate, credit constraints and public governance.

## Phase 4: V6.9–V7.2 external validity and global extension
- Extend France pilot to Paris metro housing/energy/transport and additional national cases; London, NYC, Tokyo, Cairo metropolitan studies with harmonised definitions.
- Global multiregional IO (OECD ICIO/EXIOBASE where licensing permits), FAO/ILO/IEA/World Bank/UN and trade/logistics data.
- Examine global North/South equity, skills migration, resource extraction externalities, land/indigenous rights, resilience and political transition.

## Phase 5: independent validation and publication
- Pre-register hypotheses and falsification thresholds; compare against strong reformed-market baselines.
- External economists, statisticians, environmental scientists, governance scholars and labour specialists review assumptions/code.
- Publish methods, reproducible code/data permissions, uncertainty, failure cases, working paper and eventually book *UNIRA: One Humanity, One Future*.

## Five parallel workstreams and integration contract
A. **Labour/productivity**: France sector hours, staffing, skills, 30h transitions. Output `labour_sector_year.csv`.
B. **Physical production**: energy, materials, supply-use, inventories, maintenance. Output `physical_flows.csv`.
C. **Needs/rights/environment**: comfort standards, household demand, housing matching, emissions and water. Output `needs_and_constraints.csv`.
D. **Monetary/SFC**: wages, benefits, enterprise reserves, public fund, monetary authority, prices, assets/liabilities. Output `transaction_flows.csv` and `balance_sheets.csv`.
E. **Independent audit**: source verification, test suite, scenario adversarial checks, counterfactual fairness. Output `audit_findings.md` and machine-readable checks.

**Integration rule:** Each workstream must declare geographic boundary, year, units, source, assumptions, uncertainty and API schema. Parallelism is a development workflow; there is no evidence of independent background agents having been launched in the earlier ChatGPT sessions.

## Near-term success criteria
- Reproducible V6.2 dataset with all-worker sector hours (not full-time-only extrapolation).
- Zero unexplained physical or monetary accounting residuals within documented tolerance.
- Explicit unmet needs under shocks; no silent 'success' if guarantees are underdelivered.
- UNIRA advantage, if any, must survive same-resource comparison with meaningful reformed baseline and sensitivity analysis.
