# `relational.std.graphs.Compute.outdegree()`

```python
relationalai.std.graphs.Compute.outdegree(node: Producer) -> Expression
```

Compute the outdegree of a node in the graph.
In a directed graph, the outdegree of a node is the number of edges that point away from the node.
For an undirected graph, `.outdegree()` is an alias of [`.degree()`](./degree.md).
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| node | [Producer](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces the outdegree of the node as an integer value.

## Example

Use `.outdegree()` to compute the outdegree of a node in a graph.
You access the `.outdegree()` method from a [`Graph`](../Graph.md) object's
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
    
# Create a directed graph with Person nodes and edges between friends.
# Note that graphs are directed by default.
# This graphs has two edges: one from Alice to Bob and one from Bob to Alice.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Get the number of nodes in the graph.
with model.query() as select:
    # Get all Person objects.
    person = Person()
    # Compute the outdegree of each person.
    outdegree = graph.compute.outdegree(person)
    # Select the name of each person and their outdegree.
    response = select(person.name, outdegree)
    
print(response.results)
# Output:
#     name  v
# 0  Alice  1
# 1    Bob  1
```

In undirected graphs, [`.outdegree()`](./outdegree.md) is same as [`.degree()`](./degree.md).

## See Also

[`min_outdegree()`](./min_outdegree.md),
[`max_outdegree()`](./max_outdegree.md),
[`avg_outdegree()`](./avg_outdegree.md),
[`.degree()`](./degree.md),
and [`.outdegree()`](./outdegree.md).
