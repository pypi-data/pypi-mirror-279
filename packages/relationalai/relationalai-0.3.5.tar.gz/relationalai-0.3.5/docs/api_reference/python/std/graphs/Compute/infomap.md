# `relationalai.std.graphs.Compute.infomap()`

```python
relationalai.std.graphs.Compute.infomap(
    node: Producer
    max_levels: int = 4,
    max_sweeps: int = 8,
    level_tolerance: float = 0.01,
    sweep_tolerance: float = 0.0001,
    teleportation_rate: float = 0.15,
    visit_rate_tolerance: float = 1e-15,
    randomization_seed: int | None = None,
) -> Expression
```

Assign a community label to `node` using the Infomap algorithm.
Infomap identifies communities using tools from information theory to find
the most compact way to encode the network structure using the map equation.
Nodes assigned to the same community are more likely to interact or communicate with one another
as information flows through the network.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Only positive weights are supported. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `max_levels` | `int` | The maximum number of levels at which to optimize. Default is `4`. Must be positive. |
| `max_sweeps` | `int` | The maximum number of iterations to run at each level. Default is `8`. Must be non-negative. |
| `level_tolerance` | `float` | The minimum change in the map equation required to continue to the next level. Default is `0.01`. Must be non-negative. |
| `sweep_tolerance` | `float` | The minimum change in the map equation required to continue to the next sweep. Default is `0.0001`. Must be non-negative. |
| `teleportation_rate` | `float` | The probability of teleporting to a random node. Default is `0.15`. Must be in the range `(0, 1]`. |
| `visit_rate_tolerance` | `float` | The minimum change in the visit rate required to continue to the next sweep. Default is `1e-15`. Must be non-negative. |
| `randomization_seed` | `int` or `None` | The seed for the algorithm's random number generator. Default is `None`. Must be non-negative. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the integer community label assigned by Infomap to `node` as an integer value.

## Example

Use `.infomap()` to assign community labels to nodes in a graph using the Infomap algorithm.
You access the `.infomap()` method from a [`Graph`](../Graph.md) object's
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
    daniel = Person.add(name="Daniel")
    evelyn = Person.add(name="Evelyn")
    alice.follows.add(bob)
    carol.follows.add(daniel)

# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by default.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Find the community label for a single person using the Infomap algorithm.
with model.query() as select:
    community = graph.compute.infomap(Person(name="Alice"))
    response = select(alias(community, "community_label"))

print(response.results)
# Output:
#    community_label
# 0                2

# Find the community label for each person in the graph.
with model.query() as select:
    person = Person()
    community = graph.compute.infomap(person)
    response = select(person.name, alias(community, "community_label"))

print(response.results)
# Output:
#      name  community_label
# 0   Alice                2
# 1     Bob                2
# 2   Carol                1
# 3  Daniel                1
```

In this example, `.infomap()` finds two communities in the graph:
Alice and Bob are in one community, and Carol and Daniel are in another.
Note that isolated nodes, like Evelyn, are not assigned a community ID and are filtered from the query.

## See Also

[`.label_propagation()`](./label_propagation.md),
[`.louvain()`](./louvain.md),
and [`.triangle_community()`](./triangle_community.md).
