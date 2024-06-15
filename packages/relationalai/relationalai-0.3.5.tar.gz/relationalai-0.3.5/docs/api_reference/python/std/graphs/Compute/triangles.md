# `relationalai.std.graphs.Compute.triangles()`

```python
relationalai.std.graphs.Compute.triangles(node: Producer | None = None) -> tuple[Expression, Expression, Expression]
```

Find all unique triangles in the graph.
A triangle is a set of three nodes `x`, `y`, and `z` such that
there is an edge between `x` and `y`, `y` and `z`, and `z` and `x`.
If `node` is not `None`, the unique triangles that `node` is part of are computed.
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
| `node` | [`Producer`](../../../Producer.md) or `None` | A node in the graph. If not `None`, the unique triangles that `node` is part of are computed. Otherwise, the total number of unique triangles in the graph is computed. Default is `None`. |

## Returns

Returns a tuple `(node1, node2, node3)` of three [Expression](../../../Expression.md) objects that produce
triples of nodes that form unique triangles in the graph.

For undirected graphs, triples are produced so that the nodes are ordered in ascending order by their internal identifiers.
In directed graphs, `.triangles()` produces triples of nodes such that `node1 < node2`, `node1 < node3`, and `node2 != node3`.
This ensures that each triangle is unique based on the ordering of nodes and edge directions.
For instance, `(1, 2, 3)` and `(1, 3, 2)` denote distinct directed triangles.

## Example

Use `.triangles()` to find all unique triangles in a graph.
You access the `.triangles()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued `follows` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    charlie = Person.add(name="Charlie")
    diana = Person.add(name="Diana")
    alice.follows.add(bob)
    bob.follows.add(charlie)
    charlie.follows.extend([alice, diana])
    diana.follows.add(bob)

# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by default.
graph = Graph(model)
graph.Edge.extend(Person.follows)

# Compute the unique triangles in the graph.
with model.query() as select:
    person1, person2, person3 = graph.compute.triangles()
    response = select(person1.name, person2.name, person3.name)
    
print(response.results)
# Output:
#       name  name2 name3
# 0  Charlie  Alice   Bob
# 1  Charlie  Diana   Bob

# Compute the unique triangles that include Alice.
with model.query() as select:
    alice = Person(name="Alice")
    person1, person2, person3 = graph.compute.triangles(alice)
    response = select(person1.name, person2.name, person3.name)

print(response.results)
# Output:
#       name  name2 name3
# 0  Charlie  Alice   Bob
```

## See Also

[`.is_triangle()`](./is_triangle.md) and [`.num_triangles()`](./num_triangles.md).
