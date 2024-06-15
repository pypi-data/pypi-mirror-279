# `relationalai.std.graphs.Graph`

```python
class relationalai.std.graphs.Graph(
    model: Model,
    undirected: bool = False,
    weighted: bool = False,
    default_weight: float = 1.0
)
```

Use the `Graph` class to Create graphs representing relationships between objects
in a model and perform graph analytics.
RelationalAI supports directed and undirected graphs, as well as edge-weighted graphs.

## Parameters

| Name | Type | Description |
| :--- | :--- | :------ |
| `model` | [`Model`](../../../Model/README.md) | The model on which the `Graph` is instantiated. |
| `undirected` | `bool` | Whether the graph is undirected. Default is `False`. |
| `weighted` | `bool` | Whether the graph is weighted. Default is `False`. |
| `default_weight` | `float` | The default weight for edges in the graph. Default is `1.0`. Ignored if `weighted` is set to `False`. |

## Attributes

| Name | Type | Description |
| :--- | :--- | :------ |
| [`.id`](./id.md) | `int` | The unique system ID of the graph. |
| [`.model`](./model.md) | [`Model`](../../../Model/README.md) | The model on which the graph is based. |
| [`.undirected`](./undirected.md) | `bool` | Whether the graph is undirected. Read-only. |
| [`.weighted`](./weighted.md) | `bool` | Whether the graph is weighted. Read-only. |
| [`.Node`](./Node.md) | [`Type`](../../../Type/README.md) | A [type](../../../Type/README.md) containing the graph's nodes. |
| [`.Edge`](./Edge.md) | [`Edge`](../Edge/README.md) | A type-like object containing the graph's edges. |
| [`.compute`](./compute.md) | [`Compute`](../Compute/README.md) | A namespace for graph analytics methods. |

## Methods

| Name | Description | Returns |
| :--- | :------ | :------ |
| [`.fetch()`](./fetch.md) | Get a dictionary representation of the graph. | `dict` |
| [`.visualize(style, **kwargs)`](./visualize.md) | Visualize the graph. | A gravis [Figure](TODO) object. |

## Example

Use the `Graph()` constructor to create a new `graph` object and add nodes and edges
using the [`graph.Node`](./Node.md) and [`graph.Edge`](./Edge.md) objects.

This example creates a directed graph from a basic social network model and visualizes it with node and edge labels:

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model with a `Person` type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add people to the model connected by a multi-valued `follows` property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    alice.follows.add(bob)

# Create a graph. By default, graphs are directed and unweighted.
graph = Graph(model)

# Add all 'Person' objects to the graph as nodes, labeling them by their
# 'name' property. Node and edge labels are optional and are shown in visualizations.
graph.Node.extend(Person, label=Person.name)

# Add edges using the 'Person.follows' property to connect nodes.
graph.Edge.extend(Person.follows, label="follows")

# Visualize the graph. In Jupyter notebooks, '.display()' is not needed.
graph.visualize().display()
```

![A graph with two nodes labeled Alice and Bob and an arrow pointing from Alice to Bob.](./img/directed.png)

Set the `undirected` parameter to `True` to create an undirected graph.
In visualizations, undirected edges are drawn as lines without arrows:

```python
graph = Graph(model, undirected=True)
graph.Node.extend(Person, label=Person.name)
graph.Edge.extend(Person.follows, label="follows")
graph.visualize().display()
```

![An undirected graph with two nodes labeled Alice and Bob and an line (with no arrow) connecting them.](./img/undirected.png)

To create a weighted graph, set the `weighted` parameter to `True`.
In a weighted graph, edges have a `weight` property that can be used in graph algorithms.
The `default_weight` parameter, which defaults to `1.0`,
sets the default weight for any edges without a `weight` property.
Both directed and undirected graphs can be weighted.

In the next example, we create a weighted, directed graph from a model of financial transactions between people:

```python
import relationalai as rai
from relationalai.std.graphs import Graph

# Create a model with 'Person' and 'Transaction' types.
model = rai.Model("transactions")
Person = model.Type("Person")
Transaction = model.Type("Transaction")

# Add some people and a transaction to the model.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    transaction = Transaction.add(sender=alice, recipient=bob, amount=100.0)

# Create a weighted, directed graph.
graph = Graph(model, weighted=True)

# Add all 'Person' objects to the graph as nodes, labeling them by their 'name' property.
graph.Node.extend(Person, label=Person.name)

# Add edges to the graph from the 'Transaction' type.
# The edge weights are set to the transaction's 'amount' property.
with model.rule():
    t = Transaction()
    graph.Edge.add(t.sender, t.recipient, weight=t.amount)

# Visualize the graph with edges labeled by their weight.
# Use a lambda function to access the weight of each edge,
# since no label property is set. Note that properties are
# accessed using subscript notation instead of dot notation.
graph.visualize(style={"edge": {"label": lambda e: e['weight']}}).display()
```

![A directed, weighted graph with two nodes labeled Alice and Bob and an arrow pointing from Alice to Bob with a label of 100.](./img/weighted.png)

Graphs are visualized using the [gravis]([TODO](https://robert-haas.github.io/gravis-docs/index.html)) package.
See [`.visualize()`](./visualize.md) for more examples of customizing graph visualizations.

Use the [`.compute`](./compute.md) property to access graph analytics methods,
such as computing the [PageRank](../Compute/pagerank.md) of nodes in the graph:

```python
with model.query() as select:
    person = Person()
    pagerank = graph.compute.pagerank(person)
    response = select(person.name, pagerank)

print(response.results)
# Output:
#     name         v
# 0  Alice  0.350877
# 1    Bob  0.649123
```

See the [`Compute`](../Compute/README.md) class for a list of available graph analytics methods.

## See Also

[`Compute`](../Compute/README.md),
[`Edge`](../Edge/README.md),
and [`EdgeInstance`](../EdgeInstance/README.md).
