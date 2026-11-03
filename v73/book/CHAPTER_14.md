# Chapter 14 — Guarding against power

*Second draft, 3 November 2026, updated with V7.8–V7.9. Every figure comes from the UNIRA research (V6.9, V7.0, V7.2, V7.5, V7.8 and V7.9) and the draft Constitution of One Earth, and is listed in the notes at the end of the chapter.*

---

Imagine a nurse in a small river town. On a quiet afternoon they open the Public Allocation Register on their phone. It is free, and anyone can read it.

The register says the town's clinic received two vaccine fridges this year. It says when, from where, and on which needs data. The nurse walks into the storeroom. There is one fridge.

So they write a complaint. The law says they must receive a reasoned answer within **90 days**. The law also says nobody may punish them for asking. A few weeks later, an auditor arrives without warning.

This scene is imagined, a composite of many places. But the rules in it are real articles of the draft constitution. This chapter explains why they are there. It starts from an uncomfortable question: what if the people who share the world's resources get it wrong, or steal?

## A good rule is not enough

Chapter 13 showed that directing new resources by need closes the world's gaps much faster than a market economy. But that test assumed a perfect allocator. It knew every region's needs exactly, on time, and every solar panel reached its roof.

No real institution works like that. The research looked at how real allocators fail today and found four main problems:
- **measurement error:** needs are counted wrongly;
- **data lag:** needs are counted late;
- **misreporting:** some regions exaggerate their needs to receive more;
- **leakage:** some resources never reach the people they were meant for.

Each one has been measured somewhere in the world. The research collected **44** sourced observations of them.

## A closer look: how the evidence was checked

Numbers about corruption travel fast and get rounder as they go. So the research used a strict rule.

A number counted as verified only if it appeared in text actually fetched on 3 November 2026. That could be a study's abstract, an official page or a report. Some widely quoted figures could not be seen in such text. They were marked as unverified and were not used to set the model.

This cost the research some striking numbers. A famous estimate of missing spending in Indonesia was left out. So was a well-known effect of biometric smartcards in India, and a popular "10–25%" figure for corruption losses. They may be right. But they could not be checked, so they do not appear in this chapter.

## Counting wrongly, counting late

Take counting first. South Africa's 2011 census missed **14.6%** of people. By province, the share missed ranged from **10.0% to 18.6%**. The national total can be corrected afterwards. The gap between provinces is harder to fix, and that is what would steer an allocator wrongly.

World poverty counts move too. A change in price data in 2005 added about **400 million** people to the count of the poor. A later revision removed **46 million**. The poorest places are often the least measured. Between 2002 and 2011, **57 of 155** countries had at most one poverty estimate.

Then there is delay. Poverty data usually reach users about **2 years** after they are collected. Building takes time as well. New renewable plants take **1 to 5 years** to build, and new power lines **5 to 15 years**. So an allocator is always steering by a picture of the past.

One finding here is quietly important. Errors in judging single *households* are far larger than errors in judging whole *regions*. In nine African countries, a common household test classed **80%** of poor households as not poor. It classed **40%** of non-poor households as poor. Brazil's Bolsa Família in 2004 missed **59%** of those it meant to reach, and included **49%** it did not mean to. Yet it ranks among the most progressive programmes there are.

UNIRA's allocator does not judge households. It directs new capacity to **regions**, by measured need and population. People's core guarantees, from health care to a home, are written as rights in Article 6. So the allocator works with the smaller kind of error.

## Regions that exaggerate

When resources follow reported needs, a region has a reason to inflate its figures. This is not a fear invented for this book. It has happened.

In China, local statistics inflated growth by about **1.7 percentage points a year** between 2008 and 2016. National corrections averaged **5%** of output. One province, Liaoning, admitted that its fiscal revenue had been exaggerated by about **20%** between 2011 and 2014. Its output was later revised down by more than 20%.

In Brazil, towns receive federal grants according to population brackets. In 2010, **192 of 3,565** towns were in the wrong bracket. That misdirected over **US$100 million** a year. Near the first threshold, **17–42%** of towns sat just above it, by only **62 to 241** people. The pattern grew worse from one census to the next.

The Brazilian case shows how small the cheating can be. A town needs only a few hundred extra residents on paper. That is about **0.5–2.4%** of its population. Nobody would notice by walking down the street.

## Resources that disappear

Leakage is the oldest problem of all. The research collected the best measured cases.

