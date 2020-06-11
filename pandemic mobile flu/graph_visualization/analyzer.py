import networkx as nx
import matplotlib.pyplot as plt


from config import *
from parser import parse


def relabel_patched(nodes, patched_nodes):
    result = {}
    for node in nodes:
        if node in patched_nodes:
            result[node] = node + "\n " + str(patched_nodes[node])
        else:
            result[node] = node

    return result


# parse log file
res = parse('contacts.txt')

# number of nodes, list of infections, list of patched
n, infections, patched = res

# create Graph
g = nx.DiGraph()

node_list = ["n{}".format(i) for i in range(n)]

# add nodes and edges
g.add_nodes_from(node_list)
g.add_edges_from(infections)

# relabel the nodes, adding the cycle when they've been patched
g = nx.relabel_nodes(g, relabel_patched(node_list, patched), copy=False)

pos = nx.spring_layout(g)
# draw nodes
nx.draw_networkx_nodes(g, pos, node_size=NODE_SIZE, node_color=NODE_COLOR)
# draw nodes' labels
nx.draw_networkx_labels(g, pos, font_size=NODE_LABEL_SIZE, font_color=NODE_LABEL_COLOR)

# draw edges
nx.draw_networkx_edges(g, pos, node_size=NODE_SIZE, arrowstyle='->', arrowsize=5,
                               edge_color='black', width=EDGE_WIDTH)

# draw edges' labels
edge_labels = nx.get_edge_attributes(g, 'cycle')
nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels, alpha=EDGE_LABEL_ALPHA, label_pos=0.5,
                             font_size=EDGE_LABEL_SIZE, font_color=EDGE_LABEL_COLOR)
plt.show()
