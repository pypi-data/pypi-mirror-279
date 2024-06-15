# `relationalai.std.graphs.Compute.weighted_cosine_similarity()`

```python
relationalai.std.graphs.Compute.weighted_cosine_similarity(node1: Producer, node2: Producer) -> Expression
```

Compute the weighted cosine similarity between two nodes in a graph.
Cosine similarity measures the similarity between two nodes based on their respective neighborhood vectors,
weighted according to the edges.
Values range from `-1.0` to `1.0`, inclusive, where `1.0` indicates that the nodes have identical neighborhoods.
Pairs of nodes with a similarity of `0.0`, indicating no meaningful relationship,
are automatically excluded from results for improved performance.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes |   |
| Unweighted | Yes | Edge weights default to `1.0`.  |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer/README.md) | A node in the graph. |
| `node2` | [`Producer`](../../../Producer/README.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
the weighted cosine similarity between the two nodes as a floating-point value.

## Example

Use `.weighted_cosine_similarity()` to compute the weighted cosine similarity between two nodes in a graph.
You access the `.weighted_cosine_similarity()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with Person and Friendship types.
model = rai.Model("socialNetwork")
Person = model.Type("Person")
Friendship = model.Type("Friendship")

# Add some people to the model and connect them with friendships.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    Friendship.add(person1=alice, person2=bob, strength=100)
    Friendship.add(person1=bob, person2=carol, strength=10)

# Create a weighted, undirected graph with Person nodes and edges between friends.
# This graph has two edges: one between Alice and Bob, and one between Bob and Carol.
# The edges are weighted by the strength of each friendship.
graph = Graph(model, undirected=True, weighted=True)
graph.Node.extend(Person)
with model.rule():
    friendship = Friendship()
    graph.Edge.add(friendship.person1, friendship.person2, weight=friendship.strength)

# Compute the weighted cosine similarity between each pair of people in the graph.
with model.query() as select:
    person1, person2 = Person(), Person()
    similarity = graph.compute.weighted_cosine_similarity(person1, person2)
    response = select(person1.name, person2.name, alias(similarity, "weighted_cosine_similarity"))

print(response.results)
# Output:
#     name  name2  weighted_cosine_similarity
# 0  Alice  Alice                         1.0
# 1  Alice  Carol                         1.0
# 2    Bob    Bob                         1.0
# 3  Carol  Alice                         1.0
# 4  Carol  Carol                         1.0
```

There is no row for Alice and Bob in the preceding query's results.
That's because Alice and Bob have a weighted cosine similarity of `0.0`.
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
    obj1 < obj2  # Ensure pairs are unique. Compares internal object IDs.
    # Compute the weighted cosine similarity between each pair of objects.
    # Objects that are not nodes in the graph are filtered.
    similarity = graph.compute.weighted_cosine_similarity(obj1, obj2)
    response = select(obj1.name, obj2.name, alias(similarity, "weighted_cosine_similarity"))

# Only rows for people are returned, since companies are not nodes in the graph.
print(response.results)
# Output:
#     name  name2  weighted_cosine_similarity
# 0  Carol  Alice                         1.0
```

## See Also

[`.cosine_similarity()`](./cosine_similarity.md),
[`.jaccard_similarity()`](./jaccard_similarity.md),
and [`.weighted_jaccard_similarity()`](./weighted_jaccard_similarity.md).
