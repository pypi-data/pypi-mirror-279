# `relationalai.std.graphs.Compute.louvain()`

```python
relationalai.std.graphs.Compute.louvain(
    node: Producer,
    max_levels: int = 4,
    max_sweeps: int = 8,
    level_tolerance: float = 0.01,
    sweep_tolerance: float = 0.0001,
    randomization_seed: int | None = None
) -> Expression
```

Assign a community label to `node` using the Louvain method.
Louvain is a hierarchical algorithm that iteratively merges nodes into communities so that the modularity
--- that is, the density of edges within communities relative to edges between communities --- is maximized.
The algorithm stops when the modularity measure converges or a maximum number of iterations is reached.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes | Operates on the undirected version of the graph. |
| Undirected | Yes |   |
| Weighted | Yes | Only positive weights are supported. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `max_levels` | `int` | The maximum number of levels at which to optimize. Default is `4`. Must be positive. |
| `max_sweeps` | `int` | The maximum number of iterations to run at each level. Default is `8`. Must be non-negative. |
| `level_tolerance` | `float` | The minimum change in modularity required to continue to the next level. Default is `0.01`. Must be non-negative. |
| `sweep_tolerance` | `float` | The minimum change in modularity required to continue to the next sweep. Default is `0.0001`. Must be non-negative. |
| `randomization_seed` | `int` or `None` | The seed for the algorithm's random number generator. Default is `None`. Must be non-negative. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the integer community label assigned to `node` by the Louvain algorithm.

## Example

Use `.louvain()` to assign community labels to nodes in a graph using the Louvain algorithm.
You access the `.louvain()` method from a [`Graph`](../Graph.md) object's
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

# Find the community label for a single person using Louvain.
with model.query() as select:
    community = graph.compute.louvain(Person(name="Alice"))
    response = select(alias(community, "community_label"))

print(response.results)
# Output:
#    community_label
# 0                2

# Find the community label for each person using Louvain.
with model.query() as select:
    person = Person()
    community = graph.compute.louvain(person)
    response = select(person.name, alias(community, "community_label"))

print(response.results)
# Output:
#      name  community_label
# 0   Alice                2
# 1     Bob                2
# 2   Carol                1
# 3  Daniel                1
```

In this example, `.louvain()` finds two communities in the graph:
Alice and Bob are in one community, and Carol and Daniel are in another.
Note that isolated nodes, like Evelyn, are not assigned a community ID and
are filtered out of the results.

## See Also

[`.infomap()`](./infomap.md),
[`.label_propagation()`](./label_propagation.md),
and [`.triangle_community`](./triangle_community.md).
