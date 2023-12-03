import geopandas as gpd
import pandas as pd
import maup

precinct_input = input("Enter the precincts file name: ")
precinct = gpd.read_file(precinct_input)

district_input = input("Enter the districts file name: ")
district = gpd.read_file(district_input)

print("Columns in congressional districts:", district.columns)
district_col = input("Enter the district column name: ")

# Cleaning and sorting district data
district = district.loc[
    district[district_col] != "Congressional Districts not defined"
]
col = 'NAMELSAD20'
if district_col == col:
    district['District_Num'] = district[col].str.extract(r'(\d+)').astype(int)
else:
    district['District_Num'] = district[district_col].astype(int)

# Ensure maup.assign gets the correct district index during assignment
district = district.sort_values(by='District_Num', ascending=True)
district = district.reset_index(drop=True)

crs_type = '3857'
crs_str = f'epsg:{crs_type}'
precinct = precinct.to_crs(crs_str)
district = district.to_crs(crs_str)

district_to_precinct = maup.assign(precinct, district)
precinct['district'] = district_to_precinct
precinct['district'] = pd.to_numeric(precinct["district"])
precinct['district'] = precinct['district'] + 1

crs_type = '4269'
crs_str = f'epsg:{crs_type}'
precinct = precinct.to_crs(crs_str)

output_shapefile = input("Enter output file name: ")
precinct.to_file(output_shapefile)
precinct.to_file(output_shapefile + ".geojson", driver='GeoJSON')
print("Successfully created output files as shapefiles and GeoJSON.")
