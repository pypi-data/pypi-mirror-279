# `relationalai.std.graphs.Compute`

```python
class relationalai.std.graphs.Compute()
```

The `Compute` class serves as a namespace for various graph algorithms.
This class is automatically instantiated when you create a [`Graph`](../Graph/README.md) object
and is accessible via the graph's [`.compute` attribute](../Graph/compute.md).
It provides methods for computing basic graph statistics, centrality and similarity measures, community detection, and more.

## Methods

### Basic Statistics

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.num_edges()`](./num_edges.md) | Get the number of edges in the graph. | [`Expression`](../../../Expression.md) |
| [`.num_nodes()`](./num_nodes.md) | Get the number of nodes in the graph. | [`Expression`](../../../Expression.md) |

### Degree

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.avg_degree()`](./avg_degree.md) | Compute the average degree of the graph. | [`Expression`](../../../Expression.md) |
| [`.avg_indegree()`](./avg_indegree.md) | Compute the average indegree of a directed graph. Alias for `.avg_degree()` in undirected graphs. | [`Expression`](../../../Expression.md) |
| [`.avg_outdegree()`](./avg_outdegree.md) | Compute the average outdegree of a directed graph. Alias for `.avg_degree()` in undirected graphs. | [`Expression`](../../../Expression.md) |
| [`.degree(node)`](./degree.md) | Compute the degree of a node. | [`Expression`](../../../Expression.md) |
| [`.indegree(node)`](./indegree.md) | Compute the indegree of a node. | [`Expression`](../../../Expression.md) |
| [`.max_degree()`](./max_degree.md) | Compute the maximum degree of a graph. | [`Expression`](../../../Expression.md) |
| [`.max_indegree()`](./max_indegree.md) | Compute the maximum indegree a directed graph. Alias for `.max_degree()` in undirected graphs. | [`Expression`](../../../Expression.md) |
| [`.max_outdegree()`](./max_outdegree.md) | Compute the maximum outdegree of a directed graph graph. Alias for `.max_degree()` in undirected graphs. | [`Expression`](../../../Expression.md) |
| [`.min_degree()`](./min_degree.md) | Compute the minimum degree of a graph. | [`Expression`](../../../Expression.md) |
| [`.min_indegree()`](./min_indegree.md) | Compute the minimum indegree of a directed graph. Alias for `.min_degree()` in undirected graphs. | [`Expression`](../../../Expression.md) |
| [`.min_outdegree()`](./min_outdegree.md) | Compute the minimum outdegree of a directed graph. Alias for `.min_degree()` in undirected graphs. | [`Expression`](../../../Expression.md) |
| [`.outdegree(node)`](./outdegree.md) | Compute the outdegree of a node. | [`Expression`](../../../Expression.md) |

### Centrality Measures

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.betweenness_centrality(node)`](./betweenness_centrality.md) | Compute the betweenness centrality of a node. | [`Expression`](../../../Expression.md) |
| [`.degree_centrality(node)`](./degree_centrality.md) | Compute the degree centrality of a node. | [`Expression`](../../../Expression.md) |
| [`.eigenvector_centrality(node)`](./eigenvector_centrality.md) | Compute the eigenvector centrality of the graph. | [`Expression`](../../../Expression.md) |
| [`.pagerank(node)`](./pagerank.md) | Compute the PageRank of a node. | [`Expression`](../../../Expression.md) |
| [`.weighted_degree_centrality(node)`](./weighted_degree_centrality.md) | Compute the weighted degree centrality of a node. Alias for `degree_centrality` in unweighted graphs. | [`Expression`](../../../Expression.md) |

### Similarity Measures

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.cosine_similarity(node1, node2)`](./cosine_similarity.md) | Compute the cosine similarity between two nodes. | [`Expression`](../../../Expression.md) |
| [`.jaccard_similarity(node1, node2)`](./jaccard_similarity.md) | Compute the Jaccard similarity between two nodes. | [`Expression`](../../../Expression.md) |
| [`.weighted_cosine_similarity(node1, node2)`](./weighted_cosine_similarity.md) | Compute the weighted cosine similarity between two nodes. Alias for `cosine_similarity` in unweighted graphs. Only undirected graphs are supported. | [`Expression`](../../../Expression.md) |
| [`.weighted_jaccard_similarity(node1, node2)`](./weighted_jaccard_similarity.md) | Compute the weighted Jaccard similarity between two nodes. Alias for `jaccard_similarity()` in unweighted graphs. | [`Expression`](../../../Expression.md) |

