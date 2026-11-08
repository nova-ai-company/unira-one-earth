"""Run every V6.3 component offline (from frozen snapshots), then all tests.

Order matters: ledger reads outputs of io, flows, health and ../v62.
    python3 run_all.py
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEPS = [("../v62", ["run_all.py"]), ("io", ["run.py"]), ("flows", ["run.py"]),
         ("health", ["run.py"]), ("ledger", ["ledger.py"]), ("../v64", ["run.py"]), ("../v64", ["run_lifecycle.py"]), ("../v65/data", ["build.py"]), ("../v65/model", ["run.py"]), ("../v66/data", ["build.py"]),
         ("../v66/model", ["run_health.py"]), ("../v66/model", ["run_health_levers.py"]), ("../v66/model", ["training_capacity.py"]),("../v66/model", ["run_housing.py"]),
         ("../v67", ["run_transition.py"]), ("../v67", ["energy_budget_check.py"]), ("../v68/counterfactual", ["compare.py"]), ("../v69/coordination", ["run.py"]), ("../v70/housing", ["run.py"]), ("../v70/housing", ["run_levers.py"]), ("../v70/housing", ["factories.py"]), ("../v70/housing", ["materials.py"]), ("../v72/joining", ["run.py"]), ("../v74/distribution", ["run.py"]), ("../v74/distribution", ["world.py"]), ("../v78/planning", ["forecast.py"]), ("../v78/planning", ["information.py"]), ("../v79/allocation", ["formula.py"]), ("../v79/allocation", ["location.py"]), ("../v79/prices", ["price_rule.py"]), ("../v79/money", ["thermostat.py"]), ("../v79/money", ["cap_level.py"]), ("../v79/housing", ["simulate.py"]), ("../v79/housing", ["open_share.py"]), ("../v79/money", ["time_account.py"]), ("../v79/health_need", ["weights.py"]), ("../v81/prices", ["calculator.py"]), ("../v81/prices", ["build_page.py"]), ("../v82/production", ["simulate.py"]), ("../v82/jobs", ["simulate.py"]), ("../v82/capital", ["model.py"]), ("../v82/enterprise", ["simulate.py"]), ("../v82/worldmoney", ["model.py"]), ("../v82/trade", ["analysis.py"]), ("../v82/sizes", ["sizes.py"]), ("../v83/equality_credit", ["model.py"]), ("../v83/equality_credit", ["stress.py"]), ("../v84/quotas", ["compare.py"]), ("../v84/quotas", ["sensitivity.py"]), ("../v85/realdata", ["capacity.py"]), ("../v85/realdata", ["hybrid_real.py"]), ("../v86/automation", ["model.py"]), ("../v87/livingstandard", ["simulate.py"]), ("../v87/livingstandard", ["level2.py"]), ("../v88/essential", ["model.py"]), ("../v89/integrated", ["simulate.py"]), ("../v90/conflict", ["model.py"]), ("../v90", ["build_page.py"]), ("../v91/institutions", ["panel.py"]), ("../v91/institutions", ["model.py"]), ("../v91", ["build_page.py"]), ("../v92/hours", ["hours_path.py"]), ("../v92", ["build_page.py"]), ("../validation", ["backtest.py"]), ("../validation", ["uncertainty.py"]), ("../paper", ["build_paper.py"]),
         ("../references", ["check_bib.py"]), ("../references", ["cite.py"]), ("../v67/dashboard", ["build_dashboard.py"]), ("../v73/book", ["build_book.py"]), ("../v75/constitution", ["voting.py"]), ("../v75/constitution", ["build.py"]), ("../v77/site", ["build_site.py"])]


def main():
    for d, cmd in STEPS:
        cwd = (ROOT / d).resolve()
        r = subprocess.run([sys.executable, *cmd], cwd=cwd, capture_output=True, text=True)
        print(f"[{'ok' if r.returncode == 0 else 'FAILED'}] {d}/{cmd[0]}")
        if r.returncode:
            print(r.stdout[-2000:], r.stderr[-2000:])
            raise SystemExit(1)
    total = 0
    for d in ("../v62", "io", "flows", "health", "ledger", "../v64", "../v65/data", "../v65/model", "../v66/data", "../v66/model", "../v67", "../v68/counterfactual", "../v69/coordination", "../v70/housing", "../v72/joining", "../v75/constitution", "../v78/planning", "../v74/distribution", "../v79", "../v79/housing", "../v81/prices", "../v82/production", "../v82/jobs", "../v82/capital", "../v82/enterprise", "../v82/worldmoney", "../v82/trade", "../v82/sizes", "../v83/equality_credit", "../v84/quotas", "../v85/realdata", "../v86/automation", "../v87/livingstandard", "../v88/essential", "../v89/integrated", "../v90/conflict", "../v91/institutions", "../v92/hours", "../validation"):
        start = "tests" if (ROOT / d / "tests").is_dir() else "."
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", start],
                           cwd=(ROOT / d).resolve(), capture_output=True, text=True)
        line = [l for l in r.stderr.splitlines() if l.startswith("Ran ")]
        n = int(line[0].split()[1]) if line else 0
        total += n
        print(f"[{'ok' if r.returncode == 0 else 'FAILED'}] tests {d}: {n}")
        if r.returncode:
            print(r.stderr[-2000:])
            raise SystemExit(1)
    print(f"all components regenerated; {total} tests passed")


if __name__ == "__main__":
    main()
