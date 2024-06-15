# `relationalai.std.graphs.Compute.is_triangle()`

```python
relationalai.std.graphs.Compute.is_triangle(node1: Producer, node2: Producer, node3: Producer) -> Expression
```

Check that three nodes form a triangle in the graph.
`node1`, `node2`, and `node3` form a triangle if there is an edge from `node1` to `node2`,
from `node2` to `node3`, and from `node3` to `node1`.
Must be called in a [rule](../../../Model/rule.md) or [query](../../../Model/query.md) context.

## Supported Graph Types

| Graph Type | Supported | Notes |
| :--- | :--- | :------ |
| Directed | Yes |   |
| Undirected | Yes |   |
| Weighted | Yes | Weights are ignored. |
| Unweighted | Yes |   |

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `node1` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `node2` | [`Producer`](../../../Producer.md) | A node in the graph. |
| `node3` | [`Producer`](../../../Producer.md) | A node in the graph. |

## Returns

Returns an [Expression](../../../Expression.md) object that produces
`True` if the `node1`, `node2`, and `node3` form a triangle, and `False` otherwise.

## Example

Use `.is_triangle()` to check if three nodes form a triangle in a graph.
You access the `.is_triangle()` method from a [`Graph`](../Graph.md) object's
[`.compute`](../Graph/compute.md) attribute:

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued `follows` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    charlie = Person.add(name="Charlie")
    diana = Person.add(name="Diana")
    alice.follows.add(bob)
    bob.follows.add(charlie)
    charlie.follows.extend([alice, diana])
    
# Create a directed graph with Person nodes and edges between followers.
# Note that graphs are directed by Default.
# This graph has edges from Alice to Bob, Bob to Charlie, Charlie to Alice, and Charlie to Diana.
graph = Graph(model)
graph.Node.extend(Person)
graph.Edge.extend(Person.follows)

# Do Alice, Bob, and Charlie form a triangle?
with model.query() as select:
    is_triangle = graph.compute.is_triangle(
        Person(name="Alice"),
        Person(name="Bob"),
        Person(name="Charlie")
    )
    response = select(is_triangle)
    
print(response.results)
# Output:
#       v
# 0  True

# Do Alice, Bob, and Diana form a triangle?
with model.query() as select:
    is_triangle = graph.compute.is_triangle(
        Person(name="Alice"),
        Person(name="Bob"),
        Person(name="Diana")
    )
    response = select(is_triangle)

print(response.results)
# Output:
#        v
# 0  False
```

You can also use `.is_triangle()` in a rule to filter out nodes that do not form a triangle:

```python
# Find all nodes that form a triangle
with model.query() as select:
    # Get triples of Person objects.
    person1, person2, person3 = Person(), Person(), Person()
    # Filter triples based on whether they form a triangle.
    graph.compute.is_triangle(person1, person2, person3)
    # Select the names of people that form triangles.
    response = select(person1.name, person2.name, person3.name)

print(response.results)
# Output:
#       name    name2    name3
# 0    Alice      Bob  Charlie
# 1      Bob  Charlie    Alice
# 2  Charlie    Alice      Bob
```

The output has three rows, but each row is a permutation of the same three nodes.
To get unique triples of nodes that form triangles, use [`.triangle()`](./triangles.md).

## See Also

[`num_triangles()`](./num_triangles.md) and [`triangles`](./triangles.md).
