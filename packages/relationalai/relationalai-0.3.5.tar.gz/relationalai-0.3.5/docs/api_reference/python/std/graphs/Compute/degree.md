# `relational.std.graphs.Compute.degree()`

```python
relationalai.std.graphs.Compute.degree(node: Producer) -> Expression
```

Compute the degree of a node.
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

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| node | [Producer](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces the degree of the node as an integer value.

## Example

Use `.degree()` to compute the degree of a node in a graph.
You access the `.degree()` method from a [`Graph`](../Graph.md) object's
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
# This graph has one edge between Alice and Bob.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Get the number of nodes in the graph.
with model.query() as select:
    # Get all Person objects.
    person = Person()
    # Compute the degree of each person.
    degree = graph.compute.degree(person)
    # Select the name of each person and their degree.
    response = select(person.name, degree)
    
print(response.results)
# Output:
#     name  v
# 0  Alice  1
# 1    Bob  1
```

In directed graphs, the degree of a node is the sum of its [indegree](./indegree.md) and [outdegree](./outdegree.md):

```python
# Create a directed graph with Person  nodes and edges between friends.
# Note that graphs are directed by default.
# This graph has two edges. One from Alice to Bob and one from Bob to Alice.
directed_graph = Graph(model)
directed_graph.Node.extend(Person)
directed_graph.Edge.extend(Person.friends)

# Get the degree of each person in the graph.
with model.query() as select:
    person = Person()
    degree = directed_graph.compute.degree(person)
    response = select(person.name, degree)

print(response.results)
# Output:
#     name  v
# 0  Alice  2
# 1    Bob  2
```

## See Also

[`min_degree()`](./min_degree.md),
[`max_degree()`](./max_degree.md),
[`avg_degree()`](./avg_degree.md),
[`.indegree()`](./indegree.md),
and [`.outdegree()`](./outdegree.md).
