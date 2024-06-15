# `relationalai.std.graphs.Compute.preferential_attachment()`

```python
relationalai.std.graphs.Compute.preferential_attachment(node1: Producer, node2: Producer) -> Expression
```

Compute the preferential attachment score between two nodes in a graph.
The preferential attachment score quantifies node similarity based on the product of their number of neighbors.
In link prediction analysis, a high preferential attachment score may indicate that
two nodes are likely to form a connection under the assumption that connections
are more likely between nodes with higher [degrees](./degree.md).
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
the preferential attachment score between the two nodes as an integer value, calculated by the following formula:

```
preferential attachment = number of neighbors of node1 * number of neighbors of node2
```

## Example

Use `.preferential_attachment()` to compute the preferential attachment score between two nodes in a graph.
You access the `.preferential_attachment()` method from a [`Graph`](../Graph.md) object's
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
    alice.friends.add(bob)

# Create an undirected graph with Person nodes and edges between friends.
# This graph has one edge between Alice and Bob. Carol is not connected to anyone.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Compute the preferential attachment score between Alice and Bob.
with model.query() as select:
    person1, person2 = Person(), Person()
    similarity = graph.compute.preferential_attachment(person1, person2)
    response = select(person1.name, person2.name, alias(similarity, "preferential_attachment"))

print(response.results)
# Output:
#     name  name2  preferential_attachment
# 0  Alice  Alice                        1
# 1  Alice    Bob                        1
# 2    Bob  Alice                        1
# 3    Bob    Bob                        1
```

There is no row for Alice and Carol in the preceding query's results.
That's because Alice and Carol have preferential attachment score of `0`, since Carol has no neighbors.
Pairs of nodes with zero preferential attachment are often excluded from analyses.
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
    # Compute the preferential attachment score between each pair of objects.
    # Objects that are not nodes in the graph are filtered.
    similarity = graph.compute.preferential_attachment(obj1, obj2)
    response = select(obj1.name, obj2.name, alias(similarity, "preferential_attachment"))

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#     name name2  preferential_attachment
# 0  Alice   Bob                        1
```

## See Also

[`.adamic_adar()`](./adamic_adar.md) and [`.common_neighbor()`](./common_neighbor.md).
