# `relationalai.std.graphs.EdgeInstance.from_`

Returns a [`Producer`](../../../Producer/README.md) object that produces
the node at the start of an edge.

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

# Get the names of all people following Bob.
with model.query() as select:
    edge = graph.Edge(to=Person(name="Bob"))
    follower = edge.from_
    response = select(follower.name)

print(response.results)
# Output:
#     name
# 0  Alice
```

## See Also

[`.to`](./to.md)
