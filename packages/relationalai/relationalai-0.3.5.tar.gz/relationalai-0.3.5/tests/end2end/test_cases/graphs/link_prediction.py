import relationalai as rai
from relationalai import std

# Query snapshots are output in same order as this list.
ALGOS = [
    "adamic_adar",
    "preferential_attachment",
    "common_neighbor",
]

model = rai.Model(name=globals().get("name", ""), config=globals().get("config"))
Object = model.Type("Object")
LinkPrediction = model.Type("LinkPrediction")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    obj3 = Object.add(id=3)
    obj4 = Object.add(id=4)
    LinkPrediction.add(from_=obj1, to=obj2)
    LinkPrediction.add(from_=obj2, to=obj3)
    LinkPrediction.add(from_=obj3, to=obj3)
    LinkPrediction.add(from_=obj2, to=obj4)
    LinkPrediction.add(from_=obj4, to=obj3)

graph = std.graphs.Graph(model, undirected=True)
Node, Edge = graph.Node, graph.Edge

Node.extend(Object)

with model.rule():
    r = LinkPrediction()
    Edge.add(r.from_, r.to)

for algo_name in ALGOS:
    with model.query(tag=algo_name) as select:
        o1 = Object(id=1)
        o2 = Object(id=2)
        o3 = Object(id=3)
        o4 = Object(id=4)
        algo1 = getattr(graph.compute, algo_name)(o1, o3)
        algo2 = getattr(graph.compute, algo_name)(o2, o4)
        select(o1, o3, algo1)
        select(o2, o4, algo2)
