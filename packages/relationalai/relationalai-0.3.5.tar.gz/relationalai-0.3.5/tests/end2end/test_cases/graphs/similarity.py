import relationalai as rai
from relationalai import std

# Query snapshots are output in same order as this list.
UNWEIGHTED_ALGOS = [
    "jaccard_similarity",
    "cosine_similarity",
]

WEIGHTED_ALGOS = [
    "weighted_jaccard_similarity",
    "weighted_cosine_similarity",
]

model = rai.Model(name=globals().get("name", ""), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    Relationship.add(from_=obj1, to=obj2, weight=1.0)

# Make unweighted and weighted graphs.
# NOTE: cosine_similarity only supports undirected graphs.
unweighted_graph = std.graphs.Graph(model, undirected=True)
with model.rule():
    r = Relationship()
    unweighted_graph.Edge.add(r.from_, r.to)

weighted_graph = std.graphs.Graph(model, undirected=True, weighted=True)
with model.rule():
    r = Relationship()
    weighted_graph.Edge.add(r.from_, r.to, weight=r.weight)

# Test the unweighted algorithms.
for algo_name in UNWEIGHTED_ALGOS:
    with model.query(tag=algo_name) as select:
        o1 = Object()
        o2 = Object()
        algo = getattr(unweighted_graph.compute, algo_name)(o1, o2)
        select(o1, o2, algo)

# Test the weighted algorithms.
for algo_name in WEIGHTED_ALGOS:
    with model.query(tag=algo_name) as select:
        o1 = Object()
        o2 = Object()
        algo = getattr(weighted_graph.compute, algo_name)(o1, o2)
        select(o1, o2, algo)