| Where | What leaked | How much |
| --- | --- | --- |
| Uganda, 1991–95 | School grants that never reached schools | **87%** |
| India, 2004–05 | Subsidised grain that never reached families | **54%** |
| India, 2011–12 | The same programme | **41.7%** |
| India, 2022–24 | The same programme, after reforms | **8.8–28%** |
| Brazil | Funds diverted in audited towns | **30%** |
| Aid-dependent countries | Aid moved offshore by elites | **7.5%** |
| European Union, 2023 | Cohesion spending found irregular (not fraud) | **9.3%** |
| European Union, 2023 | The whole EU budget, irregular (not fraud) | **5.6%** |

Two lessons sit in this table. Leakage can be enormous where nobody checks. And it can fall far: India cut it by **30 to 45 points** in about a decade. Yet even the European Union, with strong institutions, stays above **5%**.

## The stress test

The research then put all four failures into the UNIRA model of the 30-year world transition. The allocator no longer saw true needs. It saw noisy, late figures, some of them inflated. Part of what it sent simply vanished. Each scenario ran **30 times** with random errors.

## A closer look: how the stress test worked

The model makes one simple change to UNIRA's allocator. It decides on *perceived* needs, not true ones.

**Measurement error.** Each year, each region's need is seen with a random error. The error is as likely to be too high as too low, so it does not bias the total. In the central case it is about **15%**.

**Data lag.** The allocator sees needs as they were some years ago. In the central case, **2 years**.

**Exaggeration.** A share of regions inflate their reported need. Each year, an audit catches each cheating region with a **50%** chance. That rate is an assumption.

**Leakage.** A share of all new capacity reaches no one.

One more rule makes the test harsh. Anything sent to a region beyond its true need is counted as wasted. It is not passed on.

The values came from the evidence above, in three settings:

| Failure | Low | Central | High |
| --- | --- | --- | --- |
| Measurement error | 5% | **15%** | 30% |
| Data lag | 1 year | **2 years** | 5 years |
| Leakage, no safeguards | 10% | **25%** | 45% |
| Leakage, strong safeguards | 3% | **8%** | 15% |
| Share of regions exaggerating | 10% | **25%** | 45% |
| How much they exaggerate | 2% | **7%** | 20% |

The research is candid about its confidence. It is medium for leakage and lag. It is low to medium for measurement error and exaggeration. Those two are judgement calls, anchored on the best clues available.

## The results

| How the One Earth allocator works | Energy gap closed, year 15 | Health, year 15 | Homes, year 30 | Everyone at 40 GJ |
| --- | --- | --- | --- | --- |
| Perfectly | 60% | 38% | 50% | year 27 |
| Like the best governance observed | 57% | 36% | 46% | year 29 |
| **With strong safeguards** | **52%** | **34%** | **40%** | **year 29** |
| **With typical failures, no safeguards** | **36%** | **24%** | **19%** | not in 30 years |
| Like the worst governance observed | 15% | 12% | −9% | not in 30 years |
| Very cooperative market world | 14% | 4% | 10% | not in 30 years |
| Reformed market world | −14% | −4% | −21% | not in 30 years |

The 30 random runs barely differed, by about **1 point**, because errors average out across **179** regions.

Even with typical failures and no safeguards, needs-first allocation beats the most cooperative market world on all three needs. With strong safeguards it keeps most of the ideal result. Everyone reaches a comfortable **40 GJ** of energy by year 29, instead of never.

The research puts it simply: **safeguards are worth about as much as the allocation rule itself.**

Under the worst governance ever observed, UNIRA loses its lead on energy and homes. It still leads on health, thanks to the training programme and the soldiers who volunteer for care work. That bottom row matters. It shows the idea can fail, and roughly where.

## An illustration: errors cancel, theft does not

Here is an imagined way to see why the four failures are so different.

Picture a teacher marking a hundred exams in a hurry. Some marks come out a little high, some a little low. Over the whole class, the average is about right. That is measurement error. Across 179 regions, it behaves the same way.

Now picture a pupil who copies answers. The teacher may not notice this year. But spot checks happen every year, and copying is eventually caught. That is exaggeration, with audits.

Finally, picture someone stealing a third of the exam papers before they are marked. No averaging brings them back. Those pupils simply get no mark. That is leakage.

## Why leakage decides everything

