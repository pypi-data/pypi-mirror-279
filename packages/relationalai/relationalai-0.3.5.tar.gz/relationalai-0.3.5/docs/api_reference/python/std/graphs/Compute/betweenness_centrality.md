# `relationalai.std.graphs.Compute.betweenness_centrality()`

```python
relationalai.std.graphs.Compute.betweenness_centrality(node: Producer) -> Expression
```

Computes the [betweenness centrality](https://en.wikipedia.org/wiki/Betweenness_centrality) of a node.
Betweenness centrality measures the importance of a node
by counting how often it appears on the shortest paths between pairs of nodes in a graph.
Nodes with high betweenness centrality may play critical roles in the flow of information or resources through a network.
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
| node | [Producer](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the betweenness centrality of the node as a floating-point value.

## Example

Use `.betweenness_centrality()` to compute the betweenness centrality of a node in a graph.
You access the `.betweenness_centrality()` method from a [`Graph`](../Graph.md) object's
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
    alice.follows.extend([bob, carol])
    bob.follows.add(alice)
    carol.follows.add(alice)

# Create a directed graph with Person nodes and edge from people to the people they follow.
# Note that graphs are directed by default.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Compute the betweenness centrality of each person in the graph.
with model.query() as select:
    # Get all person objects.
    person = Person()
    # Compute the betweenness centrality of each person.
    centrality = graph.compute.betweenness_centrality(person)
    # Select the each person's name and their betweenness centrality.
    response = select(person.name, alias(centrality, "betweenness_centrality"))

print(response.results)
# Output:
#     name  betweenness_centrality
# 0  Alice                     2.0
# 1    Bob                     0.0
# 2  Carol                     0.0
```

If one of the objects produced by the `node` producer is not a node in the graph, no exception is raised.
Instead, that object is filtered from the [rule](../../../Model/rule.md) or [query](../../../Model/query.md):

```python
# Add a Company type to the model.
Company = model.Type("Company")

# Add some companies to the model.
with model.rule():
    apple = Company.add(name="Apple")
    google = Company.add(name="Google")

# Get the betweenness centrality of each person and company in the graph.
with model.query() as select:
    # Get all person and company objects.
    obj = (Person | Company)()
    # Compute the betweenness centrality of each object.
    # Objects that are not nodes in the graph are filtered out.
    centrality = graph.compute.betweenness_centrality(obj)
    # Select the each object's name and their betweenness centrality.
    response = select(obj.name, alias(centrality, "betweenness_centrality"))

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#     name  betweenness_centrality
# 0  Alice                     2.0
# 1    Bob                     0.0
# 2  Carol                     0.0
```

## See Also

[`.degree_centrality()`](./degree_centrality.md),
[`.weighted_degree_centrality()`](./weighted_degree_centrality.md),
[`eigenvector_centrality()`](./eigenvector_centrality.md),
and [`.pagerank()`](./pagerank.md).
