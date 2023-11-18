2020 New York precinct and election results shapefile.

## RDH Date retrieval
10/25/2021

## Sources
Election results primarily from individual county canvass reports as processed by OpenElections (https://github.com/openelections/openelections-data-ny/). Results for the following counties in part or in whole directly from county canvass reports: Allegany, Broome, Cattaraugus, Chautauqua, Erie, Monroe, Nassau, Ontario, Putnam.
Cattaraugus, Chenango, Jefferson, Wyoming, and Yates reported some votes at the countywide level. These were distributed by candidate to precincts based on the precinct-level reported vote. Some New York counties only report official write-ins by precinct while placing invalid write-in votes with blank or other void ballots so that write-in figures are not directly comparable at the statewide level.
Precinct shapefiles were obtained from the respective county governments for most counties. The following counties instead use shapefiles from the U.S. Census Bureau's Redistricting Data Program: Chenango, Columbia, Franklin, Genesee, Hamilton, Lewis, Montgomery, Oswego, Otsego, Schenectady, Schuyler, Seneca, St. Lawrence, Wayne, Wyoming. Nearly all of the Census shapefiles were edited to match PDF maps from the respective county boards of elections or the voter file from the New York State Board of Elections.
The Nassau County shapefile includes several dozen unassigned precinct divisions where a distinct ballot style would be required if they had registered voters. The following include registered voters and were merged into adjoining active precincts based on the voter registration file: HE 19049/19065, HE 20012/20093, HE 21087/22108, HE 22066/22702, NH 13016/13701, OB 15093/15703.
The Chemung County shapefile is significantly outdated. Multiple precincts were split, merged, and adjusted in Elmira, Horseheads, and Southport to match PDF maps provided by the county board of elections. The county boundary between Nassau and Suffolk is misaligned in both shapefiles and was edited to match the voter file. Tioga County has a more accurate parcel-based precinct shapefile that was used instead of the shapefile based on BOE descriptions of the precincts.

## Fields metadata

Vote Column Label Format
------------------------
Columns reporting votes follow a standard label pattern. One example is:
G16PREDCli
The first character is G for a general election, P for a primary, C for a caucus, R for a runoff, S for a special.
Characters 2 and 3 are the year of the election.
Characters 4-6 represent the office type (see list below).
Character 7 represents the party of the candidate.
Characters 8-10 are the first three letters of the candidate's last name.

Office Codes
AGR - Agriculture Commissioner
ATG - Attorney General
AUD - Auditor
COC - Corporation Commissioner
COU - City Council Member
DEL - Delegate to the U.S. House
GOV - Governor
H## - U.S. House, where ## is the district number. AL: at large.
INS - Insurance Commissioner
LAB - Labor Commissioner
LAN - Commissioner of Public Lands
LTG - Lieutenant Governor
PRE - President
PSC - Public Service Commissioner
RRC - Railroad Commissioner
SAC - State Appeals Court (in AL: Civil Appeals)
SCC - State Court of Criminal Appeals
SOS - Secretary of State
SSC - State Supreme Court
SPI - Superintendent of Public Instruction
TRE - Treasurer
USS - U.S. Senate

Party Codes
D and R will always represent Democrat and Republican, respectively.
See the state-specific notes for the remaining codes used in a particular file; note that third-party candidates may appear on the ballot under different party labels in different states.

## Fields
G20PREDBID - Joseph R. Biden (Democratic and Working Families fusion)
G20PRERTRU - Donald J. Trump (Republican and Conservative fusion)
G20PRELJOR - Jo Jorgensen (Libertarian Party)
G20PREGHAW - Howie Hawkins (Pacific Green Party)
G20PREIPIE - Brock Pierce (Independence Party)
G20PREOWRI - Write-in Votes

## Processing Steps
Precincts reported on combined line items for the 2020 general election were consolidated in the following counties: Bronx, Cattaraugus, Chautauqua, Kings, New York, Queens, Richmond, Tompkins, Warren.

These additional modifications were made to reflect precinct boundaries as of the 2020 general election:

Chautauqua: Add Ellery 2V; Adjust Jamestown 5-3/6-1
Chenango: Split Oxford 1/2 
Delaware: Merge Tompkins 1/2
Erie: Adjust Tonawanda 63/67
Genesee: Merge Genesee 2-3 into 2-1/2-2/3-1
Lewis: Split Croghan 2/4, Leyden 1/2; Merge Croghan 5/6, Diana 1/2
Otsego: Add Oneonta wards; Split Worcester 1/2; Adjust Laurens 1/2
Schuyler: Split Hector 2/5; Adjust Hector 3/6
Seneca: Split Seneca Falls 5/6
Washington: Consolidate Whitehall from 5 to 3 EDs
Wayne: Align Palmyra districts with county maps