Of the four failures, one does most of the damage. Counting errors are random. Some regions are overcounted, some undercounted, and across many regions the mistakes partly cancel out. Exaggeration is caught by audits.

Leakage is different. A stolen panel is simply gone. It does not average out, and no later audit brings back the years it was missing.

From this the research draws a clear line. **If One Earth cannot keep leakage well below about 45%, and data lags under about 5 years, needs-first allocation is no better than a cooperative market.** The constitution writes that line into its own text.

## Eight safeguards, each with a reason

The draft constitution answers each failure with a rule. Most of them come straight from the evidence.

| Safeguard | Article | What the evidence shows |
| --- | --- | --- |
| Public Allocation Register, within **30 days** | 33 | Uganda: capture fell from about 80% to **under 20%** after newspapers published school grants |
| Direct digital delivery, verified on site | 34 | India (Bihar): spending losses fell **24%**, then **19%** at national scale |
| Community monitoring and protected whistleblowers | 35 | Uganda health: under-five deaths fell **33%** |
| Random audits of every region, every year | 36 | Indonesia: missing funds down **8 points**; Brazil: corruption down **7.9%**, **12.7%** with repeat audits |
| Needs data less than **1 year** old | 37 | Typical lag today is about **2 years** |
| Rules against capture | 26, 26a, 30, 30a | Built from the design, not from a single study |
| Correction without punishing people | 38 | Built from the design |
| A built-in test of the whole system | 39 | Thresholds from the stress test |

Some of these need a few more words.

**The register.** Every allocation is published, saying what, where, how much, why and on which data. Personal data are never published. Sunlight works because it turns millions of people into checkers. The honest caveat: part of Uganda's fall came at the same time as wider reforms.

**Digital delivery.** Payments go straight, in U, to whoever delivers the work. Delivery is checked on site and by remote sensing before it counts as done. In India this cut losses with no loss of jobs. But it also slowed payments. A safeguard can add delay, about **half a year to a year** in that case.

**Community monitoring.** Every community may watch what it was promised. Anyone may complain and get an answer within 90 days. Here too the evidence is mixed. In Indonesia, grassroots monitoring alone did little, because everyone waited for someone else to act. That is why UNIRA pairs it with professional audits, not instead of them.

**Audits.** The Audit Authority checks every region, every year, at random and without notice. In Indonesia, raising the chance of an audit from **4%** to **100%** cut missing spending by 8 points. In Brazil, audits also had effects beyond the towns audited, through the media: **7.5–10.4%**. UNIRA's audit budget is fixed by the constitution as a share of what is allocated. So no government can starve it of money.

**Data.** The Statistical Office measures needs at least once a year, with the uncertainty stated. Data are checked against independent sources, such as censuses, satellite data and sample surveys. No region may change its methods alone.

**Rules against capture.** The Allocation Authority applies a public formula and has no power to favour any region. Changing the formula needs two-thirds of the Assembly, a double majority of regions, the Scientific Council's opinion and a citizens' assembly, and takes effect only after the next election (Article 26a). And no one may decide an allocation to a region where they or their family hold an interest.

**Correction without punishing people.** Misallocated resources are recovered and sent where they belong. A region caught misreporting loses priority for extra, discretionary allocations. It never loses its people's rights. A child should not lose a clinic because an official lied.

**The built-in test.** World leakage and data age are published every year. Then two alarms apply:
- if leakage passes **25%**, or data are more than **2 years** old, the Assembly must review the allocation system within a year;
- if leakage passes **45%**, or data are older than **5 years**, for **3 years** running, the system must be reformed by law.

This constitution says, in advance, how its own central idea could be shown wrong. It also says what must happen then.

## A closer look: the finer triggers

An earlier, longer draft of these safeguards proposed sharper triggers for each article. They are not yet in the constitution's short text. They show how each rule could be made to bite:
- an allocation still missing from the register after **60 days** would be void until published;
- leakage above **15%** in any region for **2 years** running would start an independent review there;
- a project whose delivery cannot be verified within **12 months** would be listed as undelivered;
- needs data more than **2 years** old would flag that region's allocations for checking;
- officials found diverting resources would lose office and face independent courts;
- the allocation rule itself would be reviewed in public every **5 years**.

These are proposals. The research is explicit that every threshold "may be set differently by democratic decision".

## An illustration: a region that cheats

Imagine a regional statistics office under pressure. A few officials decide to round up the number of people living in crowded homes. More homes will come their way.

