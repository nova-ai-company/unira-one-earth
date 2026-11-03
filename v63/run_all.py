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
         ("../v66/model", ["run_health.py"]), ("../v66/model", ["run_housing.py"]),
         ("../v67", ["run_transition.py"]), ("../v67", ["energy_budget_check.py"]), ("../v68/counterfactual", ["compare.py"]), ("../v69/coordination", ["run.py"]), ("../v70/housing", ["run.py"]), ("../v72/joining", ["run.py"]), ("../v74/distribution", ["run.py"]), ("../v74/distribution", ["world.py"]), ("../v78/planning", ["forecast.py"]), ("../v78/planning", ["information.py"]), ("../v79/allocation", ["formula.py"]), ("../v79/allocation", ["location.py"]), ("../v79/prices", ["price_rule.py"]), ("../v79/money", ["thermostat.py"]), ("../v79/money", ["cap_level.py"]), ("../v79/housing", ["simulate.py"]),
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
    for d in ("../v62", "io", "flows", "health", "ledger", "../v64", "../v65/data", "../v65/model", "../v66/data", "../v66/model", "../v67", "../v68/counterfactual", "../v69/coordination", "../v70/housing", "../v72/joining", "../v75/constitution", "../v78/planning", "../v74/distribution", "../v79", "../v79/housing"):
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
