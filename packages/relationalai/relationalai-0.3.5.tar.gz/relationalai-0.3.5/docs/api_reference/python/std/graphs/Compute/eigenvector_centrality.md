# `relationalai.std.graphs.Compute.eigenvector_centrality()`

```python
relationalai.std.graphs.Compute.eigenvector_centrality(node: Producer) -> Expression
```

Computes the eigenvector centrality of a node in an undirected graph.
Eigenvector centrality measures a node's significance in a graph,
taking into account not only its direct connections, but also the centrality of those connected nodes.
Nodes with high eigenvector centrality are important because they are connected to other important nodes.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

Directed graphs are not supported.
See [`.pagerank()`](./pagerank.md) for a similar measure that works with directed graphs.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | No | Not applicable to directed graphs.  |
| Undirected | Yes | See [Returns](#returns) for convergence criteria.  |
| Weighted | Yes | Weights must be non-negative. |
| Unweighted | Yes | Edge weights default to `1.0`. |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| node | [Producer](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the eigenvector centrality of the node as a floating-point value.

We use the [power iteration](https://en.wikipedia.org/wiki/Power_iteration) method, which:

- Requires the adjacency matrix to be symmetric.
- Only converges if the absolute values of the top two eigenvalues of the adjacency matrix are distinct.

## Example

Use `.eigenvector_centrality()` to compute the eigenvector centrality of a node in an undirected graph.
Directed graphs are not supported.

You access the `.eigenvector_centrality()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

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
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

with model.query() as select:
    # Get all person objects.
    person = Person()
    # Compute the eigenvector centrality of each person.
    centrality = graph.compute.eigenvector_centrality(person)
    # Select the each person's name and their eigenvector centrality.
    response = select(person.name, alias(centrality, "eigenvector_centrality"))

print(response.results)
# Output:
#      name  eigenvector_centrality
# 0   Alice                0.601501
# 1     Bob                0.371748
# 2   Carol                0.601501
# 3  Daniel                0.371748
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
    # Compute the eigenvector centrality of each object.
    # Objects that are not nodes in the graph are filtered out.
    centrality = graph.compute.eigenvector_centrality(obj)
    # Select the each object's name and their eigenvector centrality.
    response = select(obj.name, alias(centrality, "eigenvector_centrality"))

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#      name  eigenvector_centrality
# 0   Alice                0.601501
# 1     Bob                0.371748
# 2   Carol                0.601501
# 3  Daniel                0.371748
```

## See Also

[`.degree_centrality()`](./degree_centrality.md),
[`.weighted_degree_centrality()`](./weighted_degree_centrality.md),
and [`.pagerank()`](./pagerank.md).
