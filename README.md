# RentWatch Lite

A Python command-line tool that shows how heavy a rent burden renters carry in each Massachusetts county, and whether rent has grown faster than renter income from 2014 to 2024.

## Problem
A statewide average hides big differences between counties. A renter, a housing advocate and a city planner each need to see their own county's picture, and which counties are falling behind.

## Who this is for
- **A renter:** checks how their county compares.
- **A housing advocate:** finds counties where rent has outrun renter income.
- **A city planner:** sees where affordability is getting better or worse over time.

## Metrics
- **Rent burden (%):** median monthly gross rent × 12 ÷ median renter household income × 100.
- **Severe rent burden (%):** share of renter households paying 50% or more of income on rent.
- **Growth gap (points):** rent growth minus renter income growth, 2014 to 2024. Positive means rent grew faster.

## Key finding
Between 2014 and 2024, rent grew faster than renter income in Franklin (+14.5 points), Norfolk (+10.9) and Essex (+8.9) counties, while in Suffolk (−19.1) and Hampden (−14.0), renter income grew faster. In 2024, Barnstable County had the highest rent burden (40.9%) and Middlesex the lowest (31.4%).

## Projection
`--county` shows a rough straight-line estimate of the 2029 rent burden. It uses only three data points (2014, 2019, 2024), so treat it as an illustration, not a forecast. For example, Essex County's estimate for 2029 is 39.5%. It is not shown for counties with unreliable data.

## How to run it
Install the libraries: `pip3 install pandas numpy matplotlib pytest`

```bash
python3 rentwatch.py --county essex
python3 rentwatch.py --rank
python3 rentwatch.py --rank --year 2014
python3 rentwatch.py --rank --severe
python3 rentwatch.py --gap
python3 chart.py
python3 chart_over_time.py essex
python3 -m pytest
```

Example: `python3 rentwatch.py --rank`

```
Counties ranked by Rent Burden (%), 2024
               County  Rent Burden (%)
1   Barnstable County             40.9
2        Essex County             38.5
3     Plymouth County             38.2
4      Hampden County             37.1
5      Suffolk County             36.6
6    Nantucket County             36.1
7    Hampshire County             36.0
8     Franklin County             35.9
9      Norfolk County             34.8
10   Berkshire County             33.1
11     Bristol County             32.8
12   Worcester County             32.7
13       Dukes County             32.4
14   Middlesex County             31.4
```

## Data
U.S. Census Bureau, American Community Survey 5-Year Estimates, via data.census.gov: tables B25064 (median gross rent), B25119 (median household income by tenure, renter row) and B25070 (gross rent as a percentage of household income). Years: 2014, 2019 and 2024 (2010–14, 2015–19 and 2020–24 windows). The cleaned dataset is `rentwatch_all_years.csv` (14 counties × 3 years).
Raw downloads are in raw_data/.

## Limits
- ACS values are estimates with margins of error. Dukes and Nantucket have very wide margins, so their changes could be noise. They are flagged "unreliable" and left out of the findings.
- Median rent divided by median income compares typical values. It is not the share of households paying more than 30%.
- Rent and income are each in their own year's dollars, so both growth figures include inflation. The gap between them is still a fair comparison.
- Each 5-year estimate covers a five-year window, which smooths year-to-year changes.
- The projection uses three data points and is a rough estimate only.