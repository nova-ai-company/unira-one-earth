# UNIRA V8.2 — point 1: producing what people want without price signals

**The problem:** for essentials, UNIRA has a needs formula (Article 10a). For ordinary goods (clothes, furniture, bicycles, books, hobby goods), fixed prices remove the price signal that tells producers what people want. This is the classic critique of planned economies:
- Hayek (1945) argued that knowledge is dispersed, and that prices are how it is communicated;
- Kornai (1980) described the shortage economy, with its queues, forced substitution and hoarding;
- Weitzman (1980) described the "ratchet" of plans built on last year's plan.

**Test:** `simulate.py`, a stylised world identical for every regime:
- 120 products over 20 years, monthly;
- demand shifts with trends, seasons, fashion booms and random shocks;
- products die and new ones arrive;
- capacity can move only 15% a month;
- every regime has the same labour hours;
- 5 seeds.

All parameters are synthetic (`config.json`).

| regime | wishes served at once | within 3 months | lost | waste (of production) | excluded |
|---|---|---|---|---|---|
| market, flexible prices | 71% | 71% | 10% | 5.5% | **19% of wishes priced out, 98% of them in the poorer half**; prices move 11% a month |
| Soviet-style annual plan with ratchet | 25% | 52% | **47%** | 7.2% | long queues for everyone; only 52% of labour hours used |
| **UNIRA signals** (stock + waiting lists + forecasts) | **70%** | **96%** | **3.8%** | **2.8%** | nobody priced out; average wait 0.6 months |
| UNIRA with sales only (no waiting lists) | 92% | 92% | 7.6% | 3.0% | nobody priced out |

**Stock target** (UNIRA): a bigger stock means shorter waits but more waste.

| stock target (× recent forecast error) | stock held | served at once | lost | waste |
|---|---|---|---|---|
| 1.5 | 0.3 months | 58% | 4.2% | 2.1% |
| 3 | 0.5 months | 64% | 3.9% | 2.4% |
| **5 (chosen)** | **0.7 months** | **70%** | **3.8%** | **2.8%** |
| 8 | 1.1 months | 73% | 3.8% | 3.5% |

## Findings

1. **The Soviet failure is reproduced.** A plan revised once a year from last year's plan loses almost half of what people want and wastes more than any other regime.
2. **UNIRA's signals solve most of the problem without prices.** Monthly production follows revealed demand: sales plus orders on waiting lists. A forecast and a stock sized from measured error cover 96% of wishes within 3 months, and only 3.8% are lost. That is less than the market (10% lost) and far less than the plan (47%). Waste is half the market's.
3. **The price of this is waiting, not exclusion.** UNIRA serves about the same share at once as the market (70% vs 71%). The rest wait about 2–3 weeks on average. In the market, 19% of wishes are never served because the price rises, almost all of them among the poorer half.
4. **Waiting lists matter.** Without them, demand hidden by stockouts goes unseen, and the share lost doubles (3.8% → 7.6%). In exchange, more is served at once, because production is then aimed only at visible sales. Orders kept for up to 3 months are the information prices would otherwise give.
5. **Speed matters more than cleverness.** The plan fails mainly because it reacts once a year and builds on its own past targets. UNIRA reacts every month to what people actually ask for.

## Rule supported (proposed Article 10b)

Production of ordinary goods follows published, revealed demand:
- what people buy, plus what they order when a product is out of stock;
- forecasts updated every month;
- stock targets sized from measured forecast error.

There is no yearly ratchet, and producers' targets are never raised for doing well (Article 3d.5).

## Limitations

- **The world is stylised:** no real product data, and synthetic parameters, including the elasticity of market demand and the speed of capacity change.
- **Variety and quality are not modelled.** Fixed prices may reduce the range of designs, which Article 3d.7 (people choose between teams' designs) is meant to address.
- **Gaming is not modelled:** fake orders and hoarding orders. Orders should require a commitment (a deposit, refunded if the product never comes).
- The market regime is simple (price adjustment with capacity lags). Real markets also use forecasts and stock signals; the main difference tested here is who gets excluded.
- **Real test:** the pilot (v80) and later the first member regions.
