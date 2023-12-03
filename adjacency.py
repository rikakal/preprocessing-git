import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, mapping
from tqdm import tqdm
import json

state_code = input("Enter state (MI/NY/PA): ")
if state_code.upper() not in ["MI", "NY", "PA"]:
    print("Wrong input. Exiting.")
    exit()

precinct_input = input("Enter file name: ")
precincts = gpd.read_file(precinct_input)
precincts = precincts.rename(columns={'district': 'CD_2020'})

# Get state boundaries to check if any precincts intersect those boundaries
state_gdf = gpd.read_file(r"data\2022_states\tl_2022_us_state.dbf")
selected_state = state_gdf[state_gdf['STUSPS'] == state_code.upper()]
state_geo = selected_state.geometry.iloc[0]

# Convert the string from 'NEIGHBORS' into int array
precincts['NEIGHBORS'] = precincts['NEIGHBORS'].apply(
    lambda x: [int(float(neighbor)) 
            for neighbor in x.split(',')] 
    if x else []
)

# # Convert the string from 'SHARED_BND' into float array
# precincts['SHARED_BND'] = precincts['SHARED_BND'].apply(
#     lambda x: [float(shared_bnd) 
#         for shared_bnd in x.split(',')] 
#     if x else []
# )






# def find_boundary(precinct1, precinct2):
#     len = precinct1.intersection(precinct2).length
#     return round(len, 8) # round to 8 decimals


# def find_neighbors(p, distance=60.96):
#     spatial_i = p.sindex

#     for i, row in tqdm(p.iterrows(), total=p.shape[0], desc="Boundaries"):
#         geo = row['geometry']
#         if row['NEIGHBORS']:
#             n_list = list(map(int, row['NEIGHBORS']))
#             shared_bound = []
#             for neighbor_index in n_list:
#                 neighbor_row = p.iloc[neighbor_index]
#                 bound = find_boundary(geo, neighbor_row['geometry'])
#                 shared_bound.append(bound)

#         p.at[i, 'SHARED_BND'] = ', '.join(map(str, shared_bound))

#     return p





adjacency_list = [
    [
        {
            "shared_perim": row['geometry'].intersection(
                precincts.loc[neighbor]['geometry']).length,
            "id": neighbor
        }
        for neighbor in row['NEIGHBORS']
    ]
    if row['NEIGHBORS'] else []
    for _, row in precincts.iterrows()
]

# adjacency_list = [
#     [
#         {"shared_perim": shared_bnd, "id": neighbor}
#         for neighbor, shared_bnd in zip(row['NEIGHBORS'], row['SHARED_BND'])
#     ]
#     if row['NEIGHBORS'] else []
#     for _, row in precincts.iterrows()
# ]

# Iterate over rows in GDF and append nodes to the list
nodes_list = []
for i, row in precincts.iterrows():
    area = row['geometry'].area
    geo = row['geometry']
    
    # Check for intersection and calculate length
    if row['geometry'].intersects(state_geo):
        intersection_geometry = row['geometry'].intersection(state_geo)
        boundary_length = intersection_geometry.length
        node_data = {
            "id": row['id'],
            "boundary_node": True,
            "boundary_perim": boundary_length,
            "area": area,
            "geometry": geo,
            **row.drop(['NEIGHBORS', 'geometry']).to_dict()
        }
    else:
        node_data = {
            "id": row['id'],
            "boundary_node": False,
            "area": area,
            "geometry": geo,
            **row.drop(['NEIGHBORS', 'geometry']).to_dict()
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
    json.dump(graph_data, json_file, indent=4, default=lambda o: mapping(o) if isinstance(o, (Polygon, MultiPolygon)) else o)
