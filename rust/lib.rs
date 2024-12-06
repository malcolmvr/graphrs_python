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
    fn eigenvector_centrality(graph: &Graph, weighted: bool) -> PyResult<HashMap<usize, f64>> {
        let eigenvector_centrality =
            algorithms::centrality::eigenvector::eigenvector_centrality(&graph.graph, weighted, None, None);
        Ok(eigenvector_centrality.unwrap())
    }

    // #[pyfunction]
    // fn betweenness_centrality(graphml_string: &str) -> PyResult<HashMap<String, f64>> {
    //     let specs = GraphSpecs::undirected();
    //     let graph = graphrs::readwrite::graphml::read_graphml_string(graphml_string, specs).unwrap();
    //     let betweenness_centrality = algorithms::centrality::betweenness::betweenness_centrality(&graph, true, true);
    //     Ok(betweenness_centrality.unwrap())
    // }
}
