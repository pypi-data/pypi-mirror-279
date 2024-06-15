import relationalai as rai
from relationalai import std

# Query snapshots are output in same order as these lists.
NO_ARGS = [
    "num_triangles",
    "triangles",
]

ONE_ARG = [
    "num_triangles", # included here because of optional 'node' parameter
    "triangles", # included here because of optional 'node' parameter
]

THREE_ARGS = [
    "is_triangle",
]

model = rai.Model(name=globals().get("name", "test_triangles"), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

# Create a graph with 4 nodes and 4 edges, forming a triangle with a dangling node.
with model.rule(dynamic=True):
    object = [Object.add(id=i) for i in range(4)]
    for i in range(3):
        Relationship.add(from_=object[i], to=object[(i + 1) % 3])
    Relationship.add(from_=object[0], to=object[3])

graph = std.graphs.Graph(model, undirected=True)

with model.rule():
    r = Relationship()
    graph.Edge.add(r.from_, r.to)

for algo_name in NO_ARGS:
    with model.query(dynamic=True) as select:
        algo = getattr(graph.compute, algo_name)()
        if isinstance(algo, tuple):
            select(*algo)
        else:
            select(algo)

for algo_name in ONE_ARG:
    with model.query(dynamic=True) as select:
        o = Object()
        algo = getattr(graph.compute, algo_name)(o)
        if isinstance(algo, tuple):
            select(o.id, *algo)
        else:
            select(o.id, algo)

for algo_name in THREE_ARGS:
    with model.query(dynamic=True) as select:
        o1, o2, o3 = Object(), Object(), Object()
        o1.id < o2.id < o3.id
        algo = getattr(graph.compute, algo_name)(o1, o2, o3)
        if isinstance(algo, tuple):
            select(o1.id, o2.id, o3.id, *algo)
        else:
            select(o1.id, o2.id, o3.id, algo)
