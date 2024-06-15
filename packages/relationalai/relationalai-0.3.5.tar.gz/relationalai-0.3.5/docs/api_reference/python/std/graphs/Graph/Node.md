# `relationalai.std.graphs.Graph.Node`

A [`Type`](../../../Type/README.md) object representing the set of nodes in a graph.

## Example

`Graph.Node` is a [`Type`](../../../Type/README.md) object.
Use its [`.add()`](../../../Type/add.md) and [`.extend()`](../../../Type/extend.md)
methods to add nodes to the graph:

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model with a `Person` type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add people to the model connected by a multi-valued 'follows' property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    alice.follows.add(bob)

# Create a directed graph.
graph = Graph(model)

# Add all 'Person' objects to the graph's nodes using 'Node.extend()'.
# The 'label' parameter is optional and sets the node's label in the graph visualization.
graph.Node.extend(Person, label=Person.name)

# Alternatively, you can add specific nodes in a rule using 'Node.add()'.
# For example, this rule adds all of Bob's followers to the graph.
with model.rule():
    person = Person()
    person.follows == Person(name="Bob")
    graph.Node.add(person, label=person.name)

# You can query the nodes the same way you query any other `Type` object.
with model.query() as select:
    node = graph.Node()
    response = select(node.label)

print(response.results)
# Output:
#    label
# 0  Alice
# 1    Bob
```

## See Also

[`Type`](../../../Type/README.md)
