# `relationalai.std.graphs.Compute.max_outdegree()`

```python
relationalai.std.graphs.Compute.max_outdegree() -> Expression
```

Compute the maximum outdegree of all nodes in a graph.
In a directed graph, the outdegree of a node is the number of edges that point away from the node.
For an undirected graph, `.max_outdegree()` is an alias of [`.max_degree()`](./max_degree.md).
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Returns

Returns an [Expression](../../../Expression.md) object that
produces the maximum outdegree of the graph as an integer value.

## Example

Use `.max_outdegree()` to compute the maximum outdegree of a graph.
You access the `.max_outdegree()` method from a [`Graph`](../Graph.md) object's
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
    max_outdegree = graph.compute.max_outdegree()
    response = select(max_outdegree)
    
print(response.results)
# Output:
#    v
# 0  1
```

In undirected graphs, `.max_outdegree()` is the same as [`.max_degree()`](./max_degree.md).

## See Also

[`.outdegree()`](./outdegree.md), [`.min_outdegree()`](./max_outdegree.md), and [`.avg_outdegree()`](./avg_outdegree.md).
