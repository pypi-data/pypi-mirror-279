# `relationalai.std.graphs.Edge.extend()`

```python
relationalai.std.graphs.Edge.extend(prop: Property, **kwargs: Any) -> None
```

Add pairs of objects from a [`Property`](../../../Property.md) to a graph's edges.
Edge properties may be passed as keyword arguments to `**kwargs`.
Objects produced by the property are automatically added to the graph's [nodes](../Graph/Node.md).

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `prop` | `Property` | The property to extend the graph's edges with. |
| `**kwargs` | `Any` | Keyword arguments to set the edge's properties. |

## Returns

`None`.

## Example

Use `Edge.extend()` to add edges to the graph from a property.
You do not need to call `.extend()` in a [rule](../Model/rule.md) or [query](../Model/query.md) context.

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

# Extend the graph's edges with the 'Person.follows' property.
graph.Edge.extend(Person.follows)

# Query the edges in the graph.
with model.query() as select:
    edge = graph.Edge()
    response = select(edge.from_.name, edge.to.name)

print(response.results)
# Output:
#     name name2
# 0  Alice   Bob
```

## See Also

[`.add()`](./add.md) and [`Graph.Edge`](../Graph/Edge.md).
