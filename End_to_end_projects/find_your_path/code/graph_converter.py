# spencer stanley

"""file to turn json-encoded sequential experience
data into edgelist-representation graphs
"""

import ast
import json
import os
from collections import defaultdict

import pandas as pd


def to_count_graph():
    """return a graph whose edges are weighted
    by the count of items on the edge;
    i.e., the number of people who have made the
    transition from position A to position B
    """
    # get json
    path = '../Data/job_profiles/'
    profiles = []
    with open(path + 'all_jobs.json') as f:
        for line in f:
            line = line.strip()
            line = ast.literal_eval(line)
            profiles.append(line)

    # initialize graph
    graph = defaultdict(lambda: defaultdict(int))

    # construct graph
    for j in range(len(profiles)):
        if isinstance(profiles[j], list):
            # dictionaries are nested in lists
            for k in range(len(profiles[j])):
                events = profiles[j][k]['events']
                for i in range(len(events) - 1):
                    if events[i][1] != events[i + 1][1]:
                        graph[events[i][1]][events[i + 1][1]] += 1
        else:
            # data is already a dictionary
            events = profiles[j]['events']
            for i in range(len(events) - 1):
                if events[i][1] != events[i + 1][1]:
                    graph[events[i][1]][events[i + 1][1]] += 1

    return graph


def to_edgelist(graph):
    """take a dictionary representation of a graph
    and return an edgelist

    :param: graph: dictionary as {
        position: {position: n people}
    }; i.e., for each position/event, how many people moved to
    each subsequent position

    :return: edgelist: pd DataFrame of from, to, count
    """
    edgelist = pd.DataFrame(columns=['from', 'to', 'count'])

    # build edgelist out of graph; fairly straightforward
    for key in graph.keys():
        for skey in graph[key]:
            edgelist.loc[len(edgelist), ['from', 'to', 'count']] = [
                key, skey, graph[key][skey]
            ]

    weights = edgelist.groupby('from')['count'].sum()
    edgelist['weight'] = edgelist.apply(
        lambda x: weights[x['from']] / x['count'],
        axis=1
    )

    return edgelist


if __name__ == '__main__':
    g = to_count_graph()
    e = to_edgelist(g)
    e.to_csv('../Data/graphs/highest_frequency.csv', index=False)
