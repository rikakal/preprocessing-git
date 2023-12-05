import geopandas as gpd
import pandas as pd
import maup

precinct_input = input('Enter the precincts file name: ')
precinct = gpd.read_file(precinct_input)

district_input = input('Enter the districts file name: ')
district = gpd.read_file(district_input)

col = 'NAMELSAD20'
district = district.loc[district[col] != 'Congressional Districts not defined']
district['District_Num'] = district[col].str.extract(r'(\d+)').astype(int)
district = district.sort_values(by='District_Num', ascending=True)
district = district.reset_index(drop=True)

crs_type = '3857'
crs_str = f'epsg:{crs_type}'
precinct = precinct.to_crs(crs_str)
district = district.to_crs(crs_str)

district_to_precinct = maup.assign(precinct, district)
precinct['district'] = district_to_precinct
precinct['district'] = pd.to_numeric(precinct['district'])
precinct['district'] = precinct['district'] + 1

crs_type = '4269'
crs_str = f'epsg:{crs_type}'
precinct = precinct.to_crs(crs_str)

output_shapefile = input('Enter output file name: ')
precinct.to_file(output_shapefile)
precinct.to_file(output_shapefile + '.geojson', driver='GeoJSON')
print('Successfully created output files as shapefiles and GeoJSON.')
