# `relational.std.graphs.Compute.indegree()`

```python
relationalai.std.graphs.Compute.indegree(node: Producer) -> Expression
```

Compute the indegree of a node.
In a directed graph, the indegree of a node is the number of edges that point to the node.
For an undirected graph, `.indegree()` is an alias of [`.degree()`](./degree.md).
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

Returns an [Expression](../../../Expression.md) object that produces the indegree of the node as an integer value.

## Example

Use `.indegree()` to compute the indegree of a node in a graph.
You access the `.indegree()` method from a [`Graph`](../Graph.md) object's
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
    # Compute the indegree of each person.
    indegree = graph.compute.indegree(person)
    # Select the name of each person and their indegree.
    response = select(person.name, indegree)
    
print(response.results)
# Output:
#     name  v
# 0  Alice  1
# 1    Bob  1
```

For an undirected graph, `.indegree()` is same as [`.degree()`](./degree.md).

## See Also

[`min_indegree()`](./min_indegree.md),
[`max_indegree()`](./max_indegree.md),
[`avg_indegree()`](./avg_indegree.md),
[`.degree()`](./degree.md),
and [`.outdegree()`](./outdegree.md).