For a year or two, it works. Then a random audit compares their figures with a satellite survey and a sample count. The gap is too large to be an honest error.

What happens next is set out in the constitution. The extra homes still under construction are reassigned to where they are truly needed. The region loses priority for extra, discretionary allocations until audits confirm honest reporting. The officials face the courts.

What does *not* happen matters just as much. No family in that region loses its home, its health care, its children's school or its income. Those are rights under Article 6, and Article 9 says no sanction may reduce them. The officials lied. The people did not.

## What safeguards cost

Safeguards are not free, and the research says so.

Checking takes time. In Bihar, direct digital payment cut losses but slowed payments. The research suggests modelling about **half a year to a year** of extra delay as a cost of safeguards.

Checking takes people. Auditors, statisticians and inspectors must be trained and paid. Their hours are part of the work of running UNIRA's own institutions, which the research admits it has not yet counted.

And checking has limits. Even the European Union stays above 5% irregular spending. The aim is not zero leakage. The aim, on the evidence, is to stay well below the levels where needs-first allocation stops paying off.

## Power divided among many hands

Leakage is one danger. Another is older: people who gain power and keep it.

The first draft of the constitution divided public power into six parts: making law, carrying it out, allocating resources, measuring needs, auditing and judging. The stress test described below showed that this left out the three most dangerous powers of all: **arms, money and science**. Article 22a adds them. There are now nine powers, each in a separate body.

| Power | Body | How it is chosen |
| --- | --- | --- |
| Law | Assembly of the Peoples; Council of Regions | Elected directly; chosen by the regions |
| Executive | Coordination Council | Elected by the Assembly |
| Allocation | Allocation Authority | Elected by the Council of Regions, by double majority |
| Money | Monetary Authority | Appointed by the Court from a Scientific Council shortlist |
| Armed force | Peace Force, led by a Command Board | Board elected by the Council of Regions, from a list checked by the Inspector-General |
| Measuring needs | Statistical Office | Head elected by two-thirds of the Assembly, from a shortlist; one 7-year term |
| Auditing | Audit Authority | Board drawn by lot from auditors nominated by the regions, confirmed by the Assembly |
| Science | Scientific Council | Drawn by lot from scientists nominated by regional academies |
| Judging | Court | Council of Regions, from candidates of an independent commission |

No person may sit in two of these bodies, or move from one to another within **3 years**. No body chooses the people who audit or judge it. And each body's budget is fixed by law, so it cannot be starved quietly. The point is simple: **no body holds arms, money and allocation together.**

Time is limited too:
- the executive's seven to fifteen coordinators serve a **single 5-year term**;
- the chair rotates every year, and no region may hold it twice in a row;
- executive, allocation, monetary, command and judicial offices are held for **one term only**;
- no one may hold One Earth office for more than **10 years** in a lifetime;
- a change to terms or pay never benefits anyone already in office (Article 30a).

Money is limited as well. Office-holders are paid on the same 1–5× scale as everyone else, with no other income. They declare their assets, and their household's, every year in office and for five years after. They are under the same money cap as everyone else. For five years after leaving, they may not lobby the body they served in, or work for a region or enterprise they decided about. No close relative may serve in the same body at the same time.

Regions are protected from the centre. Each region has its own elected government and parliament. One Earth cannot dissolve them, except by a ruling of the Court for a grave breach of rights. There are no permanent seats, no vetoes, and no privileges of size, wealth or history.

**Allocation without favour.** Article 26a ties the Allocation Authority to the formula of Chapter 5. No allocation may depend on how a region votes or on loyalty to anyone. Each year the register shows, for every region, what the formula gives and what was actually allocated. A gap of more than 2% must be explained within 30 days, and anyone may take it to the Court. Discretionary allocations are capped at 2% of the total.

**A machine that checks.** Chapter 5 showed that errors in data and forecasts cost at most about **1%** of progress, while each point of leakage costs about one point of energy progress and 1.2 points of housing progress. So the AI's main job is integrity: comparing deliveries with needs and metered use, flagging anomalies for audit, and sizing reserves. Whether it can really cut leakage is still to be tested in pilots. And Article 3c checks the checker: signed, published models that may never score or select people.

## Voting that no giant and no clique can control

