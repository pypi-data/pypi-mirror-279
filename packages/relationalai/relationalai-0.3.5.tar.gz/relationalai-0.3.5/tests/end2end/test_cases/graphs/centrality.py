import relationalai as rai
from relationalai import std

# Query snapshots are output in same order as this list.
UNWEIGHTED_ALGOS = [
    "pagerank",
    "eigenvector_centrality",
    "degree_centrality",
    "betweenness_centrality",
]

WEIGHTED_ALGOS = ["weighted_degree_centrality"]

model = rai.Model(name=globals().get("name", "test_centrality"), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    Relationship.add(from_=obj1, to=obj2, weight=10)
# eigenvector_centrality only supports undirected graphs.
undirected_graph = std.graphs.Graph(model, undirected=True)

with model.rule():
    r = Relationship()
    undirected_graph.Edge.add(r.from_, r.to)

for algo_name in UNWEIGHTED_ALGOS:
    with model.query(tag=algo_name) as select:
        o = Object()
        algo = getattr(undirected_graph.compute, algo_name)(o)
        select(o, algo)

weighted_graph = std.graphs.Graph(model, undirected=True, weighted=True)

with model.rule():
    r = Relationship()
    weighted_graph.Edge.add(r.from_, r.to, weight=r.weight)

for algo_name in WEIGHTED_ALGOS:
    with model.query(tag=algo_name) as select:
        o = Object()
        algo = getattr(weighted_graph.compute, algo_name)(o)
        select(o, algo)
