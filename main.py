import networkx as nx
import matplotlib.pyplot as plt
from statistics import mean
import random
import math


def randomly_perturb_graph_complete(graph, percentage):
    perturbed_graph = graph.copy()
    perturbations = math.floor(nx.number_of_edges(perturbed_graph) * percentage)

    for i in range(perturbations):
        edge_to_delete = random.choice(list(nx.edges(perturbed_graph)))
        edge_to_add = random.choice(list(nx.non_edges(perturbed_graph)))

        perturbed_graph.remove_edge(*edge_to_delete)
        perturbed_graph.add_edge(*edge_to_add)

    return perturbed_graph


def randomly_perturb_graph_faster(graph, percentage):
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
    print(f"Avg. Degree: {mean([x[1] for x in graph.degree()])}")
    print(f"Diameter: {nx.diameter(graph)}")
    print(f"Avg. Path length: -")
    print(f"Avg. Closeness: {closeness_cent}")
    print(f"Avg. Betweenness: -")
    print(f"Clust. Coeff.: -")

# TODO: reindentification experiment

# TODO: custom perturbation


G = nx.ring_of_cliques(10, 10)
G_prime = randomly_perturb_graph_faster(G, 0.1)

print_statistics(G)
print_statistics(G_prime)

print(G.degree())
