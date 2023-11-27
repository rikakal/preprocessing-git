import geopandas as gpd
import pandas as pd
import maup
import networkx as nx
import json
import matplotlib.pyplot as plt

# precinct file
precinct_input = input("Enter the precincts file name: ")
precincts = gpd.read_file(precinct_input)

# district shapefile
districts_input = input("Enter the districts file name: ")
districts = gpd.read_file(districts_input)

print("Columns in congressional districts:", districts.columns)
district_col_name = input("Enter the district column name: ")

# Cleaning and sorting District data
districts = districts[districts[district_col_name] != "Congressional Districts not defined"]
if district_col_name == 'NAMELSAD20':
    districts['District_Num'] = districts['NAMELSAD20'].str.extract(r'(\d+)').astype(int)
else:
    districts['District_Num'] = districts[district_col_name].astype(int)

districts = districts.sort_values(by='District_Num', ascending=True)
districts = districts.reset_index(drop=True)
districts = districts.to_crs(precincts.crs)
print(districts)

district_to_precinct = maup.assign(precincts, districts) # Assign districts to precincts
precincts['district'] = district_to_precinct
precincts['district'] = pd.to_numeric(precincts["district"])
precincts['district'] = precincts['district'] + 1 # need to do this because the assignment takes the index

print(precincts)

crs_type = '4269'
crs_str = f'epsg:{crs_type}'
precincts = precincts.to_crs(crs_str)

output_shapefile = input("Enter output file name: ")
precincts.to_file(output_shapefile)
print("Successfully created output file.")

output_shapefile = input("Enter output file name: ")
precincts.to_file(output_shapefile + ".geojson", driver='GeoJSON')
print("Successfully created output file.")

