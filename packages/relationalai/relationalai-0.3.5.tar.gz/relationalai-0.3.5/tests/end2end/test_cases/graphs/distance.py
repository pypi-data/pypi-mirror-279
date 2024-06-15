import relationalai as rai
from relationalai import std

# Query snapshots are output in same order as this list.
UNWEIGHTED_ALGOS = [
    "distance",
]

WEIGHTED_ALGOS = ["weighted_distance"]

UNARY_ALGOS = ["diameter_range"]

model = rai.Model(
    name=globals().get("name", "test_distance"), config=globals().get("config")
)
Object = model.Type("Object")
Distance = model.Type("Distance")
Range = model.Type("Range")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    obj3 = Object.add(id=3)
    obj4 = Object.add(id=4)
    Distance.add(from_=obj1, to=obj2, weight=10)
    Distance.add(from_=obj2, to=obj3, weight=20)
    Distance.add(from_=obj3, to=obj3, weight=30)
    Distance.add(from_=obj2, to=obj4, weight=40)
    Distance.add(from_=obj4, to=obj3, weight=50)

undirected_graph = std.graphs.Graph(model, undirected=True)

with model.rule():
    d = Distance()
    undirected_graph.Edge.add(d.from_, d.to)

for algo_name in UNWEIGHTED_ALGOS:
    with model.query() as select:
        o1 = Object(id=1)
        o2 = Object(id=2)
        o3 = Object(id=3)
        o4 = Object(id=4)
        algo1 = getattr(undirected_graph.compute, algo_name)(o1, o3)
        algo2 = getattr(undirected_graph.compute, algo_name)(o2, o4)
        select(o1, o3, algo1)
        select(o2, o4, algo2)

weighted_graph = std.graphs.Graph(model, undirected=True, weighted=True)

with model.rule():
    d = Distance()
    weighted_graph.Edge.add(d.from_, d.to, weight=d.weight)

for algo_name in WEIGHTED_ALGOS:
    with model.query() as select:
        o1 = Object(id=1)
        o2 = Object(id=2)
        o3 = Object(id=3)
        o4 = Object(id=4)
        algo1 = getattr(weighted_graph.compute, algo_name)(o1, o3)
        algo2 = getattr(weighted_graph.compute, algo_name)(o2, o4)
        select(o1, o3, algo1)
        select(o2, o4, algo2)

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    obj3 = Object.add(id=3)
    obj4 = Object.add(id=4)
    Range.add(from_=obj1, to=obj2)
    Range.add(from_=obj3, to=obj2)
    Range.add(from_=obj4, to=obj3)

unary_graph = std.graphs.Graph(model, undirected=True)

with model.rule():
    r = Range()
    unary_graph.Edge.add(r.from_, r.to)

for algo_name in UNARY_ALGOS:
    with model.query() as select:
        algo = getattr(unary_graph.compute, algo_name)()
        response = select(algo)
