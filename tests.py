# pylint: disable=missing-class-docstring,missing-module-docstring,missing-function-docstring

import unittest
import networkx as nx
import graphrs_python as grs


class GraphrsPythonTest(unittest.TestCase):

    def test_create_graph_from_nodes_and_edges(self):
        nodes = ["n1", "n2", "n3", "n4"]
        edges = [("n1", "n2", 1.0), ("n2", "n3", 1.0), ("n3", "n4", 1.0), ("n4", "n2", 1.0)]
        graph = grs.create_graph_from_nodes_and_edges(nodes, edges, directed=True)
        self.assertCountEqual(graph.int_to_name.keys(), [0, 1, 2, 3])
        self.assertCountEqual(graph.int_to_name.values(), ["n1", "n2", "n3", "n4"])

    def test_create_graph_from_edges(self):
        edges = [("n1", "n2", 1.0), ("n2", "n3", 1.0), ("n3", "n4", 1.0), ("n4", "n2", 1.0)]
        graph = grs.create_graph_from_edges(edges, directed=True)
        self.assertCountEqual(graph.int_to_name.keys(), [0, 1, 2, 3])
        self.assertCountEqual(graph.int_to_name.values(), ["n1", "n2", "n3", "n4"])

    def test_create_graph_from_networkx(self):
        graph = nx.DiGraph()
        graph.add_edges_from(
            [
                ("n1", "n2", {"weight": 1.0}),
                ("n2", "n3", {"weight": 1.0}),
                ("n3", "n4", {"weight": 1.0}),
                ("n4", "n2", {"weight": 1.0}),
            ]
        )
        graph = grs.create_graph_from_networkx(graph)
        self.assertCountEqual(graph.int_to_name.keys(), [0, 1, 2, 3])
        self.assertCountEqual(graph.int_to_name.values(), ["n1", "n2", "n3", "n4"])

    def test_betweenness_centrality_1(self):
        nodes = ["n1", "n2", "n3", "n4"]
        edges = [("n1", "n2", 1.0), ("n2", "n3", 1.0), ("n3", "n4", 1.0)]
        graph = grs.create_graph_from_nodes_and_edges(nodes, edges, directed=True)
        self.assertEqual(
            grs.betweenness_centrality(graph, weighted=True, normalized=True),
            {"n1": 0.0, "n2": 0.3333333333333333, "n4": 0.0, "n3": 0.3333333333333333},
        )

    def test_betweenness_centrality_2(self):
        nodes = [11, 12, 13, 14]
        edges = [(11, 12, 1.0), (12, 13, 1.0), (13, 14, 1.0)]
        graph = grs.create_graph_from_nodes_and_edges(nodes, edges, directed=True)
        self.assertEqual(
            grs.betweenness_centrality(graph, weighted=True, normalized=True),
            {11: 0.0, 12: 0.3333333333333333, 13: 0.3333333333333333, 14: 0.0},
        )

    def test_constraint(self):
        graph = nx.karate_club_graph()
        graph = grs.create_graph_from_networkx(graph, weight="weight")
        constraints = grs.constraint(graph, weighted=True)
        self.assertEqual(constraints[0], 0.19062348905638032)

    def test_closeness_centrality(self):
        edges = [("n1", "n2", 1.0), ("n2", "n3", 1.0), ("n3", "n4", 1.0)]
        graph = grs.create_graph_from_edges(edges, directed=True)
        self.assertEqual(
            grs.closeness_centrality(graph, weighted=True, wf_improved=True),
            {"n1": 0.0, "n3": 0.4444444444444444, "n4": 0.5, "n2": 0.3333333333333333},
        )

    def test_clustering(self):
        graph = nx.karate_club_graph()
        graph = grs.create_graph_from_networkx(graph, weight="weight")
        clustering_scores = grs.clustering(graph, weighted=True)
        self.assertAlmostEqual(clustering_scores[0], 0.06631121196141879, 6)

    def test_eigenvector_centrality(self):
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
        result = grs.eigenvector_centrality(graph, weighted=True)
        self.assertAlmostEqual(result["n1"], 0.0, 5)
        self.assertAlmostEqual(result["n2"], 0.577349, 5)
        self.assertAlmostEqual(result["n3"], 0.577349, 5)
        self.assertAlmostEqual(result["n4"], 0.577349, 5)

    def test_spectral_gap(self):
        graph = nx.karate_club_graph()
        graph = grs.create_graph_from_networkx(graph, weight="weight")
        sg = grs.spectral_gap(graph, weighted=True)
        self.assertAlmostEqual(sg, 4.581245823406171, 6)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
