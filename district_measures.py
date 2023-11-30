import geopandas as gpd
import pandas as pd

gdf = gpd.read_file(input("Enter the district details file name: "))

# Select columns that we need
numeric_columns = [
    'ID',
    'Total Pop',
    'Dem',
    'Rep',
    'Oth',
    'White',
    'Minority',
    'Hispanic',
    'Black',
    'Asian',
    'Native',
    'Pacific'
]

# Clean up data
for c in numeric_columns:
    gdf[c] = pd.to_numeric(gdf[c], errors='coerce').fillna(0).astype(float)
gdf = gdf[gdf['Total Pop'] != 0]
gdf = gdf[gdf['ID'] != 0]
gdf = gdf.drop('Total VAP', axis=1)
gdf = gdf.reset_index(drop=True)
gdf = gdf.rename(columns={'ID': 'District'})
gdf['District'] = gdf.index + 1

total_pop = gdf['Total Pop'].sum()

totals = {
    'Democratic Voters': 0,
    'Republican Voters': 0,
    'Other Voters': 0,
    'White': 0,
    'Minority': 0,
    'Hispanic': 0,
    'Black': 0,
    'Asian': 0,
    'Native': 0,
    'Pacific': 0
}

for i, row in gdf.iterrows():
    pop = row['Total Pop']

    totals['Democratic Voters'] += row['Dem'] * pop  
    totals['Republican Voters'] += row['Rep'] * pop
    totals['Other Voters'] += row['Oth'] * pop
    totals['White'] += row['White'] * pop
    totals['Minority'] += row['Minority'] * pop
    totals['Hispanic'] += row['Hispanic'] * pop
    totals['Black'] += row['Black'] * pop
    totals['Asian'] += row['Asian'] * pop
    totals['Native'] += row['Native'] * pop
    totals['Pacific'] += row['Pacific'] * pop

# Convert back to percentage once we have all totals
p_democratic_voters = round(totals['Democratic Voters'] / total_pop * 100, 2)
p_republican_voters = round(totals['Republican Voters'] / total_pop * 100, 2)
p_other_voters = round(totals['Other Voters'] / total_pop * 100, 2)
p_white = round(totals['White'] / total_pop * 100, 2)
p_minority = round(totals['Minority'] / total_pop * 100, 2)
p_hispanic = round(totals['Hispanic'] / total_pop * 100, 2)
p_black = round(totals['Black'] / total_pop * 100, 2)
p_asian = round(totals['Asian'] / total_pop * 100, 2)
p_native = round(totals['Native'] / total_pop * 100, 2)
p_pacific = round(totals['Pacific'] / total_pop * 100, 2)

total_pop = (int)(total_pop)

statewide_measures = pd.DataFrame({
    "Total Population": [total_pop],
    "Total Democratic Voters %": [p_democratic_voters],
    "Total Republican Voters %": [p_republican_voters],
    "Total Other Voters %": [p_other_voters],
    "% White": [p_white],
    "% Minority": [p_minority],
    "% Hispanic": [p_hispanic],
    "% Black": [p_black],
    "% Asian": [p_asian],
    "% Native American": [p_native],
    "% Pacific": [p_pacific]
})

print(statewide_measures)

output_file_name = input("Enter the output file name: ") + ".csv"
statewide_measures.to_csv(output_file_name, index=False)
print("Created output CSV file:", output_file_name)
