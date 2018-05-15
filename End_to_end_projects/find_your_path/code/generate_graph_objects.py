import pandas as pd
import networkx as nx


def combine_two_graphs():
    """
    Create data frame containing edge details
    """
    edges_time = pd.read_csv("../Data/graphs/time_based_graph.csv")
    edges_time = edges_time[["from", "to", "count"]]
    edges_time = edges_time.rename(columns={"count": "median_time"})
    edges_frequency = pd.read_csv("../Data/graphs/highest_frequency.csv")
    edges_frequency = edges_frequency[["from", "to", "count"]]

    edges_time.dropna(inplace=True)
    edges_frequency.dropna(inplace=True)
    combined_df = pd.merge(edges_frequency, edges_time, how='inner',
                           on=['from', 'to'])
    combined_df["median_time"] = combined_df["median_time"]\
        .apply(lambda x: x if x > 0 else 1)
    combined_df["weight1"] = combined_df["median_time"] / combined_df["count"]
    return combined_df


def create_graphs(combined_df, using=None):
    """
    Generate the graph based on type of graph specified
    """
    if using == "most_common":
        edges = [(combined_df.loc[i, "from"], combined_df.loc[i, "to"],
                  combined_df.loc[i, "count"])
                 for i in range(combined_df.shape[0])]
    elif using == "shortest_time":
        edges = [(combined_df.loc[i, "from"], combined_df.loc[i, "to"],
                  combined_df.loc[i, "median_time"])
                 for i in range(combined_df.shape[0])]
    elif using == "min_transitions":
        edges = [(combined_df.loc[i, "from"], combined_df.loc[i, "to"], 1)
                 for i in range(combined_df.shape[0])]
    else:
        edges = [(combined_df.loc[i, "from"], combined_df.loc[i, "to"],
                  combined_df.loc[i, "weight1"])
                 for i in range(combined_df.shape[0])]

    g = nx.graph.Graph()
    g.add_weighted_edges_from(edges)
    return g


def save_graph():
    """
    Save the graphs generated
    """
    combined_df = combine_two_graphs()
    for g in ["most_common", "shortest_time", "min_transitions",
              "combination"]:
        graph = create_graphs(combined_df, g)
        nx.write_gpickle(graph, '../Data/graphs/final_graphs/'+g)


save_graph()
