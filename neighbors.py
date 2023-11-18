import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from tqdm import tqdm
import time

# https://dataverse.harvard.edu/dataverse/electionscience

def remove_dups(precincts):
    original_count = precincts.shape[0]  # Get the original row count
    unique_precincts = precincts.drop_duplicates(subset=[col1, col3]).copy()
    removed_count = original_count - unique_precincts.shape[0]  # Calculate the number of removed rows
    return unique_precincts, removed_count

# ESPG 3857, which uses meters as its unit of measurement
# 200 ft = 60.96 meters
def are_neighbors(precinct1, precinct2, distance=60.96):
    b1 = precinct1.buffer(distance)
    b2 = precinct2.buffer(distance)

    shared_boundary = b1.intersection(b2) # overlapping region between two polygons (ie: their shared boundary)

    if isinstance(shared_boundary, (Polygon, MultiPolygon)):
        if shared_boundary.length >= distance:
            return round(shared_boundary.length, 5) # rounded to 5 decimal places
    return None

def find_neighbors(precincts, distance=60.96):
    spatial_index = precincts.sindex

    # precincts.shape[0] gives # rows, .shape[1] gives # columns
    for i, row in tqdm(precincts.iterrows(), total=precincts.shape[0], desc="Processing precincts"):
        precinct_geo = row['geometry']

        nearby_precinct_indices = list(spatial_index.intersection(precinct_geo.bounds))
        nearby_precincts = precincts.iloc[nearby_precinct_indices]

        neighbor_list = []
        shared_bound = []
        for nearby_row in nearby_precincts.iterrows():
            if nearby_row[1]['id'] == row['id']:
                continue

            shared_perim = are_neighbors(precinct_geo, nearby_row[1]['geometry'], distance)
            if shared_perim is not None:
                neighbor_list.append(nearby_row[1]['id'])
                shared_bound.append(str(shared_perim))

        precincts.at[i, 'NEIGHBORS'] = ', '.join(neighbor_list)
        precincts.at[i, 'SHARED_BND'] = ', '.join(shared_bound)

    return precincts


# inputs for precinct file
precincts_gdf = gpd.read_file(input("Enter the file name (.dbf): "))
crs_type = '3857'
crs_str = f'epsg:{crs_type}'
precincts_gdf = precincts_gdf.to_crs(crs_str) 

# determine what columns to use for identifying unique precincts
print(precincts_gdf.head())
col1 = input("Enter the column name for precinct ID: ")
col2 = input("Enter the column name for precincts: ")
col3 = input("Enter the column name for county: ")

# id column for unique precinct identification shorthand
precincts_gdf['id'] = precincts_gdf[col2].astype(str) +  ' (' + precincts_gdf[col3].astype(str) + ')'

precincts_gdf['NEIGHBORS'] = ''
precincts_gdf['SHARED_BND'] = ''

# remove duplicates first
start_time = time.time()
unique_precincts, removed_count = remove_dups(precincts_gdf)
end_time = time.time()
print("Removed ", removed_count, " duplicate precincts in ", end_time - start_time, " seconds")

# find neighbors
start_time = time.time()
updated_precincts = find_neighbors(unique_precincts)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

# export
output_shapefile = input("Enter output file name: ")
updated_precincts.to_file(output_shapefile)
print("Successfully created output file.")
