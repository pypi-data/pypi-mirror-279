# `relationalai.std.graphs.Compute.local_clustering_coefficient()`

```python
relationalai.std.graphs.Compute.local_clustering_coefficient(node: Producer) -> Expression
```

Compute the local clustering coefficient of a node in an undirected graph.
The local clustering coefficient of a node is the
fraction of pairs of the node's neighbors that are connected to another neighbor.
Values range from `0` to `1`, where `0` indicates none of the node's neighbors are connected,
and `1` indicates that the node's neighbors are fully connected, forming a clique.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

Directed graphs are not supported.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | No |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :---------- |
| `node` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the local clustering coefficient of `node` as a floating-point value, calculated by the following formula:

```
local clustering coefficient = 2 * num_edges / (degree * (degree - 1))
```

Here, `num_edges` is the total number of edges between the neighbors of `node`
and `degree` is the [degree](./degree.md) of `node`.
Values range from `0` to `1`, where `0` indicates none of the node's neighbors are connected,
and `1` indicates that the node's neighbors are fully connected, forming a clique.

## Example

Use `.local_clustering_coefficient()` to compute the local clustering coefficient of a node in an undirected graph.
You access the `.local_clustering_coefficient()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued `friend` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    daniel = Person.add(name="Daniel")
    alice.friends.extend([bob, carol])
    bob.friends.extend([alice, carol, daniel])

# Create an undirected graph with Person nodes and edges between friends.
# This graph has four edges: Alice, Bob, and Carol form a triangle, and Daniel is only connected to Bob.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Compute the local clustering coefficient of each person.
with model.query() as select:
    person = Person()
    lcc = graph.compute.local_clustering_coefficient(person)
    response = select(person.name, alias(lcc, "clustering_coefficient"))

print(response.results)
# Output:
#      name  clustering_coefficient
# 0   Alice                1.000000
# 1     Bob                0.333333
# 2   Carol                1.000000
# 3  Daniel                0.000000

# Compute the local clustering coefficient of a specific person.
with model.query() as select:
    lcc = graph.compute.local_clustering_coefficient(Person(name="Alice"))
    response = select(alias(lcc, "clustering_coefficient"))

print(response.results)
# Output:
#    clustering_coefficient
# 0                     1.0
```

## See Also

[`avg_clustering_coefficient()`](./avg_clustering_coefficient.md)
