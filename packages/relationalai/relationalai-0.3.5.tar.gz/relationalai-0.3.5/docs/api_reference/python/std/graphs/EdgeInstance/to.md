# `relationalai.std.graphs.EdgeInstance.to`

Returns a [`Producer`](../../../Producer/README.md) object that produces
the terminal node of an edge.

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

# Get the names of all people Alice follows.
with model.query() as select:
    edge = graph.Edge(from_=Person(name="Alice"))
    follows = edge.to
    response = select(follows.name)

print(response.results)
# Output:
#   name
# 0  Bob
```

## See Also

[`.from_`](./from_.md)
