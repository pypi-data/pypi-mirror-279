# `relationalai.std.graphs.Compute.num_triangles()`

```python
relationalai.std.graphs.Compute.num_triangles(node: Producer | None = None) -> Expression
```

Compute the number of unique triangles in the graph.
A triangle is a set of three nodes `x`, `y`, and `z` such that
there is an edge between `x` and `y`, `y` and `z`, and `z` and `x`.
If `node` is not `None`, the number of unique triangles that `node` is part of is computed.
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
| `node` | [`Producer`](../../../Producer.md) or `None` | A node in the graph. If not `None`, the number of unique triangles that `node` is part of is computed. Otherwise, the total number of unique triangles in the graph is computed. Default is `None`. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the number of unique triangles in the graph as an integer value, if `node` is `None`,
or the number of unique triangles that `node` is part of as an integer value, if `node` is not `None`.

## Example

Use `.num_triangles()` to compute the number of unique triangles in a graph.
You access the `.num_triangles()` method from a [`Graph`](../Graph.md) object's
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

# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by default.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Compute the number of unique triangles in the graph.
with model.query() as select:
    num_triangles = graph.compute.num_triangles()
    response = select(alias(num_triangles, "num_triangles"))
    
print(response.results)
# Output:
#    num_triangles
# 0              1

# Compute the number of unique triangles that each node is part of.
with model.query() as select:
    person = Person()
    num_triangles = graph.compute.num_triangles(person)
    response = select(person.name, alias(num_triangles, "num_triangles"))

print(response.results)
# Output:
#       name  num_triangles
# 0    Alice              1
# 1      Bob              1
# 2  Charlie              1
# 3    Diana              0
```

## See Also

[`.is_triangle()`](./is_triangle.md) and [`.triangles()`](./triangles.md).
