"""UNIRA V6.3 — hours of human work embodied in final uses (France).

Results are in HOURS, not euros. The euro-denominated symmetric input-output
table (naio_10_cp1700, product x product, domestic flows) is used only as a
technical proxy for physical interdependence: the share of each product's
production that requires each input. No market price, profit, wage or money
flow enters any UNIRA result (see RESEARCH_NOTE §1).

    A[i,j] = Z_dom[i,j] / x[j]      domestic input i per unit of product j
    l[j]   = hours[j] / x[j]        direct hours per unit of output
    m'     = l' (I - A)^-1          total (direct + indirect) hours per unit of final use
    hours embodied in final-use vector f  =  m' f

Identity checked in tests: sum over final-use categories of m' f_k = total hours.
Hypothetical extraction of product p: set row and column p of A and f[p] to 0;
hours saved = total hours - hours of the remaining system.
"""

PRODUCTS = {  # CPA product -> NACE code in nama_10_a64_e carrying its hours
    "CPA_A01": "A01", "CPA_A02": "A02", "CPA_A03": "A03", "CPA_B": "B",
    "CPA_C10-12": "C10-C12", "CPA_C13-15": "C13-C15", "CPA_C16": "C16", "CPA_C17": "C17",
    "CPA_C18": "C18", "CPA_C19": "C19", "CPA_C20": "C20", "CPA_C21": "C21", "CPA_C22": "C22",
    "CPA_C23": "C23", "CPA_C24": "C24", "CPA_C25": "C25", "CPA_C26": "C26", "CPA_C27": "C27",
    "CPA_C28": "C28", "CPA_C29": "C29", "CPA_C30": "C30", "CPA_C31_32": "C31_C32",
    "CPA_C33": "C33", "CPA_D": "D", "CPA_E36": "E36", "CPA_E37-39": "E37-E39", "CPA_F": "F",
    "CPA_G45": "G45", "CPA_G46": "G46", "CPA_G47": "G47", "CPA_H49": "H49", "CPA_H50": "H50",
    "CPA_H51": "H51", "CPA_H52": "H52", "CPA_H53": "H53", "CPA_I": "I", "CPA_J58": "J58",
    "CPA_J59_60": "J59_J60", "CPA_J61": "J61", "CPA_J62_63": "J62_J63", "CPA_K64": "K64",
    "CPA_K65": "K65", "CPA_K66": "K66",
    "CPA_L68A": None,  # imputed rents of owner-occupiers: no labour input by definition
    "CPA_L68B": "L68", "CPA_M69_70": "M69_M70", "CPA_M71": "M71", "CPA_M72": "M72",
    "CPA_M73": "M73", "CPA_M74_75": "M74_M75", "CPA_N77": "N77", "CPA_N78": "N78",
    "CPA_N79": "N79", "CPA_N80-82": "N80-N82", "CPA_O": "O", "CPA_P": "P", "CPA_Q86": "Q86",
    "CPA_Q87_88": "Q87_Q88", "CPA_R90-92": "R90-R92", "CPA_R93": "R93", "CPA_S94": "S94",
    "CPA_S95": "S95", "CPA_S96": "S96", "CPA_T": "T", "CPA_U": "U",
}

# France does not publish hours for every A64 division. Unpublished children get the
# parent's residual hours in proportion to published PERSONS (physical key), i.e.
# equal hours per person within the parent group (documented limitation).
HOURS_TREE = {
    "A": ["A01", "A02", "A03"], "C16-C18": ["C16", "C17", "C18"], "C22_C23": ["C22", "C23"],
    "C24_C25": ["C24", "C25"], "C29_C30": ["C29", "C30"], "C31-C33": ["C31_C32", "C33"],
    "E": ["E36", "E37-E39"], "G": ["G45", "G46", "G47"], "H": ["H49", "H50", "H51", "H52", "H53"],
    "J58-J60": ["J58", "J59_J60"], "K": ["K64", "K65", "K66"], "M69-M71": ["M69_M70", "M71"],
    "M73-M75": ["M73", "M74_M75"], "N": ["N77", "N78", "N79", "N80-N82"], "R": ["R90-R92", "R93"],
    "S": ["S94", "S95", "S96"],
}


def resolve_hours(hours, year):
    """Return {nace: (thousand hours, source)} with documented allocation."""
    y = str(year)
    hw = lambda n: hours.get((y, n, "THS_HW", "EMP_DC"))
    per = lambda n: hours.get((y, n, "THS_PER", "EMP_DC"))
    out = {}
    for n in {v for v in PRODUCTS.values() if v}:
        if hw(n) is not None:
            out[n] = (hw(n), "published")
    for parent, kids in HOURS_TREE.items():
        missing = [k for k in kids if k not in out]
        if not missing:
            continue
        if hw(parent) is None or any(per(k) is None for k in missing):
            raise ValueError(f"{y}: cannot allocate hours of {parent} to {missing}")
        residual = hw(parent) - sum(out[k][0] for k in kids if k in out)
        p_sum = sum(per(k) for k in missing)
        for k in missing:
            out[k] = (residual * per(k) / p_sum, f"allocated_from_{parent}_by_persons")
    return out


