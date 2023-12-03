import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon, MultiPolygon
from tqdm import tqdm
import time
import maup

# ESPG 3857, which uses meters as its unit of measurement
# 200 ft = 60.96 meters
def are_neighbors(precinct1, precinct2, distance=60.96):
    b1 = precinct1.buffer(distance)
    b2 = precinct2.buffer(distance)

    shared_bnd_buffer = b1.intersection(b2)

    if isinstance(shared_bnd_buffer, (Polygon, MultiPolygon)):
        if shared_bnd_buffer.length >= distance:
            return True
    return False

# def find_boundary(precinct1, precinct2):
#     len = precinct1.intersection(precinct2).length
#     return round(len, 8) # round to 8 decimals

# Function to find neigbors of each precinct
def find_neighbors(p, distance=60.96):
    spatial_i = p.sindex

    # p.shape[0] gives # rows, p.shape[1] gives # columns
    for i, row in tqdm(p.iterrows(), total=p.shape[0], desc="Neighbors"):
        geo = row['geometry']

        nearby_p_indices = list(spatial_i.intersection(geo.bounds))
        nearby_p = p.iloc[nearby_p_indices]

        neighbor_list = []

        # nearby_row[0] is index, nearby_row[1] is the panda Series
        for nearby_row in nearby_p.iterrows(): 
            if nearby_row[1]['id'] == row['id']: # skip self comparison
                continue
            perim = are_neighbors(geo, nearby_row[1]['geometry'], distance)
            if perim:
                neighbor_list.append(nearby_row[0])

        p.at[i, 'NEIGHBORS'] = ', '.join(map(str, neighbor_list))

    crs_type = '4269'
    crs_str = f'epsg:{crs_type}'
    p = p.to_crs(crs_str) 

    # for i, row in tqdm(p.iterrows(), total=p.shape[0], desc="Boundaries"):
    #     geo = row['geometry']
    #     if row['NEIGHBORS']:
    #         n_edit = list(map(float, row['NEIGHBORS'].split(',')))
    #         n_list = list(map(int, n_edit))
    #         shared_bound = []
    #         for neighbor_index in n_list:
    #             neighbor_row = p.iloc[neighbor_index]
    #             bound = find_boundary(geo, neighbor_row['geometry'])
    #             shared_bound.append(bound)

    #     p.at[i, 'SHARED_BND'] = ', '.join(map(str, shared_bound))

    return p

file_precinct = input("Enter Precinct file name: ")
file_block_group = input("Enter Block Group file name: ")

print("Reading files...")
start_time = time.time()
precinct = gpd.read_file(file_precinct)
block_group_file = gpd.read_file(file_block_group)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

crs_type = '3857'
crs_str = f'epsg:{crs_type}'
block_group_file = block_group_file.to_crs(crs_str)
precinct = precinct.to_crs(crs_str) 

print("Assigning blocks to precincts...")
start_time = time.time()
columns = [col for col in block_group_file.columns 
            if col.startswith('P002') or col.startswith('P004') or
            col =='geometry']
block_group = block_group_file[columns].copy()
block_to_precinct = maup.assign(block_group, precinct)
columns = [col for col in block_group.columns if 
           col.startswith('P002') or col.startswith('P004')]
summed_columns = block_group[columns].groupby(block_to_precinct).sum()
concat_df = pd.concat([precinct, summed_columns], axis=1)
precinct_concat = gpd.GeoDataFrame(concat_df, geometry='geometry')
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

precinct_concat['id'] = range(0, len(precinct_concat))
print("Finding neighbors for each precinct...")
precinct_concat['NEIGHBORS'] = ''
#precinct_concat['SHARED_BND'] = ''
start_time = time.time()
precincts_gdf = find_neighbors(precinct_concat)
precincts_gdf = precincts_gdf.fillna(0)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

print("Renaming columns...")
start_time = time.time()
columns_mapping = {
    'P0020001': 'TOTAL_POP', 
    'P0020002': 'HISP_POP', 
    'P0020005': 'WHITE_POP', 
    'P0020006': 'BLACK_POP',
    'P0020008': 'ASIAN_POP',
    'P0020011': '2MORE_POP',
    'P0040001': 'TOTAL_VAP', 
    'P0040002': 'HISP_VAP', 
    'P0040005': 'WHITE_VAP', 
    'P0040006': 'BLACK_VAP',
    'P0040008': 'ASIAN_VAP',
    'P0040011': '2MORE_VAP',
    'G20PREDBID': 'Democrat',
    'G20PRERTRU': 'Republican'
}
precincts_gdf.rename(columns=columns_mapping, inplace=True)
# sd = precincts_gdf.columns[precincts_gdf.columns.str.contains('G20USSD')][0]
# sr = precincts_gdf.columns[precincts_gdf.columns.str.contains('G20USSR')][0]
# precincts_gdf = precincts_gdf.rename(columns={sd:'S_Democrat'})
# precincts_gdf = precincts_gdf.rename(columns={sr:'S_Republic'})
columns_drop = [col for col in precincts_gdf.columns 
                if col.startswith('P002') or col.startswith('P004')
                or col.startswith('G20') or col == 'STATEFP' 
                or col == 'elexpre' or 'cou' in col.lower()]
precincts_gdf.drop(columns=columns_drop, inplace=True)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds")

print("Removing island precincts...")
start_time = time.time()
precincts_gdf.dropna(subset=['NEIGHBORS'], inplace=True)
precincts_gdf['id'] = range(0, len(precincts_gdf))
precincts_gdf['NEIGHBORS'] = precincts_gdf['NEIGHBORS'].astype(str).apply(
        lambda x: x.replace('.0', '') if x else x
    )
print(precincts_gdf)
end_time = time.time()
print("Completed in ", end_time - start_time, " seconds\n")

output_shapefile = input("Enter output file name: ")
precincts_gdf.to_file(output_shapefile)
print("Successfully created output file.")
