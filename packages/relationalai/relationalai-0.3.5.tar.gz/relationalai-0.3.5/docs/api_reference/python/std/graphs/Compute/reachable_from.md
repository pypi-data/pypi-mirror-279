# `relationalai.std.graphs.Compute.reachable_from()`

```python
relationalai.std.graphs.Compute.reachable_from(node: Producer) -> Expression
```

Find all nodes reachable from `node` in a graph.
One node is reachable from another if there is a path from the first node to the second.
Nodes with self-loops are considered to be reachable from themselves.
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
| `node` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
[model](../../../Model/README.md) objects that are reachable from `node`.

## Example

Use `.reachable_from()` to find all nodes reachable from a node in a graph.
You access the `.reachable_from()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
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

# Who is reachable from Alice?
with model.query() as select:
    reachable = graph.compute.reachable_from(Person(name="Alice"))
    response = select(reachable.name)

print(response.results)
# Output:
#     name
# 0    Bob
# 1  Carol
```

In the example above, both Bob and Carol are reachable from Alice
because there is a path from Alice to Bob and a path from Alice to Carol that passes through Bob.
Alice is not reachable from herself because her node has no self-loop.

To check if one node is reachable from another, use [`.is_reachable()`](./is_reachable.md).
Use [`.distance()`](./distance.md) to find the shortest path length between two nodes.

## See Also

[`.is_reachable()`](./is_reachable.md) and [`.distance()`](./distance.md).
