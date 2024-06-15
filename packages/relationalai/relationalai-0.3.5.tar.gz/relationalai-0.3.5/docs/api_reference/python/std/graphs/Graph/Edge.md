# `relationalai.std.graphs.Graph.Edge`

An [`Edge`](../Edge/README.md) object that can be used to add and query edges in a graph.

## Example

`Graph.Edge` is an [`Edge`](../Edge/README.md) object.
Use its [`.add()`](../Edge/add.md) and [`.extend()`](../Edge/extend.md) methods to add edges to the graph:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model with a 'Person' and 'Message' types.
model = rai.Model("socialNetwork")
Person = model.Type("Person")
Message = model.Type("Message")

# Add people and messages to the model.
# People are connected by a multi-valued 'follows' property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    alice.follows.add(bob)
    Message.add(sender=alice, recipient=bob, text="Hey Bob!")

# Create a weighted, directed graph.
# Graphs are directed by default, so only the 'weighted' parameter is needed.
graph = Graph(model, weighted=True)

# Add edges using the 'Person.follows'. Person nodes are automatically added
# to the graph. The 'label' parameter is optional and sets the edge's label
# in the graph visualization.
graph.Edge.extend(Person.follows, label="follows")

# Alternatively, you can add specific edges in a rule using 'Edge.add()'.
# For example, this rule adds edges of type "message" between all senders and recipients.
with model.rule():
    message = Message()
    graph.Edge.add(from_=message.sender, to=message.recipient, label="message")

# You can query edges using `Graph.Edge`, which behaves like a 'Type' object.
# It returns an 'EdgeInstance' object that can be used to access the edge's
# properties. Use the 'from_' and 'to' properties to access the nodes at
# either end of the edge.
with model.query() as select:
    edge = graph.Edge()
    response = select(edge.from_.name, edge.to.name, alias(edge.label, "label"))

print(response.results)
# Output:
#     name name2        v
# 0  Alice   Bob  follows
# 1  Alice   Bob  message
```


## See Also

[`graphs.Edge`](../Edge/README.md),
[`graphs.EdgeInstance`](../EdgeInstance/README.md),
[`Graph`](./README.md),
and [`Node`](./Node.md).
