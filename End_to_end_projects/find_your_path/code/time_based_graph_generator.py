
# Asmita Vikas

import ast
import json
import os
from collections import defaultdict

import pandas as pd
import numpy as np


def to_time_graph():
    """
    return a graph whose edges are weighted by
    the number of years it took from A to B
    """
    path = '../Data/job_profiles/'
    profiles = []
    with open(path + 'all_jobs.json') as f:
        for line in f:
            line = line.strip()
            line = ast.literal_eval(line)
            profiles.append(line)

    # initialize graph
    graph = defaultdict(lambda: defaultdict(list))
    # construct graph
    for j in range(len(profiles)):
        events = profiles[j]['events']
        for i in range(len(events) - 1):
            try:
                graph[events[i][1]][events[i + 1][1]
                                    ].append(events[i + 1][0] - events[i][0])
            except BaseException:
                pass

    return graph


def to_edgelist(graph):
    """
    Given graph as dictionary, convert to edgelist
    """
    edgelist = pd.DataFrame(columns=['from', 'to', 'count'])
    for key in graph.keys():
        for skey in graph[key]:
            edgelist.loc[len(edgelist), ['from', 'to', 'count']] = [
                key, skey, np.median(graph[key][skey])
            ]

    return edgelist


def clean_edgelist(e):
    """
    clean the junk out of edgelists
    """
    e = e[(e['from'] != '') & (e['to'] != '')]  # removing all the empty 'from'
    e['count'] = e['count'].fillna(1111)  # remove nan to a really high number
    e = e[e['from'] != e['to']]
    return e


if __name__ == '__main__':
    g = to_time_graph()
    e = to_edgelist(g)
    edgelist = clean_edgelist(e)

    edgelist.to_csv('../Data/graphs/time_based_graph.csv')
