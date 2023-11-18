import geopandas as gpd
import pandas as pd

# https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html
# https://davesredistricting.org/

# 2020 has district shapes from US Census data file, 2022 has individual state district shapes
year = input("Enter district year (2020/2022): ")
if year == '2020':
    gdf1 = gpd.read_file(input("Enter US Census data file name: "))
    
    # state id
    state_info = { 
        'NY': '36',
        'MI': '26',
        'PA': '42'
    }
    state = input("Enter state in question (NY/MI/PA): ")
    if state in state_info:
        stateID = state_info[state]
    else:
        print(f"Invalid state abbreviation.")
        exit()

    # grab the correct rows according to STATEFP
    gdf1 = gdf1[gdf1['STATEFP'] == stateID]
    gdf1 = gdf1[gdf1['NAMELSAD'] != "Congressional Districts not defined"]
    gdf1['District_Num'] = gdf1['NAMELSAD'].str.extract(r'(\d+)').astype(int)

    # sort and reset index
    sorted_gdf1 = gdf1.sort_values(by='District_Num', ascending=True)
    gdf1 = gdf1.reset_index(drop=True)


elif year == '2022':
    gdf1 = gpd.read_file(input("Enter district shape file: "))

else:
    print(f"Invalid year.")
    exit()


file2 = input("Enter district details file name: ")
gdf2 = gpd.read_file(file2)

numeric_columns = ['ID', 'Total Pop', 'Dem', 'Rep', 'Oth', 'White', 'Minority', 'Hispanic', 'Black', 'Asian', 'Native', 'Pacific']

# format data from string to float
for column in numeric_columns:
    gdf2[column] = pd.to_numeric(gdf2[column], errors='coerce').fillna(0).astype(float)

gdf2 = gdf2[gdf2['Total Pop'] != 0]
gdf2 = gdf2[gdf2['ID'] != 0]
gdf2 = gdf2.drop('Total VAP', axis=1)
gdf2 = gdf2.reset_index(drop=True)
gdf2 = gdf2.rename(columns={'ID': 'District'})
gdf2['District'] = gdf2.index + 1

# load district boundaries from US Census DF/District Shape to the District Details DF
gdf2 = gdf2.set_geometry(gdf1.geometry)

crs_type = '3857'
crs_str = f'epsg:{crs_type}'
gdf2 = gdf2.to_crs(crs_str)

output_file_name = input("Enter the output file name (without extension): ")
gdf2.to_file(output_file_name, driver="ESRI Shapefile")
print("Created output shapefile:", output_file_name)
