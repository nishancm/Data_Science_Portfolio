
# Asmita Vikas
import ast
import json
import os
from collections import defaultdict

import pandas as pd


def find_shortest_time_paths(path, input_title):
    """
    Given an input, find the top 3 outputs based on shortest time
    """
    time_edgelist = pd.read_csv(path + 'time_based_graph.csv', index_col=0)
    output = time_edgelist[time_edgelist['from'] == input_title].\
        sort_values(by='weighted_avg')[:3]['to']
    return list(output.values)


if __name__ == '__main__':
    path = '../Data/graphs/'

    input_title = 'senior engineer'
    output_title = find_shortest_time_paths(input_title)
