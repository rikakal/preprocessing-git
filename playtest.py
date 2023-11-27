import geopandas as gpd
import pandas as pd

file_input = input("Enter file name: ")
gdf = gpd.read_file(file_input) 

output_shapefile = input("Enter output file name: ")
gdf.to_file(output_shapefile + ".geojson", driver='GeoJSON')
print("Successfully created output file.")

# value_counts = gdf.groupby('COUNTYFIPS').size().reset_index(name='Count')

# # Print the result
# print(value_counts)

# columns_to_sum = gdf.filter(like='TOT_POP21').columns
# total_sum = gdf[columns_to_sum].sum().sum()

# print(total_sum)


# columns_to_sum = gdf.filter(like='G20').columns
# total_sum = gdf[columns_to_sum].sum().sum()
# print(total_sum)

#print(gdf)
