# `relationalai.std.graphs.Compute.is_reachable()`

```python
relationalai.std.graphs.Compute.is_reachable(node1: Producer, node2: Producer) -> Expression
```

Check if `node2` is reachable from `node1` in the graph.
One node is reachable from another if there is a path from the first node to the second.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :---------- |
| `node1` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `node2` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) that filters pairs of
nodes in which there is a path from `node1` to `node2`.

## Example

Use `.is_reachable()` to check if one node is reachable from another in a graph.
You access the `.is_reachable()` method from a [`Graph`](../Graph.md) object's
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
    alice.follows.add(bob)
    bob.follows.add(carol)

# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by default.
# This graph has edges from Alice to Bob and Bob to Carol.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Can Alice reach Carol?
with model.query() as select:
    alice = Person(name="Alice")
    carol = Person(name="Carol")
    with model.match() as reachable:
        with model.case():
            graph.compute.is_reachable(alice, carol)
            reachable.add(True)
        with model.case():
            reachable.add(False)
    response = select(alias(reachable, "is_reachable"))

print(response.results)
# Output:
#    is_reachable
# 0          True

# Who can reach Alice?
with model.query() as select:
    person = Person()
    graph.compute.is_reachable(person, Person(name="Alice"))
    response = select(person.name)

# No one, since all edges point away from Alice.
print(response.results)
# Output:
# Empty DataFrame
# Columns: []
# Index: []
```

To find all nodes reachable from a given node, use [`.reachable_from()`](./reachable_from.md).
Use [`.distance()`](./distance.md) to find the shortest path length between two nodes.

## See Also

[`.distance()`](./distance.md) and [`.reachable_from()`](./reachable_from.md).
