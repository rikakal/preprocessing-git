- pip install geopandas
- pip install matplotlib
- pip install tqdm
- pip install rtree
- pip install maup
- pip install networkx

district_fix.py -> adding district geometry (GeoJSON boundaries) to district data details
- [USE CASE 1] geo_data_agg.py -> integrating district, precinct, and US Census data
- [USE CASE 2] neighbors.py -> computing precinct neighbors 
- [USE CASE 6] district_measures.py -> computing district details
- [USE CASE 7] adjacency.py -> computing adjacency graph: node = precincts, adjacency = nested list for each node consecutively

Resources:
- https://dataverse.harvard.edu/dataverse/electionscience (Precinct)
- https://redistrictingdatahub.org (Precinct)
- https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html (District Geometry)
- https://davesredistricting.org/ (District Measures)
- https://www2.census.gov/geo/tiger/TIGER2022/STATE/ (State boundaries)

Note: Use Case 2 Column dictionary for race/vap, which are block groups
- https://www2.census.gov/programs-surveys/decennial/2020/technical-documentation/complete-tech-docs/summary-file/2020Census_PL94_171Redistricting_StatesTechDoc_English.pdf

To process data, start with neighbors.py and store output in processed/precinct_map
- Precinct and Block Group data in data/precinct

To map districts onto precincts, run district_map.py and store output in processed/district_map
- Distict data in data/district
- Use the precinct file already processed in processed/precinct_map

To find adjacencies, run adjacency.py and store output in processed/adjacency
- Use the file already processed in processed/district_map
