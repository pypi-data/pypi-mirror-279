# `relationalai.std.graphs.Compute.degree_centrality()`

```python
relationalai.std.graphs.Compute.degree_centrality(node: Producer) -> Expression
```

Computes the degree centrality of a node.
Degree centrality measures the importance of a node based on its [degree](./degree.md).
Nodes with high degree centrality are well-connected in the graph.
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
the degree centrality of the node as a floating-point value, calculated by the following formula:

```
degree centrality = degree of the node / (total number of nodes - 1)
```

This value is at most `1.0` for simple graphs with no self loops.
In graphs with self loops, a node's degree centrality can exceed `1.0`.

## Example

Use `.degree_centrality()` to compute the degree centrality of a node in a graph.
You access the `.degree_centrality()` method from a [`Graph`](../Graph.md) object's
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

# Compute the degree centrality of each person in the graph.
with model.query() as select:
    # Get all person objects.
    person = Person()
    # Compute the degree centrality of each person.
    centrality = graph.compute.degree_centrality(person)
    # Select the each person's name and their degree centrality.
    response = select(person.name, alias(centrality, "degree_centrality"))

print(response.results)
# Output:
#     name  degree_centrality
# 0  Alice                2.0
# 1    Bob                1.0
# 2  Carol                1.0
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

# Get the degree centrality of each person and company in the graph.
with model.query() as select:
    # Get all person and company objects.
    obj = (Person | Company)()
    # Compute the degree centrality of each object.
    # Objects that are not nodes in the graph are filtered out.
    centrality = graph.compute.degree_centrality(obj)
    # Select the each object's name and their degree centrality.
    response = select(obj.name, alias(centrality, "degree_centrality"))

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#     name  degree_centrality
# 0  Alice                2.0
# 1    Bob                1.0
# 2  Carol                1.0
```

## See Also

[`.weighted_degree_centrality()`](./weighted_degree_centrality.md),
[`.betweenness_centrality()`](./betweenness_centrality.md),
[`eigenvector_centrality()`](./eigenvector_centrality.md),
and [`.pagerank()`](./pagerank.md).
