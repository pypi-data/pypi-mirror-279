# `relationalai.std.graphs.Graph.model`

The [model](../../../Model/README.md) instance from which a [`Graph`](../Graph/README.md) was created.

## Example

```python
import relationalai as rai
from relationalai.std.graphs import Graph

model = rai.Model("myModel")
graph = Graph(model)

print(graph.model == model)
# Output:
# True
```

## See Also

[`Model`](../../../Model/README.md)

