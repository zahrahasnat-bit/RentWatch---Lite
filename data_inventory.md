# RentWatch Lite — Data Inventory

## Project Overview

This document tracks the Census datasets used in RentWatch Lite, including what was extracted, how it was cleaned, and the resulting output files.

**Data year:** 2024 (ACS 5-Year Estimates, 2020–2024) [confirm on data.census.gov]  
**Geographic level:** Massachusetts counties  
**Number of counties:** 14  
**Data source:** U.S. Census Bureau, American Community Survey (ACS) 5-Year Estimates, via data.census.gov  
**Date downloaded:** [date]

---

## 1. Dataset Inventory

### B25064 — Median Gross Rent

**Purpose:** Measures the median gross rent (rent plus utilities) paid by renter households.

**Original structure:** 1 row × 28 columns (one estimate column and one margin-of-error column per county).

**Information extracted:**
- County name
- Median gross rent estimate
- Margin of error (MOE)

**Cleaning performed:**
- Identified the 14 county estimate columns and their matching MOE columns.
- Reshaped from one wide row into one row per county.
- Shortened column names to the county name (e.g. "Barnstable County").
- Removed commas and "±" signs and converted values to numbers.

**Output file:** `cleaned_median_gross_rent_2024.csv`  
**Final structure:** 14 rows × 3 columns (County, Median Gross Rent, Rent MOE)

### B25119 — Median Household Income by Tenure

**Purpose:** Measures median household income by housing tenure; only the renter-occupied row is used.

**Original structure:** 28 rows × 2 columns after extraction (14 estimates followed by 14 MOEs, no county labels).

**Information extracted:**
- County name
- Renter-occupied median household income estimate
- Margin of error (MOE)

**Cleaning performed:**
- Identified the renter-occupied median household income row.
- Extracted 14 county estimates and 14 county margins of error.
- Combined estimates and MOEs and attached county names in Census alphabetical order.
- Verified spot values against the Census source (e.g. Barnstable 33,329; Dukes 46,544).
- Verified every MOE was smaller than its estimate.
- Renamed columns and standardized county names to match the other tables.

**Output file:** `cleaned_renter_household_income_2024.csv`  
**Final structure:** 14 rows × 3 columns (County, Renter Household Income, Income MOE)

### B25070 — Gross Rent as a Percentage of Household Income

**Purpose:** Measures the share of renter households paying 50% or more of their income on gross rent.

**Information extracted:**
- Total renter-occupied households (denominator)
- Households spending 50.0% or more of income on gross rent (numerator)
- County-level estimates and margins of error for both

**Calculation performed:**

Severe Rent Burden (%) = (households spending 50% or more on gross rent ÷ total renter-occupied households) × 100

**Cleaning and processing performed:**
- Identified the total renter-occupied households row and the 50.0 percent or more row.
- Extracted county estimates and margins of error.
- Removed commas and converted values to numbers with `pd.to_numeric()`.
- Calculated the severe rent burden percentage for all 14 counties.

**Output file:** `cleaned_severe_rent_burden_2024.csv`  
**Final structure:** 14 rows × 2 columns (County, Severe Rent Burden (%))

**Note:** the cleaned file holds only the calculated percentage. The underlying Census estimates and MOEs are kept in the notebook/raw files if needed later. No MOE is currently calculated for the percentage.

---

## 2. Combined Dataset

**Output file:** `rentwatch_2024_combined.csv`  
**Structure:** 14 rows × 6 columns (County, Median Gross Rent, Rent MOE, Renter Household Income, Income MOE, Severe Rent Burden (%))

**Merge method:** inner join on County, standardized to the "[Name] County" format.

**Validation performed:**
- County names match across all three tables.
- Exactly 14 rows, no duplicate counties.
- No missing values in any column.
- Every margin of error is smaller than its estimate.
- Value ranges reviewed and judged reasonable.

---

## 3. Data Cleaning Summary

| Dataset | Original shape | Final shape | Processing |
|---|---|---|---|
| B25064 | 1 × 28 | 14 × 3 | Reshaped columns into rows, converted text to numbers |
| B25119 | 28 × 2 | 14 × 3 | Split estimates from MOEs, added county names, renamed columns |
| B25070 | multiple rows × 28 | 14 × 2 | Extracted two rows, calculated percentage |

---

## 4. Known Limitations

- ACS values are estimates with margins of error. Small counties have very wide margins, so differences involving them should be read cautiously: [county] has the widest rent MOE (±628) and [county] the widest income MOE (±21,488).
- Dividing median rent by median renter income compares typical values; it is not the share of households paying over 30%.
- Each 5-year estimate covers a five-year window, not a single year, so year-to-year changes are smoothed.

---

## 5. Current Project Status

- [x] Identify the three Census datasets
- [x] Inspect dataset rows and columns
- [x] Identify the required Census rows
- [x] Extract county-level estimates and margins of error
- [x] Calculate severe rent burden percentages
- [x] Restructure rent and income to one row per county
- [x] Standardize county names across all three tables
- [x] Merge the three datasets and validate (14 rows, no missing values)
- [ ] Save the three cleaned CSV files and the combined file
- [ ] Commit and push to GitHub

---

## 6. Next Steps

1. Clean the remaining years of data with the same process and stack them into one table with a `Year` column.
2. Compute the renter-income burden metric and the rent-vs-income growth gap.
3. Build the `AffordabilityAnalyzer` class and command-line interface.