# `relationalai.std.graphs.Compute.cosine_similarity()`

```python
relationalai.std.graphs.Compute.cosine_similarity(node1: Producer, node2: Producer) -> Expression
```

Compute the cosine similarity between two nodes in an undirected graph.
Cosine similarity measures the similarity between two nodes based on their respective neighborhood vectors.
Values range from `0.0` to `1.0`, inclusive, where `1.0` indicates that the nodes have identical neighborhoods.
Pairs of nodes with a similarity of `0.0`, indicating no meaningful relationship,
are excluded from results for improved performance.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

Directed graphs are not supported.
For a similar measure that works with directed graphs, see [`.weighted_cosine_similarity()`](./weighted_cosine_similarity.md).

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | No | Use [`.weighted_cosine_similarity`](./weighted_cosine_similarity.md) for directed graphs. |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. Use [`.weighted_cosine_similarity`](./weighted_cosine_similarity.md) to take weights into account. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer/README.md) | A node in the graph. |
| `node2` | [`Producer`](../../../Producer/README.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the cosine similarity between the two nodes as a floating-point value.

## Example

Use `.cosine_similarity()` to compute the cosine similarity between two nodes in a graph.
Directed graphs are not supported.

You access the `.cosine_similarity()` method from a [`Graph`](../Graph.md) object's
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
    bob.friends.add(carol)

# Create an undirected graph with Person nodes and edges between friends.
# Note that cosine similarity is only supported for undirected graphs.
# This graph has two edges: one between Alice and Bob, and one between Bob and Carol.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

with model.query() as select:
    # Get pairs of people.
    person1, person2 = Person(), Person()
    # Compute the cosine similarity between each pair of people.
    similarity = graph.compute.cosine_similarity(person1, person2)
    # Select each person's name and their similarity value.
    response = select(person1.name, person2.name, alias(similarity, "cosine_similarity"))

print(response.results)
# Output:
#     name  name2  cosine_similarity
# 0  Alice  Alice                1.0
# 1  Alice  Carol                1.0
# 2    Bob    Bob                1.0
# 3  Carol  Alice                1.0
# 4  Carol  Carol                1.0
```

There is no row for Alice and Bob in the preceding query's results.
That's because Alice and Bob have a cosine similarity of `0.0`.
Pairs of nodes with zero similarity, indicating no meaningful similarity, are often excluded from analyses.
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
    obj1 < ob2  # Ensure pairs are unique. Compares internal object IDs.
    # Compute the cosine similarity between each pair of objects.
    # Objects that are not nodes in the graph are filtered out of the results.
    similarity = graph.compute.cosine_similarity(obj1, obj2)
    response = select(obj1.name, obj2.name, alias(similarity, "cosine_similarity"))

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#     name  name2  cosine_similarity
# 0  Carol  Alice                1.0
```

## See Also

[`.weighted_cosine_similarity()`](./weighted_cosine_similarity.md),
[`.jaccard_similarity()`](./jaccard_similarity.md),
and [`.weighted_jaccard_similarity()`](./weighted_jaccard_similarity.md).
