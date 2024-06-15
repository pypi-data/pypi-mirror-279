# `relationalai.std.graphs.Compute.weighted_degree_centrality()`

```python
relationalai.std.graphs.Compute.weighted_degree_centrality(node: Producer) -> Expression
```

Compute the weighted degree centrality of a node in a graph.
The weighted degree centrality of a node is the sum of the weights of the edges incident to the node
divided by one less than the number of nodes in the graph.
In unweighted graphs, `.weighted_degree_centrality()` is an alias of [`.degree_centrality()`](./degree_centrality.md).
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes |   |
| Unweighted | Yes | Edge weights default to `1.0`. |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [`Expression`](../../../Expression.md) object that produces
the weighted degree centrality of the node as a floating-point value, calculated according to the formula:

```
weighted_degree_centrality = sum(weight of edges incident to node) / (number of nodes - 1)
```

## Example

Use `.weighted_degree_centrality()` to compute the weighted degree centrality of a node in a graph.
You access the `.weighted_degree_centrality()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with Person and Friendship types.
model = rai.Model("socialNetwork")
Person = model.Type("Person")
Friendship = model.Type("Friendship")

# Add some people to the model and connect them with friendships.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    Friendship.add(person1=alice, person2=bob, strength=100)
    Friendship.add(person1=bob, person2=carol, strength=10)

# Create an weighted, undirected graph with Person nodes and edges between friends.
# This graph has two edges: one from Alice and Bob and one from Bob and Carol.
# The edges are weighted by the strength of each friendship.
graph = Graph(model, undirected=True, weighted=True)
graph.Node.extend(Person)
with model.rule():
    friendship = Friendship()
    graph.Edge.add(friendship.person1, friendship.person2, weight=friendship.strength)

# Compute the weighted degree centrality of each person in the graph.
with model.query() as select:
    person = Person()
    centrality = graph.compute.weighted_degree_centrality(person)
    response = select(person.name, alias(centrality, "weighted_degree_centrality"))

print(response.results)
# Output:
#     name  weighted_degree_centrality
# 0  Alice                        50.0
# 1    Bob                        55.0
# 2  Carol                         5.0
```

## See Also

[`.degree_centrality()`](./degree_centrality.md)
