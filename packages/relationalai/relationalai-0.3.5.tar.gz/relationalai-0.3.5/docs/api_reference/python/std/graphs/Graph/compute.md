# `relationalai.std.graphs.Graph.compute`

Returns a `Compute` object for computing graph analytical methods on the graph.
See the [`Compute`](../Compute/README.md) class docs for a full list of available methods.

## Example

```python
import relationalai as rai
from relationalai.std import alias
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

# Compute the PageRank of each person in the graph.
with model.query() as select:
    person = Person()
    pagerank = graph.compute.pagerank(person)
    response = select(person.name, alias(pagerank, "pagerank"))

print(response.results)
# Output:
#     name         v
# 0  Alice  0.350877
# 1    Bob  0.649123
```

## See Also

[`Compute`](../Compute/README.md) and [`Graph`](./README.md).
