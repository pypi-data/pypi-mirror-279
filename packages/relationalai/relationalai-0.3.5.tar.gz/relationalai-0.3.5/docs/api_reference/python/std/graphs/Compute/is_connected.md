# `relationalai.std.graphs.Compute.is_connected()`

```python
relationalai.std.graphs.Compute.is_connected() -> Expression
```

Check if the graph is connected.
A graph is connected if every node is reachable from every other node in the undirected version of the graph.
For directed graphs, connected is the same as weakly connected.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Returns

Returns an [Expression](../../../Expression.md) object that filters connected graphs.

## Example

Use `.is_connected()` to check if a graph is connected.
You access the `.is_connected()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork1000")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued `follows` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    alice.follows.add(bob)

# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by default.
# This graph has one edge from Alice to Bob. Carol is not connected to anyone.
graph = Graph(model, with_isolated_nodes=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Is the graph connected?
with model.query() as select:
    with model.match() as connected:
        with graph.compute.is_connected():
            connected.add(True)
        with model.case():
            connected.add(False)
    response = select(alias(connected, "is_connected"))

print(response.results)
# Output:
#    is_connected
# 0         False
```

In the example above, the graph is not connected because Carol is not connected to anyone.

## See Also

[`.weakly_connected_component()`](weakly_connected_component.md)
