# `relationalai.std.graphs.Compute.distance()`

```python
relationalai.std.graphs.Compute.distance(node1: Producer, node2: Producer) -> Expression
```

Compute the shortest path length between two nodes in the graph.
Edge weights are ignored in weighted graphs.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

> [!NOTE]
> Be careful using `distance` on the entire graph, since for large graphs, this may be infeasible.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :--- |
| Undirected | Yes |   |
| Directed | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `node2` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the shortest path length between `node1` and `node2` as an integer value.

## Example

Use `.distance()` to compute the shortest path length between two nodes in a graph.
You access the `.distance()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued `follows` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    daniel = Person.add(name="Daniel")
    alice.follows.add(bob)
    bob.follows.add(carol)
    carol.follows.add(daniel)

# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by default.
# This graph has three edges: one from Alice to Bob, Bob to Carol, and Carol to Daniel.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Find the distance between Alice and Daniel.
with model.query() as select:
    dist = graph.compute.distance(Person(name="Alice"), Person(name="Daniel"))
    response = select(alias(dist, "distance"))

print(response.results)
# Output:
#    distance
# 0         3

# Find all nodes at distance at most two from Alice.
with model.query() as select:
    node = Person()
    dist = graph.compute.distance(Person(name="Alice"), node)
    dist <= 2
    response = select(node.name, alias(dist, "distance"))

print(response.results)
# Output:
#     name  distance
# 0  Alice         0
# 1    Bob         1
# 2  Carol         2
```

Note that the distance between a node and itself is `0`.

## See Also

[`.is_reachable()`](./is_reachable.md),
[`.reachable_from()`](./reachable_from.md),
and [`weighted_distance()`](./weighted_distance.md).
