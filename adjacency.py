import geopandas as gpd
from shapely.validation import explain_validity

import json

state_code = input("Enter state (MI/NY/PA): ")
if state_code.upper() not in ["MI", "NY", "PA"]:
    print("Wrong input. Exiting.")
    exit()

precinct_input = input("Enter the precincts file name: ")
precincts = gpd.read_file(precinct_input)
precincts = precincts.rename(columns={'district': 'CD_2020'})

# Get state boundaries to check if any precincts intersect those boundaries
state_gdf = gpd.read_file(r"data\2022_states\tl_2022_us_state.dbf")
selected_state = state_gdf[state_gdf['STUSPS'] == state_code.upper()]
state_geo = selected_state.geometry.iloc[0]

# Convert the string from 'NEIGHBORS' into int array
precincts['NEIGHBORS'] = precincts['NEIGHBORS'].apply(
    lambda x: [
        int(neighbor) 
        for neighbor in x.split(',')
    ] 
    if x else []
)

# Convert the string from 'SHARED_BND' into float array
precincts['SHARED_BND'] = precincts['SHARED_BND'].apply(
    lambda x: [
        float(shared_bnd) 
        for shared_bnd in x.split(',')
    ] 
    if x else []
)

adjacency_list = [
    [
        {"shared_perim": shared_bnd, "id": neighbor}
        for neighbor, shared_bnd in zip(row['NEIGHBORS'], row['SHARED_BND'])
    ]
    if row['NEIGHBORS'] else []
    for _, row in precincts.iterrows()
]

# Iterate over rows in GDF and append nodes to the list
nodes_list = []
for i, row in precincts.iterrows():
    area = row['geometry'].area

    # Check for intersection and calculate length
    if row['geometry'].intersects(state_geo):
        intersection_geometry = row['geometry'].intersection(state_geo)
        boundary_length = intersection_geometry.length
        node_data = {
            "id": row['id'],
            "boundary_node": True,
            "boundary_perim": boundary_length,
            "area": area,
            **row.drop(['geometry', 'NEIGHBORS', 'SHARED_BND']).to_dict()
        }
    else:
        node_data = {
            "id": row['id'],
            "boundary_node": False,
            "area": area,
            **row.drop(['geometry', 'NEIGHBORS', 'SHARED_BND']).to_dict()
        }

    nodes_list.append(node_data)

# Create graph data dictionary with "nodes" as a list
graph_data = {
    "directed": False,
    "multigraph": False,
    "graph": [],
    "nodes": nodes_list,
    "adjacency": adjacency_list
}

output_file = input("Enter output file name: ")
output_file_path = output_file + ".json"
with open(output_file_path, 'w') as json_file:
    json.dump(graph_data, json_file, indent=4)
