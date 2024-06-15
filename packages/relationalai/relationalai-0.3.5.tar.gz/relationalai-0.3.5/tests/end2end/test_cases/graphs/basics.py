import pytest

import relationalai as rai
from relationalai import std

# Query snapshots are output in same order as this list.
ALGOS = ["num_nodes", "num_edges"]

model = rai.Model(name=globals().get("name", ""), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    Relationship.add(from_=obj1, to=obj2)

graph = std.graphs.Graph(model)

# Make sure 'undirected' is set to False by default.
assert not graph.undirected

# Make sure 'weighted' is set to False by default.
assert not graph.weighted

# Make sure trying to set 'undirected' to True raises an error.
with pytest.raises(AttributeError):
    graph.undirected = True

# Make sure trying to set 'weighted' to True raises an error.
with pytest.raises(AttributeError):
    graph.weighted = True

# Add edges to the graph.
with model.rule():
    r = Relationship()
    graph.Edge.add(r.from_, r.to)

# Test each algorithm.
for algo_name in ALGOS:
    with model.query(tag=algo_name) as select:
        o = Object()
        # NOTE: This only works for unary relations.
        algo = getattr(graph.compute, algo_name)()
        select(algo)
