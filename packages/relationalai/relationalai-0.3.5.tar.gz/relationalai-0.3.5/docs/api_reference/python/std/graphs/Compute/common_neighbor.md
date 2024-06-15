# `relationalai.std.graphs.Compute.common_neighbor()`

```python
relationalai.std.graphs.Compute.common_neighbor(node1: Producer, node2: Producer) -> Expression
```

Find the common neighbors between two nodes in a graph.
A node is a common neighbor if it is connected to both `node1` and `node2`.
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
[nodes](../Graph/Node.md) that are common neighbors of `node1` and `node2`.

## Example

Use `.common_neighbor()` to find the common neighbors between two nodes in a graph.
You access the `.common_neighbor()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
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
# This graph has two edges: one between Alice and Bob, and one between Alice and Carol.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

# Find the common neighbors of Bob and Carol.
with model.query() as select:
    neighbor = graph.compute.common_neighbor(Person(name="Bob"), Person(name="Carol"))
    response = select(neighbor.name)

print(response.results)
# Output:
#     name
# 0  Alice
```

If `node1` or `node2` is not a node in the graph, no exception is raised.
Instead, that pair of objects is filtered from the [rule](../../../Model/rule.md) or [query](../../../Model/query.md):

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
    # Get all pairs of person and company objects.
    obj1, obj2 = PersonOrCompany(), PersonOrCompany()
    obj1 < obj2  # Ensure pairs are unique.
    neighbor = graph.compute.common_neighbor(obj1, obj2)
    response = select(obj1.name, obj2.name, neighbor.name)

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#     name name2  name3
# 0  Carol   Bob  Alice
```

Note that pairs of nodes with no common neighbors are filtered by `.common_neighbor()`.
For example, there is no row for Alice and Bob in the above output because they have no common neighbors.
Alice is neighbors with Bob and Carol, but Bob's only neighbor is Alice.

## See Also

[`.adamic_adar()`](./adamic_adar.md) and [`.preferential_attachment()`](./preferential_attachment.md).
