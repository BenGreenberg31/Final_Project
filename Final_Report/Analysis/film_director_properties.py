# read in network from gexf file

# Calculate degree dist., average shortest path length, triangles aka clustering coefficient, density/sparcity


import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.cluster import average_clustering

G = nx.read_gexf("director_crew_weighted_updated.gexf")

# Degree distribution
#degrees = dict(G.degree())

#Average shortest path length
avg_shortest_path_length = nx.average_shortest_path_length(G)


G_undirected = G.to_undirected()
#avg clustering coefficient
average_clustering = nx.average_clustering(G_undirected)


density = nx.density(G)

sparsity = 1 - density

print("\nAverage Shortest Path Length:", avg_shortest_path_length)

print("\nAverage Clustering Coefficient:")
print(average_clustering)

print("\nDensity:", density)

print("\nSparsity:", sparsity)
