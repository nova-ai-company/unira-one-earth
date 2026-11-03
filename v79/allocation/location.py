"""UNIRA V7.9 — which region supplies which (design 1, production location), tested on food.

Every region keeps what it needs for a decent diet (2,100 kcal eaten, 19% waste -> 2,593 kcal supplied per person);
regions above it hold a surplus, regions below a deficit (FAO food balance per region, v65). One Earth plans
the shipments. Two plans are compared, both covering every deficit:
    pro_rata    every surplus region ships to every deficit region in proportion (no planning of location)
    optimised   minimum total transport (kcal x km), min-cost flow on great-circle distances between capitals
                (World Bank country coordinates)
Fairness rule checked: how many surplus regions take part (spreading productive work) and the longest route.
python3 location.py  ->  ../outputs/food_location.json"""
import heapq
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
U = HERE.parents[1]
sys.path.insert(0, str(U / "v67"))
import run_transition as rt  # noqa: E402

NEED_KCAL = 2100 / (1 - 0.19)


def coords():
    meta = json.loads((U / "v65" / "data" / "raw" / "wb_country_meta.json").read_text())[1]
    return {m["id"]: (float(m["latitude"]), float(m["longitude"])) for m in meta if m["latitude"]}


def km(a, b):
    (la1, lo1), (la2, lo2) = [(math.radians(x), math.radians(y)) for x, y in (a, b)]
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))


def min_cost_flow(supply, demand, cost):
    """Transportation problem by successive shortest paths (Dijkstra with potentials) on the bipartite graph
    source -> suppliers -> consumers -> sink. Units: bn kcal/day. Returns {(i, j): flow}."""
    S, D = list(supply), list(demand)
    nodes = ["s"] + S + D + ["t"]
    idx = {n: i for i, n in enumerate(nodes)}
    graph = [[] for _ in nodes]

    def add(u, v, cap, c):
        graph[u].append([v, cap, c, len(graph[v])])
        graph[v].append([u, 0.0, -c, len(graph[u]) - 1])
    for i in S:
        add(idx["s"], idx[i], supply[i], 0.0)
        for j in D:
            add(idx[i], idx[j], float("inf"), cost[i, j])
    for j in D:
        add(idx[j], idx["t"], demand[j], 0.0)
    need, pot = sum(demand.values()), [0.0] * len(nodes)
    while need > 1e-9:
        dist, prev = [float("inf")] * len(nodes), [None] * len(nodes)
        dist[0] = 0.0
        pq = [(0.0, 0)]
        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            for k, (v, cap, c, _) in enumerate(graph[u]):
                nd = d + c + pot[u] - pot[v]
                if cap > 1e-12 and nd < dist[v] - 1e-12:
                    dist[v], prev[v] = nd, (u, k)
                    heapq.heappush(pq, (nd, v))
        t = idx["t"]
        if dist[t] == float("inf"):
            raise ValueError("deficits cannot be covered")
        pot = [p + (dist[i] if dist[i] < float("inf") else 0.0) for i, p in enumerate(pot)]
        f, v = need, t
        while v:
            u, k = prev[v]
            f = min(f, graph[u][k][1])
            v = u
        v = t
        while v:
            u, k = prev[v]
            graph[u][k][1] -= f
            graph[v][graph[u][k][3]][1] += f
            v = u
        need -= f
    flows = {}
    for i in S:
        for v, cap, c, rev in graph[idx[i]]:
            if nodes[v] in demand:
                used = graph[v][rev][1]
                if used > 1e-9:
                    flows[i, nodes[v]] = used
    return flows


def main():
    regions, xy = rt.load_regions(), coords()
    regions = {k: v for k, v in regions.items() if k in xy}
    bal = {k: (r["kcal"] - NEED_KCAL) * r["pop0"] / 1e9 for k, r in regions.items()}  # bn kcal/day
    supply = {k: v for k, v in bal.items() if v > 0}
    demand = {k: -v for k, v in bal.items() if v < 0}
    cost = {(i, j): km(xy[i], xy[j]) for i in supply for j in demand}
    tot_s, tot_d = sum(supply.values()), sum(demand.values())
    pro = {(i, j): supply[i] / tot_s * demand[j] for i in supply for j in demand}
    opt = min_cost_flow(supply, demand, cost)
    res = {"need_kcal_supplied_per_person": round(NEED_KCAL), "regions": len(regions),
           "surplus_regions": len(supply), "deficit_regions": len(demand),
           "surplus_bn_kcal_day": round(tot_s, 1), "deficit_bn_kcal_day": round(tot_d, 1),
           "deficit_share_of_world_supply": round(tot_d / sum(r["kcal"] * r["pop0"] / 1e9 for r in regions.values()), 4)}
    for name, fl in (("pro_rata", pro), ("optimised", opt)):
        moved = sum(fl.values())
        res[name] = {"mean_km_per_kcal": round(sum(f * cost[k] for k, f in fl.items()) / moved),
                     "supplier_regions_used": len({i for i, _ in fl}),
                     "routes": len(fl), "longest_route_km": round(max(cost[k] for k in fl))}
    res["transport_saved_pct"] = round(100 * (1 - res["optimised"]["mean_km_per_kcal"] / res["pro_rata"]["mean_km_per_kcal"]), 1)
    res["largest_optimised_flows"] = [[i, j, round(f, 1), round(cost[i, j])] for (i, j), f in
                                      sorted(opt.items(), key=lambda x: -x[1])[:12]]
    (HERE.parent / "outputs").mkdir(exist_ok=True)
    (HERE.parent / "outputs" / "food_location.json").write_text(json.dumps(res, indent=2))
    print(json.dumps({k: v for k, v in res.items() if k != "largest_optimised_flows"}, indent=1))
    print(res["largest_optimised_flows"])


if __name__ == "__main__":
    main()
