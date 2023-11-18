import geopandas as gpd
import matplotlib.pyplot as plt
from rtree import index

# precinct file
precinct_input = input("Enter the precincts file name: ")
precincts = gpd.read_file(precinct_input)

# district shapefile
districts_input = input("Enter the districts file name: ")
districts = gpd.read_file(districts_input)
print("Columns in congressional districts:", districts.columns)

# get district column name
district_column_name = input("Enter the district column name: ")

# remove any leading zeros from the district column
districts[district_column_name] = districts[district_column_name].astype(str).str.lstrip('0')
districts = districts.to_crs(precincts.crs)

# create spatial index for districts
idx = index.Index()
for i, row in districts.iterrows():
    idx.insert(i, row.geometry.bounds)

# find the district with the largest intersection area for each precinct
def find_majority_district(precinct):
    candidates = [districts.iloc[i] for i in idx.intersection(precinct.geometry.bounds)]
    intersections = [precinct.geometry.intersection(candidate.geometry) for candidate in candidates]
    largest_intersection = max(intersections, key=lambda x: x.area)
    return candidates[intersections.index(largest_intersection)][district_column_name]

# create district column in precincts GDF
precincts['district'] = precincts.apply(find_majority_district, axis=1)


# display the columns in the precincts GDF and allow the user to choose which columns to keep
print("\nColumns in precincts file:")
for i, col in enumerate(precincts.columns):
    print(f"{i}: {col}")
column_indices = input("Enter the column numbers to keep (separated by space): ")
column_indices = [int(idx) for idx in column_indices.split()]

# extract selected columns from the precincts GeoDataFrame
selected_columns = [precincts.columns[idx] for idx in column_indices]

# display the chosen column names for confirmation
print("\nChosen columns:")
for col in selected_columns:
    print(col)

confirmation = input("Do you confirm the selected columns? (y/n): ")

if confirmation.lower() == "y":
    precincts = precincts[selected_columns]

    # Export
    output_file = input('Enter the file name for output: ')
    precincts.to_file(output_file)
else:
    print("Selection not confirmed. Exiting without saving.")


# plot the precincts and districts
fig, ax = plt.subplots(figsize=(12, 12))
districts.boundary.plot(ax=ax, color='blue', linewidth=1)
precincts.boundary.plot(ax=ax, color='red', linewidth=0.5)

# display district numbers
for idx, row in districts.iterrows():
    plt.annotate(text=row[district_column_name], xy=row.geometry.centroid.coords[0], horizontalalignment='center', fontsize=9)

plt.show()
