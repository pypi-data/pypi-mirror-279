# `relationalai.std.graphs.Compute.weakly_connected_component()`

```python
relationalai.std.graphs.Compute.weakly_connected_component(node: Producer) -> Expression
```

Find the weakly connected component containing `node` in a graph.
The weakly connected component of a node is the set of nodes that are
reachable from the node in an undirected version of the graph.
Isolated nodes are not assigned a component and are excluded from the results.
Components are identified by the object in the component with the smallest internal identifier.
In an undirected graph, the weakly connected component is the same as the connected component.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes | Operates on the undirected version of the graph. |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the representative object of the weakly connected component containing `node`.
Component representatives are the objects with the smallest internal identifiers in the component.

## Example

Use `.weakly_connected_component()` to find the weakly connected component containing a node in a graph.
You access the `.weakly_connected_component()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
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
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Compute the weakly connected component for each person in the graph.
with model.query() as select:
    person = Person()
    component = graph.compute.weakly_connected_component(person)
    response = select(person.name, alias(component.name, "component_representative"))

print(response.results)
# Output:
#     name component_representative
# 0  Alice                    Alice
# 1    Bob                    Alice
```

Component representatives are the objects with the smallest internal identifiers in the component.
In the above, Alice and Bob are in the same component, with Alice as the representative.
`.weakly_connected_component()` filters nodes that cannot reach or be reached by any other node in the graph,
which is why Carol, an isolated node, is not included in the results.

Use [`std.aggregates.count`](../../../std/aggregates/count.md) to count the number of weakly connected components in a graph.
Since isolated nodes are filtered, this counts the number of weakly connected components with more than one node:

```python
from relationalai.std.aggregates import count

with model.query() as select:
    component = graph.compute.weakly_connected_component(Person())
    response = select(alias(count(component), "num_components"))

print(response.results)
# Output:
#    num_components
# 0               1
```

In this example, there's only one component in the graph containing more than one node: the component with Alice and Bob.

## See Also

[`.is_connected()`](./is_connected.md),
[`.is_reachable()`](./is_reachable.md),
and [`.reachable_from()`](./reachable_from.md).
