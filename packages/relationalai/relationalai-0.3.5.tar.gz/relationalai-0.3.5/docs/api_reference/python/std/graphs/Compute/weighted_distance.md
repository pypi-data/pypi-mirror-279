# `relationalai.std.graphs.Compute.weighted_distance()`

```python
relationalai.std.graphs.Compute.weighted_distance(node1: Producer, node2: Producer) -> Expression
```

Compute the shortest path length between `node1` and `node2` in a weighted graph.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.
Alias for [`.distance()`](./distance.md) in unweighted graphs.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :--- |
| Undirected | Yes |   |
| Directed | Yes |   |
| Weighted | Yes | Only positive edge weights are supported. |
| Unweighted | Yes | Edge weights default to `1.0`.  |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `node2` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the shortest path length between `node1` and `node2` as a float value.

## Example

Use `.weighted_distance()` to compute the shortest path length between two nodes in a weighted graph.
You access the `.weighted_distance()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with Person and Friendship types.
model = rai.Model("socialNetwork")
Person = model.Type("Person")
Friendship = model.Type("Friendship")

# Add some people to the model and connect them with the Friendship type.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    daniel = Person.add(name="Daniel")
    Friendship.add(person1=alice, person2=bob, strength=1.0)
    Friendship.add(person1=bob, person2=carol, strength=0.5)
    Friendship.add(person1=carol, person2=daniel, strength=0.75)

# Create a directed graph with Person nodes and edges between friends.
# Note that graphs are directed by default.
# This graph has three edges: one from Alice to Bob, Bob to Carol, and Carol to Daniel.
# The edges are weighted by the strength of each friendship.
graph = Graph(model, weighted=True)
graph.Node.extend(Person)
with model.rule():
    friendship = Friendship()
    graph.Edge.add(friendship.person1, friendship.person2, weight=friendship.strength)

# Find the weighted distance between Alice and Daniel.
with model.query() as select:
    dist = graph.compute.weighted_distance(Person(name="Alice"), Person(name="Daniel"))
    response = select(alias(dist, "distance"))

print(response.results)
# Output:
#    distance
# 0      2.25

# Find all nodes with weighted distance at most two from Alice.
with model.query() as select:
    node = Person()
    dist = graph.compute.weighted_distance(Person(name="Alice"), node)
    dist <= 2.0
    response = select(node.name, alias(dist, "distance"))

print(response.results)
# Output:
#     name  distance
# 0  Alice       0.0
# 1    Bob       1.0
# 2  Carol       1.5
```

## See Also

[`distance()`](./distance.md),
[`.is_reachable()`](./is_reachable.md),
and [`.reachable_from()`](./reachable_from.md).
