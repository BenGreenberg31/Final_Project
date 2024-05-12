# read in network from gexf file

# Calculate degree dist., average shortest path length, triangles aka clustering coefficient, density/sparcity


import networkx as nx

# Read the gexf file into a NetworkX graph
G = nx.read_gexf("director_crew_weighted_updated.gexf")

# Degree distribution
degree_dist = dict(G.degree())

# Average shortest path length
avg_shortest_path_length = nx.average_shortest_path_length(G)


G_undirected = G.to_undirected()
# Triangles (Clustering coefficient)
#triangles = nx.triangles(G_undirected)

# Density
density = nx.density(G)

# Sparsity (1 - Density)
sparsity = 1 - density

# Print or visualize the results
print("Degree Distribution:")
print(degree_dist)

print("\nAverage Shortest Path Length:", avg_shortest_path_length)

print("\nTriangles (Clustering Coefficient):")
#print(triangles)

print("\nDensity:", density)

print("\nSparsity:", sparsity)
