# graphrs_python

`graphrs_python` is a Python wrapper around the high-performance [graphrs](<https://crates.io/crates/graphrs>)
Rust crate. See the [performance documentation](<https://github.com/malcolmvr/graphrs/blob/main/performance.md>)
for a comparison of the performance of `graphrs` to other graph libraries.

## Example Usage

```python
import graphrs_python as grs

nodes = ["n1", "n2", "n3", "n4"]
edges = [("n1", "n2", 1.0), ("n2", "n3", 1.0), ("n3", "n4", 1.0), ("n4", "n2", 1.0)]
graph = grs.create_graph_from_nodes_and_edges(nodes, edges, directed=True)

print(grs.betweenness_centrality(graph, weighted=True, normalized=True))
print(grs.closeness_centrality(graph, weighted=True, wf_improved=True))
print(grs.eigenvector_centrality(graph, weighted=True))
```

Graphs can also be created from just edges:

```python
import graphrs_python as grs

edges = [("n1", "n2", 1.0), ("n2", "n3", 1.0), ("n3", "n4", 1.0), ("n4", "n2", 1.0)]
graph = grs.create_graph_from_edges(edges, directed=True)
```

And graphs can also be created from NetworkX `Graph` objects:

```python
import graphrs_python as grs
import networkx

graph = nx.DiGraph()
graph.add_edges_from(
    [
        ("n1", "n2", {"weight": 1.0}),
        ("n2", "n3", {"weight": 1.0}),
        ("n3", "n4", {"weight": 1.0}),
        ("n4", "n2", {"weight": 1.0}),
    ]
)
graph = grs.create_graph_from_networkx(graph, weight="weight")
```

## License

MIT
