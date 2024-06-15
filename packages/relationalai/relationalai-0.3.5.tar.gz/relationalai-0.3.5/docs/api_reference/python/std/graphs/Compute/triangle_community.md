# `relationalai.std.graphs.Compute.triangle_community()`

```python
relationalai.std.graphs.Compute.triangle_community(node: Producer) -> Expression
```

Assign a community label to `node` using the percolation method.
The percolation method finds communities of densely connected nodes by identifying triangles in the graph
and iteratively merging triangles that share an edge until no more triangles can be merged.
Nodes that are not part of any triangles are excluded.
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
| :--- | :--- | :------ |
| `node` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the community label of `node` as an integer value.

## Example

Use `.triangle_community()` to assign a community label to a node in a graph.
You access the `.triangle_community()` method from a [`Graph`](../Graph.md) object's
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
    charlie = Person.add(name="Charlie")
    diana = Person.add(name="Diana")
    alice.follows.add(bob)
    bob.follows.add(charlie)
    charlie.follows.extend([alice, diana])

# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by default.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Find the community label for a single person using the percolation method.
with model.query() as select:
    community = graph.compute.triangle_community(Person(name="Alice"))
    response = select(alias(community, "community_label"))

print(response.results)
# Output:
#    community_label
# 0                1

# Compute the community label for each person in the graph.
with model.query() as select:
    person = Person()
    community = graph.compute.triangle_community(person)
    response = select(person.name, alias(community, "community_label"))

print(response.results)
# Output:
#     name  community_label
# 0  Alice                1
# 1    Bob                1
```

The above graph has edges from Alice to Bob, Bob to Charlie, Charlie to Alice, and Charlie to Diana.
Alice, Bob, and Charlie form a triangle, but Diana is not part of any triangles.
The percolation method assigns Alice and Bob to the same community.
Diana is filtered out because she is not part of any triangles.

Use [`std.aggregate.count()`](../../aggregate/count.md) to count the number of communities identified in the graph:

```python
from relationalai.std.aggregate import count

with model.query() as select:
    person = Person()
    community = graph.compute.triangle_community(person)
    response = select(alias(count(communities), "num_communities"))

print(response.results)
# Output:
#   num_communities
# 0               1
```

## See Also

[`.label_propagation()`](./label_propagation.md) and [`.louvain()`](./louvain.md).
