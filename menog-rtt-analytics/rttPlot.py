import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import networkx as nx
import community

rtt_min_df = pd.read_csv('graphs/rtt_min.csv', header = 0,index_col=0)
ax = sns.heatmap(rtt_min_df, annot=True, fmt=".0f")
plt.savefig('graphs/rtt_min_heatmap.eps')
plt.savefig('graphs/rtt_min_heatmap.pdf')
plt.show()

rtt_med_df = pd.read_csv('graphs/rtt_med.csv', header = 0,index_col=0)
ax = sns.heatmap(rtt_med_df, annot=True, fmt=".0f")
plt.savefig('graphs/rtt_med_heatmap.eps')
plt.savefig('graphs/rtt_med_heatmap.pdf')
plt.show()

def cluster_compute(rtt_df):
    rtt_dict = rtt_df.to_dict()
    G = nx.from_dict_of_lists(rtt_dict)

    for e1,e2 in list(G.edges):
        G[e1][e2]['weight'] = rtt_df[e1][e2]

    #first compute the best partition
    partition = community.best_partition(G)
    print(partition)

    #drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    #we use the list of partitions 
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                    node_color = str(count / size))

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()

cluster_compute(rtt_min_df)
cluster_compute(rtt_med_df)