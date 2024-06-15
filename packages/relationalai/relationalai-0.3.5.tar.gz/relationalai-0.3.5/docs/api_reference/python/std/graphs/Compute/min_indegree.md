# `relationalai.std.graphs.Compute.min_indegree()`

```python
relationalai.std.graphs.Compute.min_indegree() -> Expression
```

Compute the minimum indegree of all nodes in a graph.
In a directed graph, the indegree of a node is the number of edges that point to the node.
For an undirected graph, `.min_indegree()` is an alias of [`.min_degree()`](./min_degree.md).
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Returns

Returns an [Expression](../../../Expression.md) object that produces the minimum indegree of the graph as an integer value.

## Example

Use `.min_indegree()` to compute the minimum indegree of a graph.
You access the `.min_indegree()` method from a [`Graph`](../Graph.md) object's
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
    min_indegree = graph.compute.min_indegree()
    response = select(min_indegree)
    
print(response.results)
# Output:
#    v
# 0  1
```

In undirected graphs, `.min_indegree()` is the same as [`.min_degree()`](./min_degree.md).

## See Also

[`.indegree()`](./indegree.md), [`.max_indegree()`](./max_indegree.md), and [`.avg_indegree()`](./avg_indegree.md).
