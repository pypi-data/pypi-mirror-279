# `relationalai.std.graphs.Graph.fetch()`

```python
relationalai.std.graphs.Graph.fetch() -> dict
```

Returns a dictionary with two keys, `"nodes"` and `"edges"`, containing the graph's data.
`.fetch()` is a blocking operation that queries the model and returns the data locally.
It may be slow and consume a lot of memory for large graphs.
Use `.fetch()` to pass graph data to external libraries, such as alternative visualization tools.

## Returns

A `dict` object.

## Example

```python
from pprint import pprint

import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model with a 'Person' type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add people to the model connected by a multi-valued 'follows' property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    alice.follows.add(bob)

# Create a directed graph with 'Person' nodes and 'follows' edges.
graph = Graph(model)
graph.Node.extend(Person, label=Person.name)
graph.Edge.extend(Person.follows, label="follows")

# Fetch the graph.
# NOTE: Fetching the graph queries the model and returns the data locally.
# If the graph is large, fetching it may be slow and consume a lot of memory.
pprint(graph.fetch())
# Output:
# {'edges': defaultdict(<class 'dict'>,
#                       {('+0JKlsJxRGKBYFiMq/o/Sg', 'ru89MBnrLAPLQFVtoYdnfQ'): {'label': 'follows'}}),
#  'nodes': defaultdict(<class 'dict'>,
#                       {'+0JKlsJxRGKBYFiMq/o/Sg': {'label': 'Alice'},
#                        'ru89MBnrLAPLQFVtoYdnfQ': {'label': 'Bob'}})}
```

## See Also

[`.visualize()`](./visualize.md)
