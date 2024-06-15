# `relationalai.std.graphs.Compute.min_outdegree()`

```python
relationalai.std.graphs.Compute.min_outdegree() -> Expression
```

Compute the minimum outdegree of all nodes in a graph.
In a directed graph, the outdegree of a node is the number of edges that point away from the node.
For an undirected graph, `.min_outdegree()` is an alias of [`.min_degree()`](./min_degree.md).
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the minimum outdegree of the graph as an integer value.

## Example

Use `.min_outdegree()` to compute the minimum outdegree of a graph.
You access the `.min_outdegree()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the graph and connect them with a 'friends' property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    alice.friends.extend([bob, carol])
    bob.friends.add(alice)
    carol.friends.add(alice)
    
# Create an undirected graph with Person nodes and edges between friends.
# This graph has two edges: one between Alice and Bob and one between Alice and Carol.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Compute the minimum outdegree of the graph.
with model.query() as select:
    min_outdegree = graph.compute.min_outdegree()
    response = select(min_outdegree)
    
print(response.results)
# Output:
#    v
# 0  1
```

In directed graphs, `.min_outdegree()` is the same as [`.min_degree()`](./min_degree.md).

## See Also

[`.outdegree()`](./outdegree.md), [`.max_outdegree()`](./max_outdegree.md), and [`.avg_outdegree()`](./avg_outdegree.md).
