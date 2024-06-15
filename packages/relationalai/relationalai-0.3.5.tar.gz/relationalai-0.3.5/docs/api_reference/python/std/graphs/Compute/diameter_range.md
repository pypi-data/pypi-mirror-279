# `relationalai.std.graphs.Compute.diameter_range()`

```python
relationalai.std.graphs.Compute.diameter_range() -> tuple[Expression, Expression]
```

Compute lower and upper bounds for the diameter of a graph.
The diameter is the length of the longest shortest path between any two nodes in the graph.
Edge weights are ignored in weighted graphs.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :--- |
| Undirected | Yes |   |
| Directed | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Returns

Returns a tuple of two [Expression](../../../Expression.md) objects that produce
the lower and upper bounds for the diameter of the graph.

The diameter range is computed by selecting a subset highest [degree](./degree.md) nodes
and, for each node, finding the length of the longest shortest path from that node to the rest of the graph.
The minimum and maximum of these lengths are returned as the lower and upper bounds of the diameter, respectively.

## Example

Use `.diameter_range()` to compute the range of possible diameters in a graph.
You access the `.diameter_range()` method from a [`Graph`](../Graph.md) object's
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
    carol = Person.add(name="Carol")
    alice.follows.add(bob)
    bob.follows.add(carol)

# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by default.
# This graph has edges from Alice to Bob and Bob to Carol.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Compute the diameter range of the graph.
with model.query() as select:
    diam_min, diam_max = graph.compute.diameter_range()
    response = select(alias(diam_min, "min"), alias(diam_max, "max"))

print(response.results)
# Output:
#    min  max
# 0    2    2
```

In cases like this where the lower and upper bounds are the same, the diameter of the graph is known exactly.
This may not always be the case, especially for larger and more complex graphs.

## See Also

[`.distance()`](./distance.md).
