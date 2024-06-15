# `relationalai.std.graphs.Compute.adamic_adar()`

```python
relationalai.std.graphs.Compute.adamic_adar(node1: Producer, node2: Producer) -> Expression
```

Compute the Adamic-Adar index between two nodes in a graph.
The Adamic-Adar index quantifies node similarity based on shared neighbors.
Values are non-negative.
In link prediction analysis, a high Adamic-Adar values may indicate that
two nodes are likely to form a connection if they do not already have one.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :--- |
| Undirected | Yes |   |
| Directed | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `node2` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the Adamic-Adar index between the two nodes as a floating-point value, calculated by the following formula:

```
Adamic-Adar index = sum(1 / log(degree of shared neighbor))
```

The sum is over all shared neighbors of the two nodes.

## Example

Use `.adamic_adar()` to compute the Adamic-Adar index between two nodes in a graph.
You access the `.adamic_adar()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued `friend` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    alice.friends.extend([bob, carol])

# Create an undirected graph with Person nodes and edges between friends.
# This graph has two edges: one between Alice and Bob, and one between Bob and Carol.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Compute the Adamic-Adar index between each pair of people in the graph.
with model.query() as select:
    person1, person2 = Person(), Person()
    similarity = graph.compute.adamic_adar(person1, person2)
    response = select(person1.name, person2.name, alias(similarity, "adamic_adar"))

print(response.results)
# Output:
#     name  name2  adamic_adar
# 0  Alice  Alice          inf
# 1    Bob    Bob     1.442695
# 2    Bob  Carol     1.442695
# 3  Carol    Bob     1.442695
# 4  Carol  Carol     1.442695
```

There is no row for Alice and Bob in the preceding query's results.
That's because Alice and Bob have a an Adamic-Adar index of `0.0`.
Pairs of nodes with zero index, indicating no meaningful similarity, are often excluded from analyses.
Consequently, we filter out these pairs to improve performance.

If `node1` or `node2` is not a node in the graph, no exception is raised.
Instead, that object is filtered from the [rule](../../../Model/rule.md) or [query](../../../Model/query.md):

```python
# Add a Company type to the model.
Company = model.Type("Company")

# Add some companies to the model.
with model.rule():
    apple = Company.add(name="Apple")
    google = Company.add(name="Google")

# Create the union of the Person and Company types.
PersonOrCompany = Person | Company

with model.query() as select:
    # Get all person and company objects.
    obj1, obj2 = PersonOrCompany(), PersonOrCompany()
    obj1 < obj2  # Ensure pairs are unique. Compares internal object IDs.
    # Compute the Adamic-Adar index between each pair of objects.
    # Objects that are not nodes in the graph are filtered.
    similarity = graph.compute.adamic_adar(obj1, obj2)
    response = select(obj1.name, obj2.name, alias(similarity, "adamic_adar"))

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#     name name2  adamic_adar
# 0  Carol   Bob     1.442695
```

## See Also

[`.common_neighbor()`](./common_neighbor.md) and [`.preferential_attachment()`](./preferential_attachment.md).
