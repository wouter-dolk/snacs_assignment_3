import math
import random
from statistics import mean
import networkx as nx


def randomly_perturb_graph_v1(graph, percentage):
    perturbed_graph = graph.copy()
    perturbations = math.floor(nx.number_of_edges(perturbed_graph) * percentage)

    for i in range(perturbations):
        edge_to_delete = random.choice(list(nx.edges(perturbed_graph)))
        edge_to_add = random.choice(list(nx.non_edges(perturbed_graph)))

        perturbed_graph.remove_edge(*edge_to_delete)
        perturbed_graph.add_edge(*edge_to_add)

    return perturbed_graph


def randomly_perturb_graph_v2(graph, percentage):
    perturbed_graph = graph.copy()
    perturbations = math.floor(nx.number_of_edges(perturbed_graph) * percentage)

    edges = list(nx.edges(perturbed_graph))
    non_edges = list(nx.non_edges(perturbed_graph))

    for i in range(perturbations):
        edge_to_delete = random.choice(edges)
        edge_to_add = random.choice(non_edges)

        perturbed_graph.remove_edge(*edge_to_delete)
        perturbed_graph.add_edge(*edge_to_add)

        # Update edge and non_edge lists
        edges.remove(edge_to_delete)
        edges.append(edge_to_add)
        non_edges.remove(edge_to_add)
        non_edges.append(edge_to_delete)

    return perturbed_graph


def print_statistics(graph):
    closeness = nx.closeness_centrality(graph)
    closeness_cent = mean(closeness.values())

    print('*** Statistics ***')
    print(f"Degree: what does the paper measure?")
    print(f"Diameter: {nx.diameter(graph)}")
    print(f"Avg. Shortest path length: {round(nx.average_shortest_path_length(graph), 3)}")
    print(f"Avg. Closeness: {round(closeness_cent, 3)}")
    print(f"Avg. Betweenness: {round(mean(nx.betweenness_centrality(graph).values()), 3)}")
    print(f"Clust. Coeff.: {round(nx.average_clustering(graph), 3)}")

# TODO: reindentification experiment

# TODO: custom perturbation


G = nx.ring_of_cliques(10, 10)
G_prime = randomly_perturb_graph_v2(G, 0.1)

print_statistics(G)
print_statistics(G_prime)
