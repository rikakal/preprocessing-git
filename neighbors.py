import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from tqdm import tqdm
import time
import maup

# ESPG 3857, which uses meters as its unit of measurement
# 200 ft = 60.96 meters
def are_neighbors(precinct1, precinct2, distance=60.96):
    b1 = precinct1.buffer(distance)
    b2 = precinct2.buffer(distance)

    shared_boundary = b1.intersection(b2)

    if isinstance(shared_boundary, (Polygon, MultiPolygon)):
        if shared_boundary.length >= distance:
            return round(shared_boundary.length, 2)
    return None

# Function to find neigbors of each precinct
def find_neighbors(p, distance=60.96):
    spatial_i = p.sindex

    # precincts.shape[0] gives # rows, .shape[1] gives # columns
    for i, row in tqdm(p.iterrows(), total=p.shape[0], desc="Processing"):
        geo = row['geometry']

        nearby_p_indices = list(spatial_i.intersection(geo.bounds))
        nearby_p = p.iloc[nearby_p_indices]

        neighbor_list = []
        shared_bound = []

        # nearby_row[0] is index, nearby_row[1] is the panda Series
        for nearby_row in nearby_p.iterrows(): 
            if nearby_row[1]['id'] == row['id']: # skip self comparison
                continue

            perim = are_neighbors(geo, nearby_row[1]['geometry'], distance)

            if perim is not None:
                neighbor_list.append(nearby_row[0])
                shared_bound.append(str(perim))

        p.at[i, 'NEIGHBORS'] = ', '.join(map(str, neighbor_list))
        p.at[i, 'SHARED_BND'] = ', '.join(shared_bound)

    return p

block_group = gpd.read_file(input("Enter Block Group file name: ")) 
precinct = gpd.read_file(input("Enter Precinct file name: "))

crs_type = '3857'
crs_str = f'epsg:{crs_type}'
block_group = block_group.to_crs(crs_str)
precinct = precinct.to_crs(crs_str) 

# Assigning blocks to precincts, and then summing the grouping of the blocks
print("Assigning blocks to precincts...")
start_time = time.time()
block_to_precinct = maup.assign(block_group, precinct)
columns = [col for col in block_group.columns if col.endswith('21')]
precinct[columns] = block_group[columns].groupby(block_to_precinct).sum()
precincts_gdf = precinct.fillna(0)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

precincts_gdf['id'] = range(0, len(precincts_gdf))

precincts_gdf['NEIGHBORS'] = ''
precincts_gdf['SHARED_BND'] = ''

start_time = time.time()
updated_precincts = find_neighbors(precincts_gdf)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

output_shapefile = input("Enter output file name: ")
updated_precincts.to_file(output_shapefile)
print("Successfully created output file.")
