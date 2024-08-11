import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

# Define your start and end locations by their latitude and longitude
start = (30.0444, 31.2357)  # Cairo
end = (29.9773, 31.1325)    # Giza

# Download the road network data from OpenStreetMap
G = ox.graph_from_point(start, dist=10000, network_type='drive')

# Find the nearest nodes in the graph to your start and end points
orig_node = ox.get_nearest_node(G, start)
dest_node = ox.get_nearest_node(G, end)

# Calculate the shortest path based on the road network
route = nx.shortest_path(G, orig_node, dest_node, weight='length')

# Plot the route on the map
fig, ax = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k')
plt.show()
