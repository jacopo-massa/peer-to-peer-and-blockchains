import collections

import matplotlib.pyplot as plt
import networkx as nx
from networkx.exception import NetworkXError

from config import *


def relabel_patched(nodes, patched_nodes):
    result = {}
    for node in nodes:
        if node in patched_nodes:
            result[node] = node + "\n " + str(patched_nodes[node])
        else:
            result[node] = node

    return result


def plot_graph(n, infections, patched):

    # create Graph
    g = nx.DiGraph()

    node_list = ["n{}".format(i) for i in range(n)]

    # add nodes and edges
    g.add_nodes_from(node_list)
    g.add_edges_from(infections)

    # calculate some statistics for the graph
    clustering_coefficient = nx.average_clustering(g)
    density = nx.density(g)
    try:
        diameter = nx.diameter(g)
    except NetworkXError:
        diameter = "infinite"

    # relabel the nodes, adding the cycle when they've been patched
    g = nx.relabel_nodes(g, relabel_patched(node_list, patched), copy=False)

    pos = nx.spring_layout(g)

    # draw nodes
    nx.draw_networkx_nodes(g, pos, node_size=NODE_SIZE, node_color=NODE_COLOR)

    # draw nodes' labels
    nx.draw_networkx_labels(g, pos, font_size=NODE_LABEL_SIZE, font_color=NODE_LABEL_COLOR)

    # draw edges
    nx.draw_networkx_edges(g, pos, node_size=NODE_SIZE, arrowstyle='->', arrowsize=5, edge_color='black',
                           width=EDGE_WIDTH)

    # draw edges' labels
    edge_labels = nx.get_edge_attributes(g, 'cycle')
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, alpha=EDGE_LABEL_ALPHA, label_pos=0.5,
                                 font_size=EDGE_LABEL_SIZE, font_color=EDGE_LABEL_COLOR)

    text = "Clustering coefficient = {}\n" \
           "Diameter = {}\n" \
           "Density = {}".format(clustering_coefficient, diameter, density)

    properties = dict(boxstyle='round', facecolor='wheat', alpha=0.4)
    plt.text(-1.2, -1.2, text, fontsize=10, verticalalignment='top', bbox=properties)

    return g


def plot_degree_distribution(g):
    degree_sequence = sorted([d for n, d in g.degree()], reverse=True)  # degree sequence
    # print "Degree sequence", degree_sequence
    degree_count = collections.Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())

    plt.subplots()
    plt.bar(deg, cnt, width=0.80, color='b')

    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")


def plot_sir_per_cycle(data):
    fig = plt.figure()
    a = fig.add_subplot(111)

    a.set_title("SIR Data")
    a.set_xlabel('Cycle')
    a.set_ylabel('Number of nodes')

    yvalues = data.values()
    xvalues = [x//CYCLE for x in list(data.keys())]
    a.set_xbound(0, max(xvalues))

    s = [x[0] for x in yvalues]
    i = [x[1] for x in yvalues]
    r = [x[2] for x in yvalues]

    a.plot(xvalues, s, label="Susceptible")
    a.plot(xvalues, i, label="Infectious")
    a.plot(xvalues, r, label="Recovered")
    a.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)


def plot_percentage_per_cycle(tot, data):
    fig = plt.figure()
    a = fig.add_subplot(111)

    a.set_title('% infected/cycle')
    a.set_xlabel('Number of cycles')
    a.set_ylabel('Percentage fo nodes')

    yvalues = [100*x[1]/tot for x in data.values()]
    xvalues = [x//CYCLE for x in list(data.keys())]

    a.plot(xvalues, yvalues)
