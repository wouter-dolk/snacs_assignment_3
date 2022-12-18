import math
import random
from statistics import mean, median
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import time


def randomly_perturb_graph_v1(graph, percentage):
    start = time.time()

    perturbed_graph = graph.copy()
    perturbations = math.floor(nx.number_of_edges(perturbed_graph) * percentage)

    for i in range(perturbations):
        edge_to_delete = random.choice(list(nx.edges(perturbed_graph)))
        edge_to_add = random.choice(list(nx.non_edges(perturbed_graph)))

        perturbed_graph.remove_edge(*edge_to_delete)
        perturbed_graph.add_edge(*edge_to_add)

    end = time.time()
    print(f'Network perturbation time: {round(end - start, 3)}s')

    return perturbed_graph


def randomly_perturb_graph_v2(graph, percentage):
    start = time.time()
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

    end = time.time()
    print(f'Network perturbation time: {round(end - start, 3)}s')

    return perturbed_graph


def randomly_perturb_graph_v3(graph, percentage):
    start = time.time()
    perturbed_graph = graph.copy()
    perturbations = math.floor(nx.number_of_edges(perturbed_graph) * percentage)

    edges = list(nx.edges(perturbed_graph))
    non_edges = list(nx.non_edges(perturbed_graph))

    for i in range(perturbations):
        edge_to_delete = random.choice(edges)
        perturbed_graph.remove_edge(*edge_to_delete)

        # Prevent isolate nodes
        isolates = list(nx.isolates(G))
        if len(isolates) > 0:
            filtered_non_edges = list(filter(lambda x: isolates[0] in x, non_edges))
            edge_to_add = random.choice(filtered_non_edges)
        else:
            edge_to_add = random.choice(non_edges)

        perturbed_graph.add_edge(*edge_to_add)

        # Update edge and non_edge lists
        edges.remove(edge_to_delete)
        edges.append(edge_to_add)
        non_edges.remove(edge_to_add)
        non_edges.append(edge_to_delete)

    end = time.time()
    # print(f'Network perturbation time: {round(end - start, 3)}s')

    return perturbed_graph


def custom_perturbation(graph, step_threshold):
    perturbed_graph = graph.copy()

    degree_dist = np.array(nx.degree_histogram(perturbed_graph))
    node_degrees_with_candidate_size_of_one = np.where(degree_dist == 1)[0]

    nodes = np.array(perturbed_graph.degree())
    for degree in node_degrees_with_candidate_size_of_one:

        nearest_degree = 0
        for i in range(1, step_threshold + 1):
            if degree - i > 0 and degree_dist[degree - i] > 1:
                nearest_degree = -i
                break
            if degree + i < len(degree_dist) and degree_dist[degree + i] > 1:
                nearest_degree = i
                break

        if nearest_degree > 0:
            node = nodes[np.where(nodes[:, 1] == degree)][0][0]
            edges = [x[1] for x in list(perturbed_graph.edges(node))]
            non_edges = [x for x in perturbed_graph.nodes() if x not in edges]
            for i in range(nearest_degree):
                edge_to_add = random.choice(non_edges)
                perturbed_graph.add_edge(node, edge_to_add)
                non_edges.remove(edge_to_add)
        elif nearest_degree < 0:
            node = nodes[np.where(nodes[:, 1] == degree)][0][0]
            edges = list(perturbed_graph.edges(node))
            for i in range(abs(nearest_degree)):
                edge_to_delete = random.choice(edges)
                perturbed_graph.remove_edge(*edge_to_delete)
                edges.remove(edge_to_delete)

    return perturbed_graph


