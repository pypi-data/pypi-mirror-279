# `relationalai.std.graphs.Compute.avg_clustering_coefficient()`

```python
relationalai.std.graphs.Compute.avg_clustering_coefficient() -> Expression
```

Compute the average clustering coefficient of all nodes in an undirected graph.
The average clustering coefficient is the average of the
[local clustering coefficients](./local_clustering_coefficient.md) for each node in the graph.
Values range from `0` to `1`.
Higher average clustering coefficients indicate nodes' increased tendency to form triangles with neighbors.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

Directed graphs are not supported.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | No |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the average clustering coefficient of all nodes in the graph as a floating-point value.

## Example

Use `.avg_clustering_coefficient()` to compute the average clustering coefficient of all nodes in an undirected graph.
You access the `.avg_clustering_coefficient()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued `friend` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    daniel = Person.add(name="Daniel")
    alice.friends.extend([bob, carol])
    bob.friends.extend([alice, carol, daniel])

# Create an undirected graph with Person nodes and edges between friends.
# This graph has four edges: Alice, Bob, and Carol form a triangle, and Daniel is only connected to Bob.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Compute the average clustering coefficient of the graph.
with model.query() as select:
    acc = graph.compute.avg_clustering_coefficient()
    response = select(alias(acc, "avg_clustering_coefficient"))

print(response.results)
# Output:
#    avg_clustering_coefficient
# 0                    0.583333
```

## See Also

[`local_clustering_coefficient()`](./local_clustering_coefficient.md)
