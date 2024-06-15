<!-- markdownlint-disable MD024 -->

# `relationalai.std.graphs.EdgeInstance`

```python
class relationalai.std.graphs.EdgeInstance
```

`EdgeInstance` is a subclass of [`Producer`](../Producer/README.md) that produces edges in a graph.
They are created by called a graph's [`Edge`](../Graph/Edge.md) object or the [`Edge.add()`](../Graph/Edge/add.md) method.
An `EdgeInstance` is similar to an [`Instance`](../Instance/README.md),
but rather than representing an object, it represents a pairs of objects.
As a result, you can't add `EdgeInstance` objects to a [`Type`](../../../Type/README.md).

## Attributes

| Name | Type | Description |
| :--- | :--- | :------ |
| [`.from_`](./from_.md) | [`Producer`](../../Producer.md) | The node at the start of the edge. |
| [`.to`](./to.md) | [`Producer`](../../Producer.md) | The node at the end of the edge. |

## Methods

| Name | Description | Returns |
| :--- | :------ | :------ |
| [`.set()`](./set.md) | Set properties on an edge. | [`EdgeInstance`](./README.md) |

## Example

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model with a 'Person' type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add people to the model connected by a multi-valued 'follows' property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    alice.follows.add(bob)

# Create a directed graph.
graph = Graph(model)

# Add edges to the graph from the 'Person.follows' property.
graph.Edge.extend(Person.follows, type="follows")

# Query the edges in the graph.
with model.query() as select:
    # 'edge' is an EdgeInstance object.
    edge = graph.Edge()
    # Use the '.from_' and '.to' attributes to access the nodes
    # connected by the edge, and the '.type' attribute to access
    # the edge's 'type' property.
    response = select(edge.from_.name, edge.to.name, edge.type)

print(response.results)
# Output:
#     name name2        v
# 0  Alice   Bob  follows

# Use the '.set()' method to set properties on an edge.
with model.rule():
    edge = graph.Edge()
    # Set the 'weight' property of all edges to 1.0.
    edge.set(weight=1.0)
    # NOTE: Setting the 'weight' property does not turn the graph
    # into a weighted graph. You can only create a weighted graph
    # by passing 'weighted=True' to the 'Graph' constructor.

# Query the edges in the graph.
with model.query() as select:
    edge = graph.Edge()
    response = select(edge.from_.name, edge.to.name, edge.weight)

print(response.results)
# Output:
#     name name2    v
# 0  Alice   Bob  1.0
```

## See Also

[`Graph`](../Graph/README.md) and [`Edge`](../Edge/README.md).
