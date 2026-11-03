# UNIRA V5.4 — Physical-resource accounting foundation
Date: 2026-11-03. Status: reproducible **synthetic demonstration**, not an empirical comparison.

## Why this release exists
Contemporary euro prices cannot simply be converted to UNIRA currency: financing, ownership, labour organisation, taxes and margins change, while physical scarcity remains. Model resource quantities first; add institution-specific financial accounting later.

## Three deliberately hypothetical cases
A: current-style 20 repair / 30 renovation / 50 new homes; B: reformed 25 / 45 / 30; C: UNIRA stock-first 35 / 45 / 20. Each provides 100 homes. Per-home inputs are arbitrary teaching coefficients and not city or construction-sector estimates. Each case has 20 available workers; A and B use 1,800 hours/worker-year, C uses 1,500 (30 hours × 50 weeks). The 1,800-hour assumption is illustrative, not an observed average.

| Case | Labour hours | Cement tonnes | Embodied tCO2e | New homes |
|---|---:|---:|---:|---:|
| A | 25,700 | 117 | 670 | 50 |
| B | 22,400 | 85 | 462.5 | 30 |
| C | 19,700 | 66 | 347.5 | 20 |

The apparently favourable UNIRA result is **designed into intervention mix assumptions** and is NOT evidence that the system causes those improvements. A and B are not empirical baselines, and C is not optimised. The model excludes operational energy, lifecycle maintenance, land, transport, construction supply chains, housing quality, location, consent, skills, supply chain timing and monetary equilibrium. A physically feasible scenario is not proof of social, economic or political feasibility.

## Accounting architecture
1. **Demand ledger:** households needing adequate housing, by location, size, accessibility and preferences.
2. **Stock ledger:** actual habitable buildings, condition, occupancy, legal/consent status, suitability.
3. **Bill of physical inputs:** labour hours by trade, tonnes of materials, MWh, water, logistics and embodied emissions; separate operational impacts over lifecycle.
4. **Capacity ledger:** trained workers by skill, available hours, regional material and energy availability, lead times, competing demands from food/healthcare/transport.
5. **Financial ledger:** U wage payments, public funding, investment, reserves, prices, rationing risks and inflation controls. Do not confuse nominal wages with physical output.
6. **Comparators:** current policy, ambitious reform of current policy, UNIRA; same needs and rights constraints.

## Model behaviour
`python model.py` produces `results.json` and `results.csv`. `python -m unittest -v` runs seven tests. Feasibility checks total home counts, aggregate labour availability, cement, steel, electricity and water. The `physical_cost_index` is an **unweighted capacity-utilisation average**, not a monetary cost, welfare index, optimality measure or scientifically validated environmental metric.

## Next steps: V5.5
Obtain official physical construction bills of materials, embodied-carbon declarations, and region-specific labour productivity; distinguish energy-upgrade-only from full renovation. Add household-building matching and trade-specific workforce constraints. Add annual capital replacement and operating energy. Then develop U-currency supply-demand consistency with 5,000 U/month base wages, 25,000 U cap, 30-hour weeks, and 1,000 U conditional child benefits. Stress-test shortages and regional trade. Finally compare counterfactuals under equal rights and comfort constraints.

## Sources and data policy
No empirical numeric coefficients were imported into V5.4. Every number in `scenarios.json` is an illustrative assumption. Future candidate authoritative data sources: Eurostat construction statistics (https://ec.europa.eu/eurostat), France INSEE (https://www.insee.fr), ADEME environmental product data (https://www.inies.fr), ILOSTAT (https://ilostat.ilo.org), and the IEA (https://www.iea.org). Their listing does not imply this version downloaded or calibrated against them.
