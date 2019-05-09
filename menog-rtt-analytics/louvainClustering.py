#we must install python-louvrain using pip in addition to the relevant libraries that we imported
import community
import networkx as nx
import matplotlib.pyplot as plt

#random graph
G = nx.erdos_renyi_graph(30, 0.05)


#first compute the best partition
partition = community.best_partition(G)

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
