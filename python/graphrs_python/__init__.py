# pylint: disable=c-extension-no-member

"""
A Python module that wraps the high-performance `graphrs` Rust library.
"""

from dataclasses import dataclass
from typing import Generator, Optional
from . import _lib as rust


@dataclass
class Graph:
    """Wraps a `graphrs` `Graph`."""

    int_graph: rust.Graph
    int_to_name: dict


def create_graph_from_nodes_and_edges(nodes: list, edges: list, directed: bool) -> Graph:
    """
    Creates a `graphrs` `Graph` from lists of nodes and edges.
    """

    if len(nodes) == 0 and len(edges) == 0:
        raise ValueError("Both nodes and edges cannot be empty.")

    first_node_value = nodes[0] if len(nodes) > 0 else edges[0][0]
    if not isinstance(first_node_value, (int, str)):
        raise ValueError("Nodes must be int or str.")

    if isinstance(first_node_value, str):
        name_to_int, int_to_name = _get_node_name_keys(nodes, edges)
        int_nodes, int_edges = _convert_graph_to_int(nodes, edges, name_to_int)
    else:
        int_to_name = None
        int_nodes, int_edges = nodes, _get_edges_with_weight(edges)

    int_graph = rust.create_graph(int_nodes, int_edges, directed, False)
    return Graph(int_graph, int_to_name)


def create_graph_from_edges(edges: list, directed: bool) -> Graph:
    """
    Creates a `graphrs` `Graph` from a list edges.
    """

    if len(edges) == 0:
        raise ValueError("`edges` cannot be empty.")

    first_node_value = edges[0][0]
    if not isinstance(first_node_value, (int, str)):
        raise ValueError("Nodes must be int or str.")

    if isinstance(first_node_value, str):
        name_to_int, int_to_name = _get_node_name_keys([], edges)
        int_nodes, int_edges = _convert_graph_to_int([], edges, name_to_int)
    else:
        int_to_name = None
        int_nodes, int_edges = [], _get_edges_with_weight(edges)

    int_graph = rust.create_graph(int_nodes, int_edges, directed, True)
    return Graph(int_graph, int_to_name)


def create_graph_from_networkx(graph, weight: Optional[str] = None) -> Graph:
    """
    Creates a `graphrs` `Graph` from a NetworkX `Graph`.
    """
    import networkx as nx  # pylint: disable=import-error,import-outside-toplevel

    if not isinstance(graph, nx.Graph):
        raise ValueError("`graph` must be a networkx.Graph instance.")

    nodes = list(graph.nodes)
    edges = [(e[0], e[1], e[2][weight] if weight else float("nan")) for e in graph.edges(data=True)]

    if len(nodes) == 0 and len(edges) == 0:
        raise ValueError("Both nodes and edges cannot be empty.")

    first_node_value = nodes[0] if len(nodes) > 0 else edges[0][0]
    if not isinstance(first_node_value, (int, str)):
        raise ValueError("Nodes must be int or str.")

    if isinstance(first_node_value, str):
        name_to_int, int_to_name = _get_node_name_keys(nodes, edges)
        int_nodes, int_edges = _convert_graph_to_int(nodes, edges, name_to_int)
    else:
        int_to_name = None
        int_nodes, int_edges = nodes, _get_edges_with_weight(edges)

    int_graph = rust.create_graph(int_nodes, int_edges, graph.is_directed(), False)
    return Graph(int_graph, int_to_name)


def betweenness_centrality(graph: Graph, weighted: bool, normalized: bool = True) -> dict:
    """
    Computes the betweenness centrality of a graph.
    """
    centralities = rust.betweenness_centrality(graph.int_graph, weighted, normalized)
    if graph.int_to_name is None:
        return centralities
    else:
        return {graph.int_to_name[k]: v for k, v in centralities.items()}


def closeness_centrality(graph: Graph, weighted: bool, wf_improved: bool = True) -> dict:
    """
    Computes the closeness centrality of a graph.
    """
    centralities = rust.closeness_centrality(graph.int_graph, weighted, wf_improved)
    if graph.int_to_name is None:
        return centralities
    else:
        return {graph.int_to_name[k]: v for k, v in centralities.items()}


def clustering(graph: Graph, weighted: bool) -> dict:
    """
    Computes the clustering coefficient of the nodes in a graph.
    """
    clustering_scores = rust.clustering(graph.int_graph, weighted)
    if graph.int_to_name is None:
        return clustering_scores
    else:
        return {graph.int_to_name[k]: v for k, v in clustering_scores.items()}


def constraint(graph: Graph, weighted: bool) -> dict:
    """
    Computes the constraint of a graph.
    """
    constraints = rust.constraint(graph.int_graph, weighted)
    if graph.int_to_name is None:
        return constraints
    else:
        return {graph.int_to_name[k]: v for k, v in constraints.items()}


def eigenvector_centrality(
    graph: Graph, weighted: bool, max_iter: Optional[int] = None, tolerance: Optional[float] = None
) -> dict:
    """
    Computes the eigenvector centrality of a graph.
    """
    centralities = rust.eigenvector_centrality(graph.int_graph, weighted, max_iter, tolerance)
    if graph.int_to_name is None:
        return centralities
    else:
        return {graph.int_to_name[k]: v for k, v in centralities.items()}


def spectral_gap(graph: Graph, weighted: bool) -> float:
    """
    Computes the spectral gap of a graph.
    """
    return rust.spectral_gap(graph.int_graph, weighted)


### PRIVATE FUNCTIONS


def _convert_graph_to_int(nodes: list, edges: list, name_to_int: dict) -> tuple:
    int_nodes = [name_to_int[n] for n in nodes]
    int_edges = [
        (name_to_int[e[0]], name_to_int[e[1]], e[2] if len(e) == 3 else float("nan")) for e in edges
    ]
    return int_nodes, int_edges


def _get_edges_with_weight(edges: list) -> list:
    if not edges or len(edges[0]) == 3:
        return edges
    return [(e[0], e[1], float("nan")) for e in edges]


def _get_node_name_keys(nodes: list, edges: list) -> dict:
    name_to_int = {}
    int_to_name = {}
    for i, n in enumerate(set(_get_all_node_names(nodes, edges))):
        name_to_int[n] = i
        int_to_name[i] = n
    return name_to_int, int_to_name


def _get_all_node_names(nodes: list, edges: list) -> Generator:
    for n in nodes:
        yield n
    for e in edges:
        yield e[0]
        yield e[1]
