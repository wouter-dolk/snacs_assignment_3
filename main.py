import networkx as nx
import matplotlib.pyplot as plt
import random
import math


def randomly_perturb_graph(G, percentage):
    perturbations = math.floor(nx.number_of_edges(G) * percentage)

    # TODO: create variant that cals nx edges and non edges once

    for i in range(perturbations):
        edge_to_delete = random.choice(list(nx.edges(G)))
        edge_to_add = random.choice(list(nx.non_edges(G)))

        G.remove_edge(*edge_to_delete)
        G.add_edge(*edge_to_add)

    return G


G = nx.ring_of_cliques(10, 10)
randomly_perturb_graph(G)

# make function that prints statistics for a network, so we can already compare utility of pre and post perturbation
