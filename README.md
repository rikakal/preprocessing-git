pip install geopandas
pip install matplotlib
pip install tqdm
pip install rtree
pip install maup

district_fix.py -> adding district geometry (GeoJSON boundaries) to district data details
[USE CASE 1] geo_data_agg.py -> integrating district, precinct, and US Census data
[USE CASE 2] neighbors.py -> computing precinct neighbors 
[USE CASE 6] district_measures.py -> computing district details

Resources:
# https://dataverse.harvard.edu/dataverse/electionscience (Precinct)
# https://redistrictingdatahub.org (Precinct)
# https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html (District Geometry)
# https://davesredistricting.org/ (District Measures)
