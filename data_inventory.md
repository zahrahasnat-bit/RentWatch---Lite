# RentWatch Lite — Data Inventory

**Source:** U.S. Census Bureau, ACS 5-Year Estimates (data.census.gov). Massachusetts counties (14). Years: 2014, 2019, 2024.

| Table | Measures | Used |
|---|---|---|
| B25064 | Median gross rent | Estimate and margin of error |
| B25119 | Median household income by tenure | "Renter occupied" row, estimate and margin of error |
| B25070 | Gross rent as % of household income | Total renters and "50.0 percent or more" row, to compute severe burden % |

**Raw files:** `raw_data/` (nine Census CSVs, one per table per year).
**Cleaned dataset:** `rentwatch_all_years.csv`, 14 counties × 3 years, columns: County, Year, Median Gross Rent, Rent MOE, Renter Household Income, Income MOE, Severe Rent Burden (%), Rent Burden (%).

**Cleaning steps**
- Reshaped each file from one column per county to one row per county.
- Picked the "Renter occupied" income row and the "50.0 percent or more" burden row by label.
- Removed commas and ± signs and converted text to numbers.
- Excluded the statewide "Massachusetts" column so only the 14 counties remain.
- Verified every year's income file names its own dollar year, and checked 14 rows per year with no missing values.

**Note:** an earlier version mixed 2014 income into the 2024 data. It was found by comparing against each year's raw file and fixed.