import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from tqdm import tqdm
import time
import maup

# https://dataverse.harvard.edu/dataverse/electionscience

# Function to check if two precincts are indeed neighbors
# ESPG 3857, which uses meters as its unit of measurement
# 200 ft = 60.96 meters
def are_neighbors(precinct1, precinct2, distance=60.96):
    b1 = precinct1.buffer(distance)
    b2 = precinct2.buffer(distance)

    shared_boundary = b1.intersection(b2) # overlapping region between two polygons (ie: their shared boundary)

    if isinstance(shared_boundary, (Polygon, MultiPolygon)):
        if shared_boundary.length >= distance:
            return round(shared_boundary.length, 2) # rounded to 2 decimals
    return None

# Function to find neigbors of each precinct
def find_neighbors(precincts, distance=60.96):
    spatial_index = precincts.sindex

    # precincts.shape[0] gives # rows, .shape[1] gives # columns
    for i, row in tqdm(precincts.iterrows(), total=precincts.shape[0], desc="Processing precincts"):
        precinct_geo = row['geometry']

        # Get indices of the neighbors that intersect with current precent
        nearby_precinct_indices = list(spatial_index.intersection(precinct_geo.bounds))

        # Get precinct itself based on the indices
        nearby_precincts = precincts.iloc[nearby_precinct_indices]

        # Empty lists for neigbors and their shared boundary
        neighbor_list = []
        shared_bound = []

        # nearby_row is a tuple where nearby_row[0] is index, nearby_row[1] is the panda Series
        for nearby_row in nearby_precincts.iterrows(): 
            if nearby_row[1]['id'] == row['id']: # skip self comparison
                continue

            shared_perim = are_neighbors(precinct_geo, nearby_row[1]['geometry'], distance)

            if shared_perim is not None:
                neighbor_list.append(nearby_row[0])
                shared_bound.append(str(shared_perim))

        precincts.at[i, 'NEIGHBORS'] = ', '.join(map(str, neighbor_list))
        precincts.at[i, 'SHARED_BND'] = ', '.join(shared_bound)

    return precincts



# Add population first to Precinct
block_group = gpd.read_file(input("Enter Block Group file name: ")) # Block Group - Race Data
precinct = gpd.read_file(input("Enter Precinct file name: ")) # Precinct

# Convert CRS
crs_type = '3857'
crs_str = f'epsg:{crs_type}'
block_group = block_group.to_crs(crs_str)
precinct = precinct.to_crs(crs_str) 

# Assigning blocks to precincts, and then summing the grouping of the blocks so that we have race data per precinct
print("Assigning blocks to precincts...")
start_time = time.time()
block_to_precinct = maup.assign(block_group, precinct) # Assign block groups to precincts
columns = [col for col in block_group.columns if col.endswith('21')]
precinct[columns] = block_group[columns].groupby(block_to_precinct).sum()
precincts_gdf = precinct.fillna(0)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

# Number each precinct
precincts_gdf['id'] = range(0, len(precincts_gdf))

# Create empty columns for neighbors and their shared boundary
precincts_gdf['NEIGHBORS'] = ''
precincts_gdf['SHARED_BND'] = ''

# Find neighbors
start_time = time.time()
updated_precincts = find_neighbors(precincts_gdf)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

# Export as shapefile
output_shapefile = input("Enter output file name: ")
updated_precincts.to_file(output_shapefile)
print("Successfully created output file.")