### Link Prediction

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.adamic_adar(node1, node2)`](./adamic_adar.md) | Compute the Adamic-Adar index between two nodes. | [`Expression`](../../../Expression.md) |
| [`.common_neighbor(node1, node2)`](./common_neighbor.md) | Find the common neighbors between two nodes. | [`Expression`](../../../Expression.md) |
| [`.preferential_attachment(node1, node2)`](./preferential_attachment.md) | Compute the preferential attachment score between two nodes. | [`Expression`](../../../Expression.md) |

### Community Detection

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.infomap()`](./infomap.md) | Assign a community label to each node using the Infomap algorithm. | [`Expression`](../../../Expression.md) |
| [`.is_triangle(node1, node2, node3)`](./is_triangle.md) | Check if three nodes form a triangle. | [`Expression`](../../../Expression.md) |
| [`.label_propagation(node)`](./label_propagation.md) | Assign a community label to `node` using the label propagation algorithm. | [`Expression`](../../../Expression.md) |
| [`.louvain(node)`](./louvain.md) | Assign a community label to `node` using the Louvain algorithm. | [`Expression`](../../../Expression.md) |
| [`.num_triangles()`](./num_triangles.md) | Compute the number of triangles in the graph. | [`Expression`](../../../Expression.md) |
| [`.triangles()`](./triangles.md) | Find all unique triangles in the graph. | `tuple` of three [`Expression`](../../../Expression.md) objects. |
| [`.triangle_community(node)`](./triangle_community.md) | Assign a community label to `node` using the percolation method. | [`Expression`](../../../Expression.md) |

### Clustering

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.avg_clustering_coefficient()`](./avg_clustering_coefficient.md) | Compute the average clustering coefficient of the graph. | [`Expression`](../../../Expression.md) |
| [`.local_clustering_coefficient(node)`](./local_clustering_coefficient.md) | Compute the local clustering coefficient of a node. | [`Expression`](../../../Expression.md) |

### Connectivity

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.is_connected()`](./is_connected.md) | Check if the graph is connected. | [`Expression`](../../../Expression.md) |
| [`.is_reachable(node1, node2)`](./is_reachable.md) | Check if `node2` is reachable from `node1`. | [`Expression`](../../../Expression.md) |
| [`.reachable_from(node)`](./reachable_from.md) | Find all nodes reachable from `node`. | [`Expression`](../../../Expression.md) |
| [`.weakly_connected_component(node)`](./weakly_connected_component.md) | Find the weakly connected component containing `node`. | [`Expression`](../../../Expression.md) |

### Distance

| Name | Description | Returns |
| :--------- | :------------------ | :--- |
| [`.diameter_range()`](./diameter_range.md) | Compute lower and upper bounds for the diameter of a graph. | `tuple` of two [`Expression`](../../../Expression.md) objects. |
| [`.distance(node1, node2)`](./distance.md) | Compute the shortest path length between two nodes. Ignores weights in weighted graphs. | [`Expression`](../../../Expression.md) |
| [`.weighted_distance(node1, node2)`](./weighted_distance.md) | Compute the shortest path length between two nodes in a weighted graph. Alias for `distance` in unweighted graphs. | [`Expression`](../../../Expression.md) |

## Example

Graph algorithms are executed by calling the appropriate method from a [`Graph`](../Graph/README.md) object's
[`.compute`](../Graph/compute.md) attribute.
The following example demonstrates how to compute the [PageRank](./pagerank.md) of each person in a social network graph:

```python
import relationalai as rai
from relationalai.std import alias
from relationalai.std.graphs import Graph

# Create a model named "socialNetwork" with a Person type.
model = rai.Model("socialNetwork")
Person = model.Type("Person")

# Add some people to the model and connect them with a multi-valued 'friends' property.
with model.rule():
    alice = Person.add(name="Alice")
    bob = Person.add(name="Bob")
    carol = Person.add(name="Carol")
    daniel = Person.add(name="Daniel")
    alice.friends.extend([bob, carol])
    carol.friends.add(daniel)

# Create an undirected graph with Person nodes and edges from people to their friends.
# This graph has three edges: one from Alice to Bob, Alice to Carol, and Carol to Daniel.
graph = Graph(model, undirected=True)
graph.Node.extend(Person)
graph.Edge.extend(Person.friends)

with model.query() as select:
    # Get all person objects.
    person = Person()
    # Compute the PageRank of each person.
    pagerank = graph.compute.pagerank(person)
    # Select the each person's name and their PageRank value.
    response = select(person.name, alias(pagerank, "pagerank"))

print(response.results)
# Output:
#      name  pagerank
# 0   Alice  0.324562
# 1     Bob  0.175438
# 2   Carol  0.324562
# 3  Daniel  0.175438
```

See the documentation for each method in the [Methods](#methods) section for more examples.

## See Also

[`Graph`](../Graph/README.md) and [`Graph.compute`](../Graph/compute.md).
