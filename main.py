import math
import random
from statistics import mean
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


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

# random node with degree > 1


# TODO: custom perturbation
# random perturb and then remove candidate set sizes of 1 and add them to others

def print_statistics(graph):
    print('*** Statistics ***')
    print(f"Degree: ")
    print(f"Diameter: {nx.diameter(graph)}")
    print(f"Avg. Shortest path length: {round(nx.average_shortest_path_length(graph), 3)}")
    print(f"Avg. Closeness: {round(mean(nx.closeness_centrality(graph).values()), 3)}")
    print(f"Avg. Betweenness: {round(mean(nx.betweenness_centrality(graph).values()), 3)}")
    print(f"Clust. Coeff.: {round(nx.average_clustering(graph), 3)}")


def candidate_set_dist(degree_hist):
    candidate_sets = {
        '1': 0,
        '2-4': 0,
        '5-10': 0,
        '11-20': 0,
        '20+': 0
    }

    for i in degree_hist:
        if i == 1:
            candidate_sets['1'] += i
        elif 2 <= i <= 4:
            candidate_sets['2-4'] += i
        elif 5 <= i <= 10:
            candidate_sets['5-10'] += i
        elif 11 <= i <= 20:
            candidate_sets['11-20'] += i
        elif i > 20:
            candidate_sets['20+'] += i

    candidate_sets.update({k: v / sum(candidate_sets.values()) for k, v in candidate_sets.items()})
    return candidate_sets


def h1_candidate_sets(graph):
    degree_hist = nx.degree_histogram(graph)
    return candidate_set_dist(degree_hist)


def perturbation_experiment(graph, name):
    candidate_sets = [h1_candidate_sets(graph)]

    for i in range(1, 11):
        perturbed_graph = randomly_perturb_graph_v2(graph, i * 0.01)
        candidate_sets.append(h1_candidate_sets(perturbed_graph))

    x_axis = [x for x in range(0, 11)]
    y1 = np.array([])
    y2 = np.array([])
    y3 = np.array([])
    y4 = np.array([])

    for candidate_set in candidate_sets:
        y1 = np.append(y1, candidate_set['1'])
        y2 = np.append(y2, candidate_set['2-4'])
        y3 = np.append(y3, candidate_set['5-10'])
        y4 = np.append(y4, candidate_set['11-20'])

    # Stack the candidate set proportions
    y2 = y1 + y2
    y3 = y2 + y3
    y4 = y3 + y4

    # Plot reinditification using H1
    fig, ax = plt.subplots()
    ax.fill_between(x_axis, y1, color='blue', alpha=1)
    ax.fill_between(x_axis, y1, y2, color='blue', alpha=0.6)
    ax.fill_between(x_axis, y2, y3, color='blue', alpha=0.3)
    ax.fill_between(x_axis, y4, y3, color='blue', alpha=0.2)
    plt.xticks([0, 5, 10], ['0%', '5%', '10%'])
    plt.yticks([0.00, 0.20, 0.40, 0.60, 0.80, 1.00])
    plt.margins(x=0, y=0)
    plt.xlabel('Perturbation')
    plt.ylabel('Node proporion')
    plt.title(f'{name}')
    plt.show()

    # Statistics for 0, 5 10 and 100% perturbation
    print_statistics(graph)
    print_statistics(randomly_perturb_graph_v2(graph, 0.05))
    print_statistics(randomly_perturb_graph_v2(graph, 0.1))
    print_statistics(randomly_perturb_graph_v2(graph, 1))


# G = nx.read_edgelist('data/enron.tsv', delimiter='\t', nodetype=int, encoding="utf-8")
# G = nx.read_edgelist('data/CEOclubmembership.csv', delimiter=',', nodetype=int, encoding="utf-8")
# G = nx.read_edgelist('data/edges.csv', delimiter=',', nodetype=int, encoding="utf-8")
G = nx.ring_of_cliques(10, 10)
# G = nx.florentine_families_graph()
# print_statistics(randomly_perturb_graph_v2(G, 0.01))
perturbation_experiment(G, 'CEO club membership')


