# `relationalai.std.graphs.Compute.max_indegree()`

```python
relationalai.std.graphs.Compute.max_indegree() -> Expression
```

Compute the maximum indegree of all nodes in a graph.
In a directed graph, the indegree of a node is the number of edges that point to the node.
For an undirected graph, `.max_indegree()` is an alias of [`.max_degree()`](./max_degree.md).
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
produces the maximum indegree of the graph as an integer value.

## Example

Use `.max_indegree()` to compute the maximum indegree of a graph.
You access the `.max_indegree()` method from a [`Graph`](../Graph.md) object's
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

# Compute the minimum indegree of the graph.
with model.query() as select:
    max_indegree = graph.compute.max_indegree()
    response = select(max_indegree)
    
print(response.results)
# Output:
#    v
# 0  1
```

In undirected graphs, `.max_indegree()` is the same as [`.max_degree()`](./max_degree.md).

## See Also

[`.indegree()`](./indegree.md), [`.min_indegree()`](./max_indegree.md), and [`.avg_indegree()`](./avg_indegree.md).
