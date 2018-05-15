# spencer stanley

import sys

# import pandas as pd


def top3(current_node):
    """
    return 3 most frequent next steps for given job title
    """

    graph = pd.read_csv('../../Data/graphs/highest_frequency.csv')

    filter_g = graph.loc[graph['from'] == current_node, ['to', 'count']]
    top3 = filter_g.sort_values('count', ascending=False).to[:3]

    return ', '.join(top3)
