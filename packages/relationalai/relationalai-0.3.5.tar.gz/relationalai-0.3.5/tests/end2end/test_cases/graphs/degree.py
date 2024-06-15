import relationalai as rai
from relationalai import std

# Query snapshots are output in same order as these lists.
UNARY_ALGOS = [
    "min_degree",
    "max_degree",
    "avg_degree",
    "min_indegree",
    "max_indegree",
    "avg_indegree",
    "min_outdegree",
    "max_outdegree",
    "avg_outdegree",
]

BINARY_ALGOS = [
    "degree",
    "indegree",
    "outdegree",
]

model = rai.Model(name=globals().get("name", "test_degree"), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    Relationship.add(from_=obj1, to=obj2)

graph = std.graphs.Graph(model)

with model.rule():
    r = Relationship()
    graph.Edge.add(r.from_, r.to)

for algo_name in UNARY_ALGOS:
    with model.query(tag=algo_name) as select:
        algo = getattr(graph.compute, algo_name)()
        select(algo)

for algo_name in BINARY_ALGOS:
    with model.query(tag=algo_name) as select:
        o = Object()
        algo = getattr(graph.compute, algo_name)(o)
        select(o, algo)