Chapter 5 described the two chambers and tested them. In brief: Assembly seats follow the square root of each region's population (the Penrose rule), so India and China hold about **4.4%** each instead of **16–17%**, and no region may hold more than **5%**. A law needs at least **55%** of regions representing at least **65%** of the population, counted by square root. Counted raw, India and China together, **35.2%** of humanity, could block any world law alone. Counted by square root, blocking takes at least **21** regions, and passing a law at least **120 of 217**.

Changing the constitution is harder still: **two-thirds** of the Assembly, **65%** of regions representing **65%** of the population, and a world referendum won by a majority of voters and in a majority of regions. Changes to the institutions need two Assembly votes with an election between them (Article 42b). And a protected core can never be changed: the rights of Article 6, elections on fixed dates, term limits, the independence of the Court, the limits on the Peace Force and on emergencies, and the right to leave (Article 42a).

## Who guards the only army?

UNIRA abolishes war, so only One Earth may hold arms. That creates the most dangerous power of all. Whoever controls the only armed force could rule everyone. Chapter 12 described the Peace Force in detail. Here are its locks.

| Control | Rule |
| --- | --- |
| Who may send it | To enforce a Court ruling: the ruling **and** a double majority of regions. Any other use: a majority of the Assembly **and** a double majority of regions, reviewed by the Court within 7 days |
| Emergencies | Under an immediate threat to life, the Command Board may act for at most **72 hours**, only at the request of a region or the Court, and never renewed |
| No national army inside it | No region provides more than **5%** of members or commanders |
| No local loyalty | Commanders serve at most **3 years** at each level; members never serve in their own region; every unit of more than 100 members mixes at least ten regions |
| Size | Never more than **1,000,000** members, about 12 per 100,000 people; planned about **500,000** |
| Money | Never more than **0.15%** of world output; planned about **0.05%** |
| Oversight | An Inspector-General appointed by the Court reports publicly; anyone harmed may go to the Court |
| Forbidden uses | Never against peaceful protest, a lawful election or a region's democratic institutions |

One detail shows how carefully this was thought through. Research on new armies finds they are most at risk of coups while they are being built. So the Force grows step by step, with members from all regions from the first day. And the Inspector-General is in place before the first unit forms.

Regions keep civilian police for everyday crime, trained to One Earth's human-rights standards and equipped only for policing.

## Testing the Constitution against its own abuse

The research then attacked the Constitution itself. It imagined thirteen ways to seize power: a popular leader who wants to stay, a general planning a coup, a bloc of big regions capturing the Assembly, a fake emergency, money and data turned into a tool of control, a packed Court, a region stopped by force from leaving.

The evidence on how freedom is actually lost is sobering. Today about **74%** of the world's people live under autocracies, and **44** countries are sliding toward autocracy (V-Dem 2026). At least **a third** of presidents who reached their term limit tried to stay, and two-thirds of those tried by changing the constitution. Democracies are **75%** more likely to erode during a state of emergency.

So the danger is rarely tanks in the street. It is law used against freedom. The first draft was strong on fair voting and a mixed Peace Force, but it had five open doors: no rule on emergencies, accounts that could be frozen without a judge, an amendment rule that was not protected, a Court that could be packed, and no procedure for leaving.

Seventeen new articles close them, with amendments to Article 5a. Here they are, grouped by the door each one shuts.

