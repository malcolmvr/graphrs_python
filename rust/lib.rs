use pyo3::prelude::*;

#[pymodule]
mod _lib {

    use graphrs::{algorithms, Edge, Graph as GraphRS, GraphSpecs, Node};
    use pyo3::prelude::*;
    use std::collections::HashMap;

    #[pyclass]
    struct Graph {
        pub graph: GraphRS<usize, ()>,
    }

    #[pyfunction]
    fn create_graph(
        nodes: Vec<usize>,
        edges: Vec<(usize, usize, f64)>,
        directed: bool,
        create_missing: bool,
    ) -> PyResult<Graph> {
        let _nodes = nodes.into_iter().map(|n| Node::from_name(n)).collect();
        let _edges = edges
            .into_iter()
            .map(|(a, b, w)| Edge::with_weight(a, b, w))
            .collect();
        let mut specs = match directed {
            true => GraphSpecs::directed(),
            false => GraphSpecs::undirected(),
        };
        specs.self_loops = true;
        if create_missing {
            specs.missing_node_strategy = graphrs::MissingNodeStrategy::Create;
        }
        let graph = GraphRS::new_from_nodes_and_edges(_nodes, _edges, specs).unwrap();
        Ok(Graph { graph })
    }

    #[pyfunction]
    fn betweenness_centrality(graph: &Graph, weighted: bool, normalized: bool) -> PyResult<HashMap<usize, f64>> {
        let betweenness_centrality =
            algorithms::centrality::betweenness::betweenness_centrality(&graph.graph, weighted, normalized);
        Ok(betweenness_centrality.unwrap())
    }

    #[pyfunction]
    fn closeness_centrality(graph: &Graph, weighted: bool, wf_improved: bool) -> PyResult<HashMap<usize, f64>> {
        let closeness_centrality =
            algorithms::centrality::closeness::closeness_centrality(&graph.graph, weighted, wf_improved);
        Ok(closeness_centrality.unwrap())
    }

    #[pyfunction]
    fn clustering(graph: &Graph, weighted: bool) -> PyResult<HashMap<usize, f64>> {
        let clustering_scores =
            algorithms::cluster::clustering(&graph.graph, weighted, None).unwrap();
        Ok(clustering_scores)
    }

    #[pyfunction]
    fn constraint(graph: &Graph, weighted: bool) -> PyResult<HashMap<usize, f64>> {
        let constraints =
            algorithms::structural_holes::constraint::constraint(&graph.graph, None, weighted);
        Ok(constraints)
    }

    #[pyfunction]
    #[pyo3(signature = (graph, weighted, max_iter=None, tolerance=None))]
    fn eigenvector_centrality(graph: &Graph, weighted: bool, max_iter: Option<u32>, tolerance: Option<f64>) -> PyResult<HashMap<usize, f64>> {
        let eigenvector_centrality =
            algorithms::centrality::eigenvector::eigenvector_centrality(&graph.graph, weighted, max_iter, tolerance);
        Ok(eigenvector_centrality.unwrap())
    }

    #[pyfunction]
    fn spectral_gap(graph: &Graph, weighted: bool) -> PyResult<f64> {
        let sg =
            algorithms::resiliency::spectral_gap::spectral_gap(&graph.graph, weighted).unwrap();
        Ok(sg)
    }

}
