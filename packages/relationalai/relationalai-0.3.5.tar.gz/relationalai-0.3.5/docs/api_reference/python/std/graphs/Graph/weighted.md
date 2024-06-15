# `relationalai.std.graphs.Graph.undirected`

An attribute assigned to `True` if the graph is weighted and `False` otherwise.

## Example

```python
import relationalai as rai
from relationalai.std.graphs import Graph

model = rai.Model("myModel")
graph = Graph(model)

# By default, graphs are unweighted.
print(graph.weighted)
# Output:
# False
```

To create a weighted graph, set the `Graph()` constructor's  `weighted` parameter to `True`:

```python
graph = Graph(model, weighted=True)

print(graph.weighted)
# Output:
# True
```

`.weighted` is a read-only attribute and cannot be changed after a graph is created.
Attempting to do so raises an `AttributeError`:

```python
graph.weighted = False
# Output:
# AttributeError: property 'weighted' of 'Graph' object has no setter
```
