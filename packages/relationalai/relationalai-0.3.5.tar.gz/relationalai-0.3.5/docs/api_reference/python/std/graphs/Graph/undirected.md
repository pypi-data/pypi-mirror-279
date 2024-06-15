# `relationalai.std.graphs.Graph.undirected`

An attribute assigned to `True` if the graph is undirected and `False` if it is directed.

## Example

```python
import relationalai as rai
from relationalai.std.graphs import Graph

model = rai.Model("myModel")
graph = Graph(model)

# By default, graphs are directed.
print(graph.undirected)
# Output:
# False
```

To create an undirected graph, set the `Graph()` constructor's  `undirected` parameter to `True`:

```python
graph = Graph(model, undirected=True)

print(graph.undirected)
# Output:
# True
```

`.undirected` is a read-only attribute and cannot be changed after a graph is created.
Attempting to do so raises an `AttributeError`:

```python
graph.undirected = False
# Output:
# AttributeError: property 'undirected' of 'Graph' object has no setter
```
