# `relationalai.std.graphs.EdgeInstance.set()`

```python
EdgeInstance.set(**kwargs) -> EdgeInstance
```

Sets properties on an [`EdgeInstance`](./README.md) object and returns the `EdgeInstance`.
Note that unlike [`Instance.set()`](../../../Instance/set.md),
you can't set a [`Type`](../../../Type/README.md) on an edge.
Must be called in a [rule](../../Model/rule.md) or [query](../../Model/query.md) context.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `*kwargs` | `Any` | Properties and values to set on the `EdgeInstance`. |

## Returns

An [`EdgeInstance`](./README.md) object.

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

# Create a directed graph with 'Person' nodes and 'follows' edges.
graph = Graph(model)
graph.Edge.extend(Person.follows)

# Set the 'color' property of all edges to 'red'.
with model.rule():
    edge = graph.Edge()
    edge.set(color="red")

# Query the edges in the graph.
with model.query() as select:
    edge = graph.Edge()
    response = select(edge.from_.name, edge.to.name, edge.color)

print(response.results)
# Output:
#     name name2    v
# 0  Alice   Bob  red
```

## See Also

[`Edge.add()`](../Edge/add.md) and [`Edge.extend()`](../Edge/extend.md).
