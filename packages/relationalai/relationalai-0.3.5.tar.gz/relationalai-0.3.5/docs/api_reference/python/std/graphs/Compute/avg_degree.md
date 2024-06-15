# `relationalai.std.graphs.Compute.avg_degree()`

```python
relationalai.std.graphs.Compute.avg_degree() -> Expression
```

Get the average degree of all nodes the graph.
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

Returns an [Expression](../../../Expression.md) object
that produces the average degree of the graph as a floating-point value.

## Example

Use `.avg_degree()` to compute the average degree of a graph:

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

# Compute the average degree of the graph.
with model.query() as select:
    avg_degree = graph.compute.avg_degree()
    response = select(avg_degree)
    
print(response.results)
# Output:
#           v
# 0  1.333333
```

In directed graphs, the degree of a node is the sum of its [indegree](./indegree.md) and [outdegree](./outdegree.md):

```python
# Create a directed graph with Person  nodes and edges between friends.
# Note that graphs are directed by default.
# This graph has four edges: two between Alice and Bob and two between Alice and Carol.
directed_graph = Graph(model)
directed_graph.Node.extend(Person)
directed_graph.Edge.extend(Person.friends)

# Compute the average degree of the directed graph.
with model.query() as select:
    avg_degree = directed_graph.compute.avg_degree()
    response = select(avg_degree)
    
print(response.results)
# Output:
#           v
# 0  2.666667
```

## See Also

[`.degree()`](./degree.md), [`.max_degree()`](./max_degree.md), and [`.avg_degree()`](./avg_degree.md).
