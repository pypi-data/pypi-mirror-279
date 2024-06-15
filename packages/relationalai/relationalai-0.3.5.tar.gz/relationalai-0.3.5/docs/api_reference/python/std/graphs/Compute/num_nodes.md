# `relationalai.std.graphs.Compute.num_nodes()`

```python
relationalai.std.graphs.Compute.num_nodes() -> Expression
```

Get the number of nodes in the graph.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Returns

Returns an [Expression](docs/api_reference/python/Expression.md) that
produces the number of nodes in the graph as an integer value.

## Example

Use `.num_nodes()` to get the number of nodes in a graph.
You access the `.num_nodes()` method from a [`Graph`](../Graph.md) object's
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
    alice.friends.add(bob)
    bob.friends.add(alice)
    
# Create an undirected graph with Person nodes and edges between friends.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Get the number of nodes in the graph.
with model.query() as select:
    avg_degree = graph.compute.num_nodes()
    response = select(avg_degree)
    
print(response.results)
# Output:
#    v
# 0  2
```

## See Also

[`.num_edges()`](./num_edges.md)