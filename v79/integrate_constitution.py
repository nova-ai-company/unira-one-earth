"""One-off merge of the V7.9 articles into the draft constitution (v75/constitution/UNIRA_CONSTITUTION_DRAFT.md).
Kept in the repository as the record of exactly what was changed. Not part of run_all (it is not idempotent).
Sources: v79/power/POWER_ARTICLES.md, v79/innovation/evidence.md, v79/housing/RESEARCH_NOTE.md, and the tested
rules of v79/allocation, v79/prices and v79/money."""
import re
from pathlib import Path

V79 = Path(__file__).resolve().parent
C = V79.parent / "v75" / "constitution" / "UNIRA_CONSTITUTION_DRAFT.md"
s = C.read_text(encoding="utf-8")


def clean(t):
    t = re.sub(r"\s*\[(E|J)[^\]]*\]", "", t)  # evidence/judgement marks stay in v79/power only
    t = re.sub(r"\(E (\d+)(?:[–-]E? ?(\d+))?\)", lambda m: "(v79/power evidence row " + m.group(1) + (f"–{m.group(2)}" if m.group(2) else "") + ")", t)
    t = re.sub(r"\(E (\d+), E (\d+)(, E (\d+))?\)", lambda m: "(v79/power evidence rows " + ", ".join(x for x in (m.group(1), m.group(2), m.group(4)) if x) + ")", t)
    return t.strip() + "\n"


def blocks(md):
    """{article label: text} for every '**Article X —' / '**T-7.' block in a draft file."""
    out = {}
    parts = re.split(r"(?m)^(?=\*\*(?:Article \w+ —|T-\d+\.))", md)
    for p in parts:
        m = re.match(r"\*\*(Article (\w+)|T-(\d+))", p)
        if m:
            body = re.split(r"(?m)^(?:---|## |### )", p)[0]
            out[m.group(2) or f"T-{m.group(3)}"] = body.strip()
    return out


def insert_after(label, text):
    """Insert `text` after the block of article `label` (before the next article, rule or heading)."""
    global s
    start = re.search(rf"(?m)^\*\*{re.escape(label)}[ .]", s)
    assert start, label
    nxt = re.compile(r"(?m)^(?:\*\*Article |\*\*T-\d|---\s*$|## |### )").search(s, start.end())
    pos = nxt.start() if nxt else len(s)
    s = s[:pos].rstrip() + "\n\n" + text.strip() + "\n\n" + s[pos:]


def replace(a, b):
    global s
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)


P = blocks((V79 / "power" / "POWER_ARTICLES.md").read_text(encoding="utf-8"))
inn = (V79 / "innovation" / "evidence.md").read_text(encoding="utf-8")
inn_art = inn[inn.index("**Article 3c — Innovation and improvement.**"):inn.index("*Evidence: V7.9 (`v79/innovation/evidence.md`)")]
inn_art = inn_art.replace("**Article 3c — Innovation and improvement.**", "**Article 3d — Innovation and improvement.**")
inn_art += "*Evidence: V7.9 (`v79/innovation/evidence.md`): public research underlies all 210 new drugs approved in the USA in 2010–16; open data raise follow-on research; unexplained pay differences cut effort. A fixed price per hour would penalise teams that save hours, so clause 5 lets them keep part of the saving. Thresholds are provisional until measured starting values exist.*\n"

# ---- Part I: models, innovation
insert_after("Article 3b", clean(P["3c"]))
insert_after("Article 3c", inn_art)

# ---- Peace Force (5a amendments, 5b, 5c)
replace("   It is never used against peaceful protest, a lawful election or a region's democratic institutions.",
        "   It is never used against peaceful citizens or protest, a lawful election or referendum, a region's democratic institutions, or a region's vote to leave One Earth (Article 41a).")
replace("""2. **Deployment:** the Coordination Council may deploy the Force only with:
    - a ruling of the Court;
    - approval by double majority of the Council of Regions (Article 25).

   In an immediate threat to life it may act for at most 72 hours, then needs both.""",
        """2. **Deployment:**
    - to enforce a ruling of the Court, the Force may be deployed with that ruling and approval by double majority of the Council of Regions;
    - every other deployment needs a majority of the Assembly of the Peoples and a double majority of the Council of Regions (Article 25); the Court reviews it within 7 days and may halt it;
    - under an immediate threat to life, the Command Board (Article 5b) may act for at most 72 hours, only at the request of a region's government or of the Court, and informs the Court at once; the 72 hours cannot be renewed.""")
replace("    - commanders rotate every 3 years;", "    - commanders serve one term of at most 3 years at each level of command and never return to the Command Board;")
insert_after("Article 5a", clean(P["5b"]))
insert_after("Article 5b", clean(P["5c"]))

# ---- Part II
insert_after("Article 6", clean(P["6a"]))
insert_after("Article 9", clean(P["9a"]))

