import itertools
import os
from collections import defaultdict

from graphs import *
from parser import parse

LOG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "logs")


def get_sir_data_per_cycle(tot, infections, patched):

    # dict {cycle: <patched in 'cycle'>}
    patched_cycle = defaultdict(list)
    for key, val in sorted(patched.items()):
        patched_cycle[val].append(key)

    # dict {cycle: <total infected until 'cycle' - patched in 'cycle' that were infected in previous cycles>}
    infections_cycle = {}

    # list built step-by-step containing all the encountered infected nodes
    infected_before = []
    for key, group in itertools.groupby(infections, lambda t: t[2]['cycle']):
        ic = list(dict.fromkeys([i[0] for i in list(group)]))
        ic.extend(list(dict.fromkeys([i[1] for i in list(group)])))
        infected_before.extend([x for x in ic if x not in infected_before])

        infections_cycle[key] = len(infected_before)

        # count the number of patched nodes that were previously infected
        common = len(set(infected_before).intersection(set(patched_cycle.get(key, []))))

        infections_cycle[key] -= common
    data_cycle = defaultdict(list)

    # counter of total patched, increased cycle after cycle
    r = 0
    last_i = 0
    for c in range(0, MAX_TIME, CYCLE):
        # INFECTED / INFECTIVE
        i = infections_cycle.get(c, infections_cycle.get(c-CYCLE, last_i))
        last_i = i if i > 0 else 0
        # RECOVERED / PATCHED
        r += len(patched_cycle.get(c, []))
        # SUSCEPTIBLE (calculated knowing the total number of nodes)
        s = tot - i - r

        data_cycle[c] = [s, i, r]

    return dict(data_cycle)


def analyze_simulation(simulation_filename):

    # parse log file
    res = parse(simulation_filename)

    # number of nodes, list of infections, list of patched
    n, infections, patched = res

    # build and plot the network of infections
    g = plot_graph(n, infections, patched)

    # plot degree distribution for the graph
    plot_degree_distribution(g)

    # process parsed data
    sir_data = get_sir_data_per_cycle(n, infections, patched)

    # plot processed data
    plot_sir_per_cycle(sir_data)

    # plot percentage of infected per cycle
    plot_percentage_per_cycle(n, sir_data)

    # show all the plotted graphs
    plt.show()


if __name__ == '__main__':
    for f in os.listdir(LOG_PATH):
        if f.startswith("contacts"):
            print(f)
            analyze_simulation(os.path.join(LOG_PATH, f))
