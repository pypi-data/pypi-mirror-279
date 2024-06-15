import pytest
import relationalai as rai
from relationalai import std
from relationalai.errors import RAIException

# Query snapshots are output in same order as this list.
ALGOS = [
    "louvain",
    "weakly_connected_component",
    "triangle_community",  # Expects empty dataframe b/c graph has no triangles.
    "infomap",
    "label_propagation",
]

model = rai.Model(name=globals().get("name", "test_community"), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    obj3 = Object.add(id=3)
    Relationship.add(from_=obj1, to=obj2)

graph = std.graphs.Graph(model, undirected=True)
graph.Node.extend(Object)

with model.rule():
    r = Relationship()
    graph.Edge.add(r.from_, r.to)

for algo_name in ALGOS:
    with model.query(tag=algo_name) as select:
        o = Object()
        algo = getattr(graph.compute, algo_name)(o)
        select(o, algo)


# Check that exceptions are raised when invalid parameters are passed.
PARAMETERS = {
    "infomap": {
        "max_levels": [-1, 0, -1.23, 0.0, 1.23, "a", []],
        "max_sweeps": [-1, -1.23, 0.0, 1.23, "a", []],
        "level_tolerance": [-1.0, -1, "a", []],
        "sweep_tolerance": [-1.0, -1, "a", []],
        "teleportation_rate": [-1.0, -1, 0.0, 0, 1.0001, 2, "a", []],
        "visit_rate_tolerance": [-1.0, -1, 0.0, 0, "a", []],
        "randomization_seed": [-1, 1.23, "a", []],
    },
    "label_propagation": {
        "max_sweeps": [-1, -1.23, 0.0, 1.23, "a", []],
        "randomization_seed": [-1, 1.23, "a", []],
    },
    "louvain": {
        "max_levels": [-1, 0, -1.23, 0.0, 1.23, "a", []],
        "max_sweeps": [-1, -1.23, 0.0, 1.23, "a", []],
        "level_tolerance": [-1.0, -1, "a", []],
        "sweep_tolerance": [-1.0, -1, "a", []],
        "randomization_seed": [-1, 1.23, "a", []],
    },
}
with model.query(dynamic=True):
    o = Object()
    for algo_name, params in PARAMETERS.items():
        for param_name, values in params.items():
            for value in values:
                with pytest.raises(RAIException):
                    getattr(graph.compute, algo_name)(o, **{param_name: value})