FINAL_USES = {  # label -> IO column codes (domestic flows) summed
    "household_consumption": ["P3_S14"],
    "government_consumption": ["P3_S13"],
    "npish_consumption": ["P3_S15"],
    "gross_fixed_capital_formation": ["P51G"],
    "inventories_and_valuables": ["P52", "P53"],
    "exports": ["P6"],
}


def solve(A, b):
    """Solve (I - A) x = b by Gauss-Jordan with partial pivoting (stdlib)."""
    n = len(A)
    M = [[(1.0 if i == j else 0.0) - A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-14:
            raise ValueError("singular (I - A)")
        M[col], M[piv] = M[piv], M[col]
        p = M[col][col]
        M[col] = [v / p for v in M[col]]
        for r in range(n):
            if r != col and M[r][col]:
                f = M[r][col]
                M[r] = [a - f * c for a, c in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]


def multipliers(A, l):
    """m' = l'(I-A)^-1, computed as the solution of (I-A)' m = l."""
    At = [list(row) for row in zip(*A)]
    return solve(At, l)


class IOSystem:
    def __init__(self, cells, hours, year):
        """cells: {(year, stk_flow, prd_ava, prd_use): MIO_EUR}; hours: {(year, nace, unit, item): v}"""
        y = str(year)
        self.year, self.products = y, list(PRODUCTS)
        P = self.products
        get = lambda f, a, u: cells.get((y, f, a, u)) or 0.0
        self.x = [get("TOTAL", "P1", p) for p in P]
        self.Z = [[get("DOM", i, j) for j in P] for i in P]
        self.A = [[self.Z[i][j] / self.x[j] if self.x[j] else 0.0 for j in range(len(P))]
                  for i in range(len(P))]
        self.F = {k: [sum(get("DOM", p, c) for c in cols) for p in P] for k, cols in FINAL_USES.items()}
        self.F_imp = {k: [sum(get("IMP", p, c) for c in cols) for p in P] for k, cols in FINAL_USES.items()}
        self.Z_imp_total = [sum(get("IMP", i, j) for j in P) for i in P]
        self.total_output = get("TOTAL", "P1", "TOTAL")
        resolved = resolve_hours(hours, y)
        self.hours = [resolved[PRODUCTS[p]][0] if PRODUCTS[p] else 0.0 for p in P]
        self.hours_source = [resolved[PRODUCTS[p]][1] if PRODUCTS[p] else "none_imputed_rent" for p in P]
        self.hours_total_na = hours.get((y, "TOTAL", "THS_HW", "EMP_DC"))
        self.l = [h / xv if xv else 0.0 for h, xv in zip(self.hours, self.x)]
        self.m = multipliers(self.A, self.l)

    # --- accounting ---------------------------------------------------------
    def embodied(self, f):
        return sum(mi * fi for mi, fi in zip(self.m, f))

    def embodied_by_use(self):
        return {k: self.embodied(f) for k, f in self.F.items()}

    def embodied_by_use_and_product(self):
        """Hours embodied in each final product (incl. its whole domestic supply chain)."""
        return {k: [mi * fi for mi, fi in zip(self.m, f)] for k, f in self.F.items()}

    def row_balance_residuals(self):
        """x_i - (sum_j Z_dom[i,j] + domestic final uses of i); should be ~0."""
        n = len(self.products)
        return [self.x[i] - sum(self.Z[i]) - sum(self.F[k][i] for k in self.F) for i in range(n)]

    def import_hours_equivalent(self):
        """Hours France would need to make its imports itself with its own technology
        (domestic technology assumption). An indicator of labour embodied abroad,
        not an estimate of foreign hours."""
        imp = [self.Z_imp_total[i] + sum(self.F_imp[k][i] for k in self.F_imp) for i in range(len(self.products))]
        return self.embodied(imp)

    # --- counterfactuals ----------------------------------------------------
    def hours_with_final_demand_scaled(self, scale):
        """Total hours if domestic final demand for product p is scaled by scale[p]
        (A unchanged: input recipes of remaining products stay the same)."""
        f = [sum(self.F[k][i] for k in self.F) * scale.get(p, 1.0) for i, p in enumerate(self.products)]
        return self.embodied(f)

    def hypothetical_extraction(self, p):
        """Hours saved if product p disappears as final AND intermediate good.
        Upper bound: assumes no substitute input is needed by its users."""
        k = self.products.index(p)
        A2 = [[0.0 if (i == k or j == k) else a for j, a in enumerate(row)] for i, row in enumerate(self.A)]
        l2 = [0.0 if i == k else v for i, v in enumerate(self.l)]
        m2 = multipliers(A2, l2)
        f = [0.0 if i == k else sum(self.F[c][i] for c in self.F) for i in range(len(self.products))]
        return sum(self.hours) - sum(a * b for a, b in zip(m2, f))
