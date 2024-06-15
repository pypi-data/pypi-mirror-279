# `relationalai.std.graphs.Edge.add()`

```python
relationalai.std.graphs.Edge.add(from_: Producer, to: Producer, **kwargs: Any) -> EdgeInstance
```

Adds edges to the graph from objects produced by `from_` to objects produced by `to`.
Edge properties may be passed as keyword arguments to `**kwargs`.
Objects produced by `from_` and `to` are automatically added to the graph's [nodes](../Graph/Node.md).
Must be called in a [rule](../Model/rule.md) or [query](../Model/query.md) context.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `from_` | [`Producer`](../../Producer.md) | The node at the start of the edge. |
| `to` | [`Producer`](../../Producer.md) | The node at the end of the edge. |
| `**kwargs` | `Any` | Keyword arguments to set the edge's properties. |

## Returns

An [`EdgeInstance`](../EdgeInstance/README.md) object.

## Example

Use `Edge.add()` to add edges to the graph:

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model with 'Person' and 'Transaction' types.
model = rai.Model("transactions")
Person = model.Type("Person")
Transaction = model.Type("Transaction")

# Add some people and transactions to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    Transaction.add(sender=bob, receiver=alice, amount=100.0)

# Create a directed graph.
graph = Graph(model)

# Add transactions to the graph as edges.
# The 'weight' parameter sets the weight property of each edge.
with model.rule():
    transaction = Transaction()
    graph.Edge.add(
        from_=transaction.sender,
        to=transaction.receiver,
        weight=transaction.amount
    )

# Query the edges in the graph.
with model.query() as select:
    edge = graph.Edge()
    response = select(edge.from_.name, edge.to.name, edge.weight)

print(response.results)
# Output:
#   name  name2      v
# 0  Bob  Alice  100.0
```

## See Also

[`.extend()`](./extend.md) and [`Graph.Edge`](../Graph/Edge.md).
