# UNIRA external review: feedback form

Copy this file, fill it in, and return it. Plain text or Markdown is fine. Leave blank any section outside your expertise. Specific, checkable comments are more useful than general ones: give the file and line, and say what should change.

---

## 1. Reviewer

| Field | Answer |
|---|---|
| Name (or "anonymous") | |
| Affiliation (optional) | |
| Field(s) of expertise (labour / macro-money / energy-climate / food-land / health workforce / housing-construction / governance-political science / law / demography-migration / statistics-reproducibility / other) | |
| Files actually read | |
| Did you run the code? (no / partly / fully; Python version) | |
| Declaration of interests (affiliations, funding, positions on world federalism, degrowth or related movements) | |
| May this review be published? (yes, signed / yes, anonymous / no) | |
| Date | |

## 2. Overall assessment

**2.1 Is the separation between normative design rules and empirical claims clear and maintained throughout?** (Tick one)
☐ Yes ☐ Mostly ☐ No

Comment:

**2.2 Within your field, how sound are the methods?** (Tick one)
☐ Sound ☐ Sound with minor issues ☐ Major issues ☐ Unsound

Comment:

**2.3 Within your field, do the headline results follow from the data and assumptions?** (Tick one)
☐ Yes ☐ Partly ☐ No

Comment:

**2.4 Are the conditions and limitations stated honestly and completely?** (Tick one)
☐ Yes ☐ Partly ☐ No

Comment:

**2.5 Summary in 3–5 sentences:**

## 3. Major issues

These are problems that would change a headline result or its stated conditions. For each one, give a severity from 1 to 3 (1 = would overturn the result in your field, 2 = changes the size or conditions of the result, 3 = weakens confidence but the result likely holds).

| # | Issue | Affected result (e.g. "France year-1 gap closed at 88%") | File / section | Severity | Suggested remedy |
|---|---|---|---|---|---|
| M1 | | | | | |
| M2 | | | | | |
| M3 | | | | | |

## 4. Specific errors

These are factual, arithmetic, coding, citation or consistency errors. Line numbers refer to the files as distributed. Use `grep -n` or any editor to find them.

| # | File | Line(s) | What is wrong | What it should be | Source for the correction |
|---|---|---|---|---|---|
| E1 | | | | | |
| E2 | | | | | |
| E3 | | | | | |
| E4 | | | | | |

Known candidates are listed in `REVIEW_BRIEF.md` §6 and `REVIEW_QUESTIONS.md` §10.6. Please confirm or reject each one you check:

| Candidate | Confirmed / rejected / not checked | Comment |
|---|---|---|
| Housing: 4.7 bn m²/yr (backlog) vs 6–7 bn m²/yr peak (with growth): corrected reconciliation | | |
| Labour 33–64 h/m² (48 central) | | |
| "≈85% preserved with strong safeguards" vs 80–89% by domain | | |
| All 151 tests pass (`python3 v63/run_all.py`) | | |
| Blocking minority of 21 regions (`double_majority_55_65_sqrt` in `v75/outputs/voting.json`) | | |
| New clean energy used both for convergence and implicitly for decarbonisation (`v67/transition.py` L97–104) | | |

## 5. Verdict on each falsification test

For each test, say whether it is well posed and what the current evidence suggests. **Well posed** means measurable, not trivially passed, and not resting mainly on SYNTHETIC inputs.

- **Well posed?**
  - Y = yes;
  - P = partly;
  - N = no.
- **Current evidence:**
  - Survives = refutation not supported by the evidence;
  - At risk = evidence points toward refutation;
  - Refuted;
  - Cannot judge.

| Test | Claim refuted if… | Well posed? (Y / P / N) | Current evidence (Survives / At risk / Refuted / Cannot judge) | Evidence or data that would decide it | Sharper wording you propose |
|---|---|---|---|---|---|
| F1 Labour | employment at ages 20–64 cannot exceed about 85% within a few years under universal work, and θ < 0.1 | | | | |
| F2 Money | capped people spend instead of saving, and excess demand at fixed prices exceeds reserve stocks | | | | |
| F3 Health | world training capacity cannot exceed about 1.5×, putting EU-level care for all more than 50 years away | | | | |
| F4 Ecology | clean-energy build stays below the 2025 record (669 GW/yr), or material use cannot fall at least 2× during the building programme | | | | |
| F5 Housing | world construction capacity cannot add about 65 bn m² within a generation | | | | |
| F6 Comparison | a reformed market economy with the same resources reaches the same outcomes | | | | |
| F7 Governance | leakage cannot be kept well below about 45%, or data lags stay above about 5 years | | | | |

Are any important falsification tests **missing**? For example: capital and workplace constraints, the hours needed to run UNIRA's own institutions, legitimacy, or legal feasibility of the transition.

## 6. Assumptions

Which SYNTHETIC assumptions (S1–S16 in `REVIEW_BRIEF.md` §5) are least defensible in your field? What value or range would you use instead, and what is the source?

| Assumption | Used value | Your value / range | Source |
|---|---|---|---|
| | | | |
| | | | |

## 7. Suggested data and literature

These are datasets, studies or methods the research should use and does not.

| Item (dataset, table code, paper or method) | What it would replace or add | Where it applies (file / section) | Access (open / licensed / microdata) |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

## 8. Reproducibility (if you ran the code)

| Check | Result |
|---|---|
| Command(s) run | |
| Tests passed / failed | |
| Outputs byte-identical to the archive? (list any differences) | |
| Hash mismatches in `raw_manifest.csv` | |
| Environment problems (missing packages, hard-coded paths) | |

## 9. Answers to field questions

Give the question numbers from `REVIEW_QUESTIONS.md` (e.g. "3.1") and your answers.

| Question | Answer |
|---|---|
| | |
| | |

## 10. Final recommendation for the research programme

Tick one:

☐ The physical-feasibility claims in my field are adequately supported as stated.
☐ The claims hold only after the major issues above are fixed.
☐ The claims should be substantially weakened or withdrawn in my field.
☐ I cannot judge.

Highest-priority next step in your field:

Other comments:
