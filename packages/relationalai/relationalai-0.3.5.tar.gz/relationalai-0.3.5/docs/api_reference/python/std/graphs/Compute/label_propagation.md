# `relationalai.std.graphs.Compute.label_propagation()`

```python
relationalai.std.graphs.Compute.label_propagation(
    node: Producer,
    max_sweeps: int = 20,
    randomization_seed: int | None = None
) -> Expression
```

Assign a community label to `node` using the label propagation algorithm.
Label propagation is an algorithm that begins by assigning each node a unique community label
and iteratively updates the label of each node to the most common label among its neighbors
until convergence or a maximum number of iterations is reached.
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
| `max_sweeps` | `int` | The maximum number of iterations to run the label propagation algorithm. Default is `20`. |
| `randomization_seed` | `int` or `None` | The seed for the algorithm's random number generator. Default is `None`. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the integer community label assigned by label propagation to `node`.

## Example

Use `.label_propagation()` to assign a community label to a node in a graph.
You access the `.label_propagation()` method from a [`Graph`](../Graph.md) object's
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

# Find the community label for a single person using label propagation.
with model.query() as select:
    community = graph.compute.label_propagation(person)
    response = select(alias(community, "community_label"))

print(response.results)
# Output:
#    community_label
# 0                2

# Find the community label for each person in the graph.
with model.query() as select:
    person = Person()
    community = graph.compute.label_propagation(person)
    response = select(person.name, alias(community, "community_label"))

print(response.results)
# Output:
#      name  community_label
# 0   Alice                2
# 1     Bob                2
# 2   Carol                1
# 3  Daniel                1
```

In this example, `.label_propagation()` finds two communities in the graph:
Alice and Bob are in one community, and Carol and Daniel are in another.
Note that isolated nodes, like Evelyn, are not assigned a community ID and
are filtered out of the results.

## See Also

[`.infomap()`](./infomap.md),
[`.louvain()](./louvain.md),
and [`.triangle_community`](./triangle_community.md).
