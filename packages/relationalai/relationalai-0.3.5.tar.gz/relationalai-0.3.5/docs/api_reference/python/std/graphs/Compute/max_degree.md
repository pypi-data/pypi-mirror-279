# `relationalai.std.graphs.Compute.max_degree()`

```python
relationalai.std.graphs.Compute.max_degree() -> Expression
```

Compute the maximum degree of all nodes a graph.
For an undirected graph, the degree of a node is the number of neighbors it has in the graph.
In a directed graph, the degree of a node is the sum of its [indegree](./indegree.md) and [outdegree](./outdegree.md).
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Returns

Returns an [Expression](../../../Expression.md) object that produces the maximum degree of the graph as an integer value.

## Example

Use `.max_degree()` to compute the maximum degree of a node in a graph.
You access the `.max_degree()` method from a [`Graph`](../Graph.md) object's
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

# Compute the maximum degree of the graph.
with model.query() as select:
    max_dgree = graph.compute.max_degree()
    response = select(max_dgree)
    
print(response.results)
# Output:
#    v
# 0  2
```

In directed graphs, the degree of a node is the sum of its [indegree](./indegree.md) and [outdegree](./outdegree.md):

```python
# Create a directed graph with Person  nodes and edges between friends.
# Note that graphs are directed by default.
# This graph has four edges: two between Alice and Bob and two between Alice and Carol.
directed_graph = Graph(model)
directed_graph.Node.extend(Person)
directed_graph.Edge.extend(Person.friends)

# Compute the maximum degree of the directed graph.
with model.query() as select:
    max_degree = directed_graph.compute.max_degree()
    response = select(max_degree)
    
print(response.results)
# Output:
#    v
# 0  4
```

## See Also

[`.degree()`](./degree.md), [`.min_degree()`](./min_degree.md), and [`.avg_degree()`](./avg_degree.md).
