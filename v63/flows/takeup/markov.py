"""3-state (U, E, I) Markov-chain helpers, pure Python.

Assumptions when used to annualise quarterly flows (documented in README.md):
  * first-order Markov: next-quarter status depends only on current status;
  * homogeneous within a state: no duration dependence, no unobserved heterogeneity;
  * quarter-specific matrices (NSA) are compounded in calendar order, so seasonality is kept.
Because the long-term unemployed exit far more slowly (lfsi_long_e01), the chain
re-applies the AVERAGE exit rate to survivors who are in fact slower: it OVERSTATES the
one-year U->E probability. The direct year-on-year rate (lfsi_long_a) is preferred.
"""
STATES = ("U", "E", "I")


def matmul(a, b):
    n, m, p = len(a), len(b), len(b[0])
    return [[sum(a[i][k] * b[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def identity(n=3):
    return [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]


def from_levels(levels):
    """levels: {('U','E'): thousands, ...} for all 9 transitions -> row-stochastic matrix.
    Returns None if any of the 9 cells is missing or a row total is zero."""
    m = []
    for s in STATES:
        row = [levels.get((s, t)) for t in STATES]
        if any(v is None for v in row) or sum(row) <= 0:
            return None
        tot = sum(row)
        m.append([v / tot for v in row])
    return m


def compound(matrices):
    """Product P1 @ P2 @ ... in the given (chronological) order."""
    out = identity(len(matrices[0]))
    for p in matrices:
        out = matmul(out, p)
    return out


def prob(matrix, origin, dest):
    return matrix[STATES.index(origin)][STATES.index(dest)]
