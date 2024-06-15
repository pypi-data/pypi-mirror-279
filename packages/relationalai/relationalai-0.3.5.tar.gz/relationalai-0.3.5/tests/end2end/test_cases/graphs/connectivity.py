import relationalai as rai 
from relationalai import std


model = rai.Model(name=globals().get("name", ""), config=globals().get("config"))
Object = model.Type("Object")
Relationship = model.Type("Relationship")

with model.rule():
    obj1 = Object.add(id=1)
    obj2 = Object.add(id=2)
    Relationship.add(from_=obj1, to=obj2)

disconnected_graph = std.graphs.Graph(model)
disconnected_graph.Node.extend(Object)

connected_graph = std.graphs.Graph(model)
with model.rule():
    r = Relationship()
    connected_graph.Edge.add(r.from_, r.to)

# Check that is_connected works
with model.query() as select:
    with model.match() as connected:
        with connected_graph.compute.is_connected():
            connected.add(True)
        with model.case():
            connected.add(False)
    with model.match() as disconnected:
        with disconnected_graph.compute.is_connected():
            disconnected.add(True)
        with model.case():
            disconnected.add(False)
    select(connected, disconnected)

# Check that reachable_from works
with model.query() as select:
    n = Object()
    reachable_from_n = connected_graph.compute.reachable_from(n)
    select(n, reachable_from_n)

# Check that is_reachable works
with model.query() as select:
    n1 = Object(id=1)
    n2 = Object(id=2)
    with model.match() as reachable1:
        with model.case():
            connected_graph.compute.is_reachable(n1, n2)
            reachable1.add(True)
        with model.case():
            reachable1.add(False)
    with model.match() as reachable2:
        with model.case():
            connected_graph.compute.is_reachable(n2, n1)
            reachable2.add(True)
        with model.case():
            reachable2.add(False)
    select(reachable1, reachable2)
