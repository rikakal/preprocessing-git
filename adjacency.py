import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, mapping
import json


def flatten_geom(geom_3d):
    if isinstance(geom_3d, Polygon):
        return Polygon([(x, y) for x, y, z in geom_3d.exterior.coords])
    elif isinstance(geom_3d, MultiPolygon):
        return MultiPolygon([Polygon(
            [(x, y) for x, y, z in poly.exterior.coords])
            for poly in geom_3d.geoms])
    else:
        return None


state_code = input('Enter state (MI/NY/PA): ')
if state_code.upper() not in ['MI', 'NY', 'PA']:
    print('Wrong input. Exiting.')
    exit()

precinct_input = input('Enter file name: ')
precincts = gpd.read_file(precinct_input)
precincts = precincts.rename(columns={'district': 'CD_2020'})

state_gdf = gpd.read_file(r'data\2022_states\tl_2022_us_state.dbf')
selected_state = state_gdf[state_gdf['STUSPS'] == state_code.upper()]
state_geo = selected_state.geometry.iloc[0]

precincts['NEIGHBORS'] = precincts['NEIGHBORS'].apply(
    lambda x: [int(float(neighbor))
               for neighbor in x.split(',')]
    if x else []
)

# if state_code.upper() == 'PA':
#     precincts['geometry'] = precincts['geometry'].apply(
#         lambda geom: geom.buffer(0) if not geom.is_valid else geom)
#     precincts['geometry_2d'] = precincts['geometry'].apply(flatten_geom)
#     precincts = precincts.drop(columns=['geometry'])
#     precincts = precincts.rename(columns={'geometry_2d': 'geometry'})
#     precincts = precincts.set_geometry('geometry')

#     crs_type = '4269'
#     crs_str = f'epsg:{crs_type}'
#     precincts = precincts.to_crs(crs_str)

adjacency_list = []
for _, row in precincts.iterrows():
    g = row['geometry']
    neighbors_list = [
        {
            'shared_perim': g.intersection(
                precincts.loc[neighbor]['geometry']).length,
            'id': neighbor
        }
        for neighbor in row['NEIGHBORS']
        #if g.intersection(precincts.loc[neighbor]['geometry']).length > 0
    ]
    adjacency_list.append(neighbors_list if row['NEIGHBORS'] else [])

nodes_list = []
for i, row in precincts.iterrows():
    area = row['geometry'].area
    geo = row['geometry']

    if row['geometry'].intersects(state_geo):
        intersection_geometry = row['geometry'].intersection(state_geo)
        boundary_length = intersection_geometry.length
        node_data = {
            'id': row['id'],
            'boundary_node': True,
            'boundary_perim': boundary_length,
            'area': area,
            'geometry': geo,
            **row.drop(['NEIGHBORS', 'geometry']).to_dict()
        }
    else:
        node_data = {
            'id': row['id'],
            'boundary_node': False,
            'area': area,
            'geometry': geo,
            **row.drop(['NEIGHBORS', 'geometry']).to_dict()
        }

    nodes_list.append(node_data)

graph_data = {
    'directed': False,
    'multigraph': False,
    'graph': [],
    'nodes': nodes_list,
    'adjacency': adjacency_list
}

output_file = input('Enter output file name: ')
output_file_path = output_file + '.json'
with open(output_file_path, 'w') as json_file:
    # Mapping to seralize Polygon shapes
    json.dump(graph_data, json_file, indent=4, default=lambda obj: mapping(obj)
              if isinstance(obj, (Polygon, MultiPolygon)) else obj)
