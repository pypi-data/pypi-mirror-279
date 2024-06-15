# `relationalai.std.graphs.Edge.__call__()`

```python
relationalai.std.graphs.Edge.__call__(
    from_: Producer | None = None,
    to: Prodcuer | None = None,
    **kwargs
) -> EdgeInstance
```

Returns an [`EdgeInstance`](../EdgeInstance/README.md) object that produces edges from the graph.
Use the optional `from_` and `to` arguments to filter edges by the nodes they connect.
Must be called in a [rule](../Model/rule.md) or [query](../Model/query.md) context.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `from_` | [`Producer`](../../Producer.md) | The initial node of the edge. If `None`, the edge can start from any node. |
| `to` | [`Producer`](../../Producer.md) | The terminal node of the edge. If `None`, the edge can end at any node. |
| `**kwargs` | `Any` | Keyword arguments to filter edges by their properties. |

## Returns

An [`EdgeInstance`](../EdgeInstance/README.md) object.

## Example

Call an `Edge` object in a [rule](../Model/rule.md) or [query](../Model/query.md) context
to get an [`EdgeInstance`](../EdgeInstance/README.md) object that produces the graph's edges:

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
    carol = Person.add(name="Carol")
    Transaction.add(sender=alice, receiver=bob, amount=50.0)
    Transaction.add(sender=bob, receiver=alice, amount=100.0)
    Transaction.add(sender=alice, receiver=carol, amount=200.0)

# Create a weighted, directed graph from the model.
graph = Graph(model, weighted=True)

# Add edges to the graph from the 'Transaction' type.
with model.rule():
    transaction = Transaction()
    graph.Edge.add(
        from_=transaction.sender,
        to=transaction.receiver,
        weight=transaction.amount
    )

# Query all edges in the graph.
with model.query() as select:
    edge = graph.Edge()
    response = select(edge.from_.name, edge.to.name, edge.weight)

print(response.results)
# Output:
#     name  name2      v
# 0  Alice    Bob   50.0
# 1  Alice  Carol  200.0
# 2    Bob  Alice  100.0

# Use the 'from_' and 'to' properties to filter edges by
# the nodes they connect. For example, to get all edges
# starting from Alice:
with model.query() as select:
    edge = graph.Edge(from_=Person(name="Alice"))
    response = select(edge.to.name, edge.weight)

print(response.results)
# Output:
#     name      v
# 0    Bob   50.0
# 1  Carol  200.0

# To get all edges ending at Alice:
with model.query() as select:
    edge = graph.Edge(to=Person(name="Alice"))
    response = select(edge.from_.name, edge.weight)

print(response.results)
# Output:
#   name      v
# 0  Bob  100.0

# To get all edges between Alice and Bob:
with model.query() as select:
    edge = graph.Edge(
        from_=Person(name="Alice"),
        to=Person(name="Bob")
    )
    response = select(edge.weight)

print(response.results)
# Output:
#       v
# 0  50.0

# You can also filter edges by their properties. For example,
# to get all transactions with an amount equal to 100.0:
with model.query() as select:
    edge = graph.Edge(weight=100.0)
    response = select(edge.from_.name, edge.to.name)

print(response.results)
# Output:
#   name  name2
# 0  Bob  Alice
```

## See Also

[`EdgeInstance`](../EdgeInstance/README.md)
