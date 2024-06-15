import relationalai as rai
from relationalai import std

# Query snapshots are output in same order as these lists.
NO_ARGS = [
    "avg_clustering_coefficient",
]

ONE_ARG = [
    "local_clustering_coefficient",
]

model = rai.Model(name=globals().get("name", ""), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    obj3 = Object.add(id=3)
    obj4 = Object.add(id=4)
    Relationship.add(from_=obj1, to=obj2)
    Relationship.add(from_=obj1, to=obj3)
    Relationship.add(from_=obj1, to=obj4)
    Relationship.add(from_=obj2, to=obj3)

graph = std.graphs.Graph(model, undirected=True)
graph.Node.extend(Object)

with model.rule():
    r = Relationship()
    graph.Edge.add(r.from_, r.to)

for algo_name in NO_ARGS:
    with model.query(tag=algo_name) as select:
        algo = getattr(graph.compute, algo_name)()
        select(algo)

for algo_name in ONE_ARG:
    with model.query(tag=algo_name) as select:
        o = Object()
        algo = getattr(graph.compute, algo_name)(o)
        select(o, algo)