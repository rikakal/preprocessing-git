import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np

precinct_input = input("Enter the precincts file name: ") 
precincts = gpd.read_file(precinct_input)

G = nx.Graph()

for i, row in precincts.iterrows():
    G.add_node(row['id'], geometry=row['geometry'])

# Add edges based on shared boundaries
for i, row in precincts.iterrows():
    precinct_id = row['id']
    neighbors = row['NEIGHBORS']
    shared_boundaries = row['SHARED_BND']
    
    if neighbors is not None:
        n = neighbors.split(", ")
        b = shared_boundaries.split(", ")
        j = 0

        while j < len(n):            
            neighbor_id = precincts.iloc[int(n[j])]['id']

            # Add an edge if it doesn't already exist
            if not G.has_edge(precinct_id, neighbor_id):
                G.add_edge(precinct_id, neighbor_id, shared_boundary=b[j])

            j += 1


nodes_without_geometry = [node for node, data in G.nodes(data=True) if 'geometry' not in data]
G.remove_nodes_from(nodes_without_geometry)


pos = {node: (data['geometry'].centroid.x, data['geometry'].centroid.y) for node, data in G.nodes(data=True)}

# Convert the positions to a 2D NumPy array
pos_array = {node: np.array(pos[node]) for node in pos}

# Draw graph
# nx.draw(G, pos=pos_array, with_labels=True, node_size=10)
# plt.show()

g_name = input("Enter graph name: ")
G.graph['name'] = g_name

output_file = input("Enter output file name: ") 
output_file_path = output_file + ".json"
graph_data = nx.node_link_data(G)
graph_data_json = json.dumps(graph_data, default=str, indent=2)

with open(output_file_path, 'w') as json_file:
    json_file.write(graph_data_json)