def print_statistics(graph):
    print('*** Statistics ***')
    print(f"Median Degree: {median([tup[1] for tup in graph.degree()])}")
    try:
        print(f"Diameter: {nx.diameter(graph)}")
        print(f"Avg. Shortest path length: {round(nx.average_shortest_path_length(graph), 3)}")
    except nx.NetworkXError:
        print(f"Diameter: -")
        print(f"Avg. Shortest path length: -")
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

    perturbed_graph = graph
    for i in range(1, 11):
        # Add 1% perturbation every time
        perturbed_graph = randomly_perturb_graph_v3(perturbed_graph, 0.01)
        candidate_sets.append(h1_candidate_sets(perturbed_graph))

    x_axis = [x for x in range(0, 11)]
    y1 = np.array([])
    y2 = np.array([])
    y3 = np.array([])
    y4 = np.array([])
    y5 = np.array([])

    for candidate_set in candidate_sets:
        y1 = np.append(y1, candidate_set['1'])
        y2 = np.append(y2, candidate_set['2-4'])
        y3 = np.append(y3, candidate_set['5-10'])
        y4 = np.append(y4, candidate_set['11-20'])
        y5 = np.append(y5, candidate_set['20+'])

    # Stack the candidate set proportions
    y2 = y1 + y2
    y3 = y2 + y3
    y4 = y3 + y4
    y5 = y4 + y5

    # Plot reinditification using H1
    fig, ax = plt.subplots()
    ax.fill_between(x_axis, y1, color='blue', alpha=1)
    ax.fill_between(x_axis, y1, y2, color='blue', alpha=0.6)
    ax.fill_between(x_axis, y2, y3, color='blue', alpha=0.3)
    ax.fill_between(x_axis, y4, y3, color='blue', alpha=0.2)
    ax.fill_between(x_axis, y5, y4, color='white', alpha=0)
    plt.xticks([0, 5, 10], ['0%', '5%', '10%'])
    plt.yticks([0.00, 0.20, 0.40, 0.60, 0.80, 1.00])
    plt.margins(x=0, y=0)
    plt.xlabel('Perturbation')
    plt.ylabel('Node proporion')
    plt.title(f'{name}')
    plt.show()


def perturbation_experiment_2(graph, name):
    candidate_sets = [h1_candidate_sets(graph)]

    for i in range(1, 11):
        perturbed_graph = custom_perturbation(graph, i)
        candidate_sets.append(h1_candidate_sets(perturbed_graph))

    x_axis = [x for x in range(0, 11)]
    y1 = np.array([])
    y2 = np.array([])
    y3 = np.array([])
    y4 = np.array([])
    y5 = np.array([])

    for candidate_set in candidate_sets:
        y1 = np.append(y1, candidate_set['1'])
        y2 = np.append(y2, candidate_set['2-4'])
        y3 = np.append(y3, candidate_set['5-10'])
        y4 = np.append(y4, candidate_set['11-20'])
        y5 = np.append(y5, candidate_set['20+'])

    # Stack the candidate set proportions
    y2 = y1 + y2
    y3 = y2 + y3
    y4 = y3 + y4
    y5 = y4 + y5

    # Plot reinditification using H1
    fig, ax = plt.subplots()
    ax.fill_between(x_axis, y1, color='purple', alpha=1)
    ax.fill_between(x_axis, y1, y2, color='purple', alpha=0.6)
    ax.fill_between(x_axis, y2, y3, color='purple', alpha=0.3)
    ax.fill_between(x_axis, y4, y3, color='purple', alpha=0.2)
    ax.fill_between(x_axis, y5, y4, color='white', alpha=0)
    # plt.xticks([0, 5, 10], ['0%', '5%', '10%'])
    plt.yticks([0.00, 0.20, 0.40, 0.60, 0.80, 1.00])
    plt.margins(x=0, y=0)
    plt.xlabel('Maximum step size')
    plt.ylabel('Node proporion')
    plt.title(f'{name}')
    plt.show()


def utility_experiment(graph):
    # Statistics for 0, 5, 10 and 100% perturbation
    print_statistics(graph)
    print_statistics(randomly_perturb_graph_v3(graph, 0.05))
    print_statistics(randomly_perturb_graph_v3(graph, 0.1))
    print_statistics(randomly_perturb_graph_v3(graph, 1))


# Old datasets
# G = nx.read_edgelist('data/enron.tsv', delimiter='\t', nodetype=int, encoding="utf-8")
# G = nx.read_edgelist('data/CEOclubmembership.csv', delimiter=',', nodetype=int, encoding="utf-8")
# G = nx.read_edgelist('data/dolphin.csv', delimiter=',', nodetype=int, encoding="utf-8")

# Current datasets
G = nx.read_edgelist('data/football.csv', delimiter=',', nodetype=int, encoding="utf-8")
# G = nx.read_edgelist('data/gameofthrone.csv', delimiter=',', nodetype=int, encoding="utf-8", data=(("weight", float),))
# G = nx.read_edgelist('data/copenhagen.csv', delimiter=',', nodetype=int, encoding="utf-8")
# G = nx.read_edgelist('data/email.csv', delimiter=',', nodetype=int, encoding="utf-8")
# G = nx.read_edgelist('data/bitcoin.csv', delimiter=',', nodetype=int, encoding="utf-8", data=(("rating", float),("time", float)))

# perturbation_experiment(G, 'Bitcoin')
perturbation_experiment_2(G, 'Footballl')
# utility_experiment(G)