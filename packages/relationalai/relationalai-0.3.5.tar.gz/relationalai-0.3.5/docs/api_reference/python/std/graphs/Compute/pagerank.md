# `relationalai.std.graphs.Compute.pagerank()`

```python
relationalai.std.graphs.Compute.pagerank(
    node: Producer,
    damping_factor: float = 0.85,
    tolerance: float = 1e-6,
    max_iter: int = 20
) -> Expression
```

Computes the PageRank centrality of a node in a graph.
PageRank measures a node's influence in a graph based on the quality and quantity of its inbound links.
Nodes with high PageRank values may be considered more influential than other nodes in the network.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Only positive weights are supported. |
| Unweighted | Yes | Edge weights default to `1.0`. |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `damping_factor` | `float` | The PageRank damping factor. Must be between `0.0` and `1.0`, inclusive. Default is `0.85.` |
| `tolerance` | `float` | The convergence tolerance for the PageRank algorithm. Default is `1e-6`. |
| `max_iter` | `int` | The maximum number of iterations allowed in the PageRank algorithm. Default is `20`. |

## Returns

Returns an [`Expression`](../../../Expression.md) object that produces
the PageRank centrality of the node as a floating-point value.

## Example

Use `.pagerank()` to compute the PageRank centrality of a node in a graph.

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued 'friends' property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    daniel = Person.add(name="Daniel")
    alice.friends.extend([bob, carol])
    carol.friends.add(daniel)

# Create an undirected graph with Person nodes and edges from people to their friends.
# This graph has three edges: one from Alice to Bob, Alice to Carol, and Carol to Daniel.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

with model.query() as select:
    # Get all person objects.
    person = Person()
    # Compute the PageRank of each person.
    pagerank = graph.compute.pagerank(person)
    # Select the each person's name and their PageRank value.
    response = select(person.name, alias(pagerank, "pagerank"))

print(response.results)
# Output:
#      name  pagerank
# 0   Alice  0.324562
# 1     Bob  0.175438
# 2   Carol  0.324562
# 3  Daniel  0.175438
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

with model.query() as select:
    # Get all person and company objects.
    obj = (Person | Company)()
    # Compute the PageRank of each object.
    # Objects that are not nodes in the graph are filtered out.
    pagerank = graph.compute.pagerank(obj)
    # Select the each object's name and their PageRank value.
    response = select(obj.name, alias(pagerank, "pagerank"))

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#      name  pagerank
# 0   Alice  0.324562
# 1     Bob  0.175438
# 2   Carol  0.324562
# 3  Daniel  0.175438
```

## See Also

[`.betweenness_centrality()`](./betweenness_centrality.md),
[`.degree_centrality()`](./degree_centrality.md),
[`.weighted_degree_centrality()`](./weighted_degree_centrality.md),
and [`.eigenvector_centrality()`](./eigenvector_centrality.md).