| Danger | What the constitution now says | Articles |
| --- | --- | --- |
| A general seizes the army | No commander-in-chief, only a Command Board of five from five continents. Heavy weapons are spread across many depots and need **three keys**, held by people from three different regions. No other armed body may exist. | 5b |
| Soldiers obey a tyrant | Every member of the Force must refuse an order that clearly breaks the constitution, and may not be punished for refusing. Obeying is no defence. | 5c |
| Censorship | No prior censorship, no shutting or slowing networks. Only a court may order specific content removed. No one controls more than a quarter of a region's news audience. | 6a |
| A fake emergency | An emergency lasts at most **30 days**; each renewal needs two-thirds of both chambers. It may never delay an election, dissolve a body or change the constitution. | 9a |
| Money and data as weapons | No account frozen and no payment data opened without a judge. Small everyday payments are private, even though there is no cash at all. | 12a |
| Captured models | Signed, published models, two independent teams, no scoring of people. | 3c |
| Money for friends | A Monetary Authority bound by a published rule, with no discretion. | 17b |
| One body holds everything | Nine powers in nine bodies, chosen in different ways. | 22a |
| Allocation as reward or punishment | Needs only; formula against actual published every year; changes slow and reviewed. | 26a |
| Staying in office | One term for key offices, 10 years in a lifetime, no rule change that benefits the holder, elections on fixed dates. | 30a |
| A packed Court | **21** judges, a third renewed every 4 years, removed only by two-thirds of judges and of regions. | 32a |
| Leaders ignore citizens | A permanent Citizens' Council of 100 drawn by lot; assemblies of at least 500 review formula changes, long emergencies and amendments. | 32b |
| Slow decay | A yearly democracy health check. If it falls two years running, extra audits, a citizens' assembly and early elections follow automatically. | 39a |
| A region held by force | A procedure to leave: referendum within 2 years, simple majority with 50% turnout, exit 2 years later, no force. | 41a |
| Amending freedom away | A protected core (rights, elections, term limits, the Court, the Force's limits, the right to leave) that no amendment may weaken. | 42a |
| Rushed amendments | Two Assembly votes with an election between them, a citizens' assembly, and none during or just after an emergency. | 42b |
| A dangerous start | The Court, the Audit Authority, the Inspector-General, the Democracy Monitor and the Citizens' Council exist before the first Force unit, the first U and the first allocation. The Force stays under **250,000** for its first 5 years. | T-7 |

After the fixes, every attack meets at least two independent barriers. But the research is honest about the limit: no text can guarantee freedom. Would-be autocrats are stopped more often by ordinary people who refuse to go along than by courts. So the design spreads power across many hands and many regions, and keeps the door to leave always open.

## What the critics say, and what the research answers

**"Who guards the guardians?"**

Nobody, in the end, except other people. That is why the design spreads checking as widely as it can. Auditors check allocators. The Court checks laws and allocations. Communities check deliveries. Anyone can read the register and complain. No single body holds the last word. Whether that holds under pressure, the model cannot say.

**"A digital currency where every sale has an invoice is a surveillance machine."**

This is a serious worry, and the constitution meets it only in part. Article 12 guarantees privacy, access without a smartphone, several independent networks, independent oversight and a right to appeal. There is no cash; if a network fails, essential needs continue and are recorded later. Personal gifts need no invoice. The register publishes amounts and places, never personal data. Article 12a adds more: anonymous everyday payments up to a limit, invoices that name the seller but not the buyer, payment data kept in the person's own region by at least three independent operators, deleted after two years, and opened only by a judge. But guarantees on paper are not the same as guarantees in practice. The technology that would deliver them is not yet built or tested.

**"A constitution is only paper."**

True. Many countries have fine constitutions and poor governance. The stress test is useful here because it does not assume the rules are obeyed. It asks what happens when they are not. Its answer: with typical failures, UNIRA still beats the best market world. Under the worst governance ever seen, it does not.

**"Your audit catch rate is invented."**

It is an assumption, and the research labels it so. A 50% chance a year of catching a cheating region has no direct measurement behind it. The good news is that exaggeration mattered much less than leakage in every run. The bad news is that nobody knows how a world audit body would really perform.

**"Building homes and power plants is far more corrupt than handing out grain."**

This may be right. Most leakage evidence comes from cash and food programmes. Construction is often more corrupt. The research names this among its next steps: testing leakage in infrastructure, not only in transfers.

**"Corrupt officials do not lose resources. They steer them to friends."**

Also fair. The model counts stolen resources simply as lost. In reality, favoured regions might receive extra, which could do more harm. This is not yet modelled.

## The limit no safeguard can fix

One case in the evidence is different from all the others.

In 2021 the global vaccine-sharing scheme, COVAX, promised **2 billion** doses. By the end of November it had delivered about **596 million**, about 30%. The failure was not in deciding who should get doses. It was in getting the doses at all.

An allocator is only as good as what it has to give. That is why this book spends so many chapters on production: energy built, nurses trained, homes raised. Fair sharing of too little is still too little.

## What the evidence says

- Real allocators count needs wrongly, count them late, are misled by exaggeration and lose resources to leakage. All four have been measured.
- Errors in judging regions are much smaller than errors in judging households. UNIRA allocates to regions and gives people rights.
- With typical failures and no safeguards, needs-first allocation still beats the most cooperative market: **36%** of the energy gap closed by year 15, against **14%**.
- With strong safeguards it keeps most of its ideal performance: **52%** against **60%**, and everyone reaches 40 GJ by year 29.
- Leakage is the decisive danger. Above about **45%**, with data lags near 5 years, the advantage disappears. The constitution's built-in test sets its alarms at **25%** and **45%**.
- Power is split nine ways (Article 22a), terms are single and short, and officials are under the money cap. The only armed force needs both a court and the regions to move, and its heavy weapons need three keys from three regions.
- After seventeen new articles, every one of thirteen attack scenarios meets at least two independent barriers. **34** of the **111** clauses tested rest directly on evidence; the exact thresholds are judgement.
- Information errors cost at most about **1%** of progress; leakage costs far more. The AI's main value is checking honesty, not forecasting.

## What we still don't know

- Most leakage evidence comes from cash and food programmes in low- and middle-income countries. Building homes and power plants may leak more, since construction is often more corrupt.
- The audit catch rate of 50% a year is an assumption, not a measurement.
- The model counts capture only as loss. In reality, stolen resources may be steered to favoured regions, which could hurt more.
- Errors were treated as independent between regions. If a whole continent were undercounted at once, the damage would be larger.
- The model does not include politics: legitimacy, anger in regions that receive less, or institutions slowly decaying over decades.
- The costs of safeguards, in delay and in staff, are noted but not fully modelled.
- How the privacy rules of Article 12a would be built into a world digital currency is not yet designed or tested.
- Whether the new power articles work. Most of their thresholds are judgement, and no constitution has tried automatic democratic brakes like Article 39a.
- An allocator is only as good as what it has to give. COVAX promised **2 billion** vaccine doses in 2021 and delivered about **596 million** by the end of November. The failure was supply, not targeting.

---

### Notes on sources
- Stress test of the One Earth allocator (model, parameters, scenarios, results, limitations): `v69/RESEARCH_NOTE.md`; model in `v69/coordination/model.py`, `v69/run.py`.
- Evidence on measurement error, household targeting, lags, misreporting, leakage, safeguard effects and costs, and the verification rule (44 sourced rows: Stats SA PES; World Bank; IEA; Reinikka & Svensson 2004; Drèze & Khera; Avis, Ferraz & Finan; Andersen, Johannesen & Rijkers 2022; European Court of Auditors; Chen et al. 2019; Olken 2007; COVAX): `v69/evidence/evidence.md`, `v69/evidence/evidence.csv`.
- Earlier draft safeguard articles with their finer triggers (Articles 13–20 of the safeguards draft): `v67/WORKING_PAPER_02.md`, appendix; `v70/RESEARCH_NOTE.md`, Part B.
- Safeguard articles (33–39), Scientific Council (3a), rights (6, 9), currency (12), separation of powers (22), Assembly (23), double majority (25), Allocation Authority (26), executive (27), terms and asset declarations (30), regions (31), Court (32), amendments (42), Peace Force (5a, with the De Bruin 2018 note): `v75/constitution/UNIRA_CONSTITUTION_DRAFT.md`.
- Separation of nine powers and how each body is chosen (22a), allocation without favour (26a), limits on office (30a), and the seventeen power articles with amendments to 5a (3c, 5b, 5c, 6a, 9a, 12a, 17b, 22a, 26a, 30a, 32a, 32b, 39a, 41a, 42a, 42b, T-7): `v75/constitution/UNIRA_CONSTITUTION_DRAFT.md`. Stress test of 13 attack scenarios and 48 evidence rows (V-Dem 2026; Versteeg et al. 2020; Lührmann & Rooney; 34 of 111 clauses evidence-supported): `v79/RESEARCH_NOTE.md` §6 and `v79/power/`. List of new articles: rule 33 in `v63/DESIGN_CLARIFICATIONS_2026-11-03.md`.
- AI and integrity (information errors at most about 1%; each point of leakage costs about 1 point of energy and 1.2 of housing progress): `v78/RESEARCH_NOTE.md` §4; `v78/outputs/information.json`.
- Seat shares and double-majority tests on 2024 populations (blocking needs at least 21 regions under square-root weights, key `double_majority_55_65_sqrt`): `v75/outputs/voting.json`; model `v75/constitution/voting.py`. The note under Article 25 of the constitution draft still says 20; the model output gives 21.
- Square-root weighting and the double majority agreed by the author: `v63/DESIGN_CLARIFICATIONS_2026-11-03.md`, items 28–29.
- Uncounted hours of UNIRA's own institutions; next research on infrastructure leakage: `v67/WORKING_PAPER_02.md`, sections 12 and 13.