# ---- Article 10: the tested formula
insert_after("Article 10", """**Article 10a — The allocation formula.** *(Gives the public formula of Article 10.)*
1. For each need (energy, health care, homes, food, education), each region's gap is the published target per person minus its measured level, times its population.
2. Targets take account of real differences in need, such as age, climate, disability and remoteness. Each adjustment is published with its evidence and approved by the Scientific Council.
3. **Decent for everyone first.** New capacity first closes every region's gap to the decent level. Only then does it go to the comfortable level. Within each step, it goes to the largest gaps first, in proportion to need.
4. **Where to produce.** One Earth decides where goods are produced so as to use the fewest working hours, resources and transport, while giving every region productive work.
5. The formula, its data and each year's results are published in the Register (Article 33). Any region may challenge them before the Court.

*Evidence: in the 30-year world plan, serving the decent level first brings every region to decent energy in 4 years instead of 8, decent health care in 7 instead of 12, and decent housing in 9 instead of 20, with no loss on the comfortable goal. Planning where food comes from cuts transport by 69% (V7.9, `v79/allocation`).*""")

# ---- Money and data
insert_after("Article 12", clean(P["12a"]))
replace("""3. Gains in productivity become shorter working hours, never higher prices or unemployment.""",
        """3. Gains in productivity become shorter working hours, never higher prices or unemployment.
4. **New products.** The price of a new product is the hours of work it embodies, including all inputs, times the fixed price of one hour. It is set once, when the product is introduced, and published with its calculation.
5. **The price of one hour is fixed forever.**
6. **Nature has a price too.** Goods that use scarce natural resources (fossil fuels, energy, rare materials, land) carry a resource surcharge, measured physically. Energy, fuels and air travel never become cheaper, relative to other goods, than they are when a region joins. The surcharge goes to the One Earth Fund.
7. **Rare goods.** What cannot be produced again, such as an original work of art or a seat at a unique event, is allocated by turn, lottery or rotation, never by bidding.

*Evidence: priced by hours alone, French fuels would become 79% cheaper and electricity 65% cheaper relative to other goods, because their market prices pay mostly for resources, not work. That would encourage waste, so the surcharge is essential (V7.9, `v79/prices`).*""")
replace("""1. Savings are free and protected, up to a personal money cap set each year by a published coefficient, so that people keep working to produce what is needed.""",
        """1. Savings are free and protected, up to a personal money cap set each year by the Monetary Authority under Article 17b, so that people keep working to produce what is needed.
4. **The cap applies only to savings held, never to salary or spending.** Every person always receives their full salary and may spend it.""")
p17b = clean(P["17b"]).replace(
    "4. **The thermostat rule.** The cap moves each year by a published formula, within at most 10% up or down. The formula is based on the measured stock of unspent money compared with its target and on hours worked compared with need. Anyone can recompute the result from public data.",
    "4. **The thermostat rule.** Each year the cap is multiplied by the square root of (target stock of unspent money ÷ actual stock), within at most 10% up or down, and never set below one year of base salary. The target is set by law (12 months of the region's consumption in the research model). Anyone can recompute the result from public data.")
p17b = p17b.replace("[the formula itself is still a research item, see Article 17 notes]", "")
p17b += "\n*Evidence: in a 60-year simulation with a disaster, a wave of precautionary saving, a baby boom and fast automation, this rule kept unspent money within 10–14 months of consumption and no salaried person was ever blocked from a first home. Without the 10% limit the cap could fall 88% in a single year (V7.9, `v79/money`).*\n"
insert_after("Article 17a", p17b)

# ---- Homes
house = (V79 / "housing" / "RESEARCH_NOTE.md").read_text(encoding="utf-8")
seg = house[house.index("> **7. Allocation where demand exceeds supply.**"):house.index("*Evidence: in a 30-year simulation")]
seg = "\n".join(l[2:] if l.startswith("> ") else ("" if l.strip() == ">" else l) for l in seg.splitlines()).strip()
replace("6. New homes are built with low-carbon materials where possible.",
        "6. New homes are built with low-carbon materials where possible.\n" + seg +
        "\n\n*Evidence: in a 30-year simulation of a city with 2.5 applicants per desirable home, points with a lottery housed 28% of high-need households within 5 years (0% for a queue), with no income gradient; bidding left the poorer half with almost nothing; the must-live-in rule cut empty desirable homes from 6–32% to under 0.5% (V7.9, `v79/housing`).*")

# ---- Institutions
insert_after("Article 22", clean(P["22a"]))
insert_after("Article 26", clean(P["26a"]))
insert_after("Article 30", clean(P["30a"]))
insert_after("Article 32", clean(P["32a"]))
insert_after("Article 32a", clean(P["32b"]))
insert_after("Article 39", clean(P["39a"]))
insert_after("Article 41", clean(P["41a"]))
insert_after("Article 42", clean(P["42a"]))
insert_after("Article 42a", clean(P["42b"]))
insert_after("T-6", clean(P["T-7"]))

# ---- notes for the author
s = s.rstrip() + """

- **V7.9 (2026-11-03): the missing designs and power safeguards added** — Articles 3c, 3d, 5b, 5c, 6a, 9a, 10a, 12a, 17b, 22a, 26a, 30a, 32a, 32b, 39a, 41a, 42a, 42b, T-7; amendments to 5a, 13, 17 and 18. Evidence and the stress test of 13 attack scenarios are in `v79/`.
- **Decisions still open for the author:**
  - the level of the money cap: the low cap (about 1.4 years of base salary, reached by about half of adults) or a higher one (about 5 years, reached by about 28%), and whether money above the cap may buy paid free time (time account);
  - whether regions may reserve up to 30% of desirable homes for an open lottery among all applicants (Article 18.8);
  - the age weight for health need (Article 10a.2), to be calibrated.
"""
C.write_text(s, encoding="utf-8")
print("articles:", s.count("**Article "), "words:", len(s.split()))
