import geopandas as gpd
import pandas as pd

# gdf = gpd.read_file(r"processed\precinct\np_mi\np_mi.dbf")
# print(gdf)
#total_sum = gdf[['G20PRERTRU', 'G20PREDBID', 'G20PRELJOR', 'G20PREGHAW', 'G20PRENDEL', 'G20PRETBLA', 'G20USSRJAM', 'G20USSDPET', 'G20USSGSQU', 'G20USSNDER', 'G20USSTWIL']].sum().sum()
#print("Total Sum:", total_sum)

# pdf = pd.read_csv(r"mi_race_2021_t.csv")
#total_sum = pdf['TOT_POP21'].sum()
#print(pdf)

gdf = gpd.read_file(r"precinct-data.csv")
total_sum = gdf['Total_2020_VAP'].sum()
print(total_sum)


gdf1 = gpd.read_file(r"data\district\2020-district-shapes\tl_2020_us_cd116.dbf")

gdf1 = gdf1[gdf1['STATEFP'] == '36']
gdf1 = gdf1[gdf1['NAMELSAD'] != "Congressional Districts not defined"]
print(gdf1)

# pd.set_option('display.max_colwidth', None)
# print(gdf)

# import json

# # Read GeoJSON file
# file_path = (r'processed\map\2022_agg_mi.geojson')
# with open(file_path, 'r') as file:
#     geojson_data = json.load(file)

# # Specify the column name you want to print
# column_name = 'precincts'

# # Print only the specified column for the first 5 features
# if 'features' in geojson_data:
#     for feature in geojson_data['features'][:1]:
#         if 'properties' in feature and column_name in feature['properties']:
#             column_value = feature['properties'][column_name]
#             print(f"{column_name}: {column_value}")
# else:
#     print("Invalid GeoJSON format. Missing 'features' property.")


# gdf = gpd.read_file(r'processed\map\2020_map_mi\2020_map_mi.shp')
# gdf.to_file('2020_map_mi.geojson', driver='GeoJSON')

# gdf = gpd.read_file(r'processed\map\2020_map_ny\2020_map_ny.shp')
# gdf.to_file('2020_map_ny.geojson', driver='GeoJSON')

# gdf = gpd.read_file(r'processed\map\2020_map_pa\2020_map_pa.shp')
# gdf.to_file('2020_map_pa.geojson', driver='GeoJSON')

# gdf = gpd.read_file(r'processed\map\2022_map_mi\2022_map_mi.shp')
# gdf.to_file('2022_map_mi.geojson', driver='GeoJSON')

# gdf = gpd.read_file(r'processed\map\2022_map_ny\2022_map_ny.shp')
# gdf.to_file('2022_map_ny.geojson', driver='GeoJSON')

# gdf = gpd.read_file(r'processed\map\2022_map_pa\2022_map_pa.shp')
# gdf.to_file('2022_map_pa.geojson', driver='GeoJSON')

# import geopandas as gpd
# import pandas as pd
# from rtree import index
# import matplotlib as plt

# precincts = gpd.read_file(input("Enter precincts file: "))
# districts = gpd.read_file(input("Enter districts file: "))

# districts = districts.to_crs(precincts.crs)

# # create spatial index for districts
# idx = index.Index()
# for i, row in districts.iterrows():
#     idx.insert(i, row.geometry.bounds)

# # find the precincts that match each district
# def find_precincts(district):
#      # check if each precinct is within district bounds
#     matching_precincts = [precinct['id'] for _, precinct in precincts.iterrows() if precinct.geometry.within(district.geometry)]
#     return ', '.join(matching_precincts)  # convert list to comma-separated string

# # create precincts column in districts GDF
# districts['precincts'] = districts.apply(lambda x: find_precincts(x), axis=1)

# pd.set_option('display.max_colwidth', None)

# output_file = (input('Enter the file name for output: '))
# districts.to_file(output_file)

# # Plot precincts and districts
# fig, ax = plt.subplots(figsize=(10, 10))

# # Plot precincts
# precincts.plot(ax=ax, color='lightgrey', edgecolor='black', alpha=0.5, label='Precincts')

# # Plot districts
# districts.plot(ax=ax, color='blue', edgecolor='black', alpha=0.5, label='Districts')

# # Set plot title
# plt.title('Precincts and Districts Map')

# # Set legend
# ax.legend()

# # Show the plot
# plt.show()


