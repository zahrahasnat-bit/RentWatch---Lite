import numpy as np
import pandas as pd
# numpy is used for the straight-line projection later.


class CountyNotFoundError(Exception):
    """Our own error type, raised when someone asks for a county that isn't in the data."""
    # Making our own error lets the command line catch it and print a friendly message.


class AffordabilityAnalyzer:
    """Answers questions about rent affordability in Massachusetts counties."""
    # A class bundles the data and the functions that use it into one object.

    def __init__(self, path="rentwatch_all_years.csv"):
        # __init__ runs once when you create the analyzer. "self" means "this analyzer".
        self.data = pd.read_csv(path)
        # Loads the three-year table and keeps it inside the analyzer.

        self.data = self.data[self.data["County"].str.endswith(" County")].copy()
        # Keeps only real counties, so a stray "Massachusetts" row can never get in.

        self.years = [int(y) for y in sorted(self.data["Year"].unique())]
        # The years in the data, in order: [2014, 2019, 2024].
        # int() turns pandas' special number type into a plain Python number.

        self.first_year = self.years[0]
        self.last_year = self.years[-1]
        # The earliest and latest years, used for growth and "latest" rankings.

    def _find_county(self, name):
        """Turn what the user typed into the exact county name in the data."""
        # The underscore at the start means "internal helper, not meant to be called directly".
        text = str(name).strip().title()
        # strip() removes spaces; title() capitalizes: " essex " -> "Essex".

        if not text.endswith("County"):
            text += " County"
        # Lets the user type "Essex" instead of "Essex County".

        if text not in set(self.data["County"]):
            valid = ", ".join(sorted(self.data["County"].unique()))
            raise CountyNotFoundError(f"'{name}' was not found. Valid counties: {valid}")
            # raise stops the function and sends our error back to whoever called it.
        return text

    def burden_for(self, county):
        """Burden numbers for one county, one row per year."""
        county = self._find_county(county)
        rows = self.data[self.data["County"] == county]
        # Keeps only this county's rows.
        return rows[["Year", "Median Gross Rent", "Renter Household Income",
                     "Rent Burden (%)", "Severe Rent Burden (%)"]].sort_values("Year")

    def rank_counties(self, year=None, by="Rent Burden (%)"):
        """Rank all counties from most to least burdened in one year."""
        year = self.last_year if year is None else year
        # If no year is given, use the latest one.
        rows = self.data[self.data["Year"] == year]
        ranked = rows.sort_values(by, ascending=False)[["County", by]].reset_index(drop=True)
        # Sorts from highest to lowest and keeps just the county and the measure.
        ranked.index = ranked.index + 1
        # Makes the row numbers start at 1 instead of 0, so they read as ranks.
        return ranked

    def growth_gap(self):
        """Rent growth minus income growth between the first and last year, with a reliability flag."""
        first = self.data[self.data["Year"] == self.first_year].set_index("County")
        last = self.data[self.data["Year"] == self.last_year].set_index("County")
        # One table per year, each labelled by County so counties line up with themselves.

        result = pd.DataFrame({
            "Rent Growth (%)": (last["Median Gross Rent"] / first["Median Gross Rent"] - 1) * 100,
            "Income Growth (%)": (last["Renter Household Income"] / first["Renter Household Income"] - 1) * 100,
        })
        result["Growth Gap (pts)"] = result["Rent Growth (%)"] - result["Income Growth (%)"]
        # Positive: rent grew faster than income. Negative: income grew faster.

        rent_margin = (first["Rent MOE"] ** 2 + last["Rent MOE"] ** 2) ** 0.5
        income_margin = (first["Income MOE"] ** 2 + last["Income MOE"] ** 2) ** 0.5
        # Combined margin of error for a change between two estimates.

        rent_real = (last["Median Gross Rent"] - first["Median Gross Rent"]).abs() > rent_margin
        income_real = (last["Renter Household Income"] - first["Renter Household Income"]).abs() > income_margin
        result["Reliable"] = rent_real & income_real
        # True only if BOTH changes are bigger than their margins of error.

        return result.round(1).sort_values("Growth Gap (pts)", ascending=False).reset_index()

    def project_burden(self, county, by="Rent Burden (%)"):
        """Rough straight-line estimate of the next period's value for one county."""
        county = self._find_county(county)
        rows = self.data[self.data["County"] == county].sort_values("Year")

        slope, intercept = np.polyfit(rows["Year"], rows[by], 1)
        # polyfit fits the best straight line through the points. The 1 means "a straight line".
        # The line is: value = slope * year + intercept.

        next_year = self.last_year + 5
        # The ACS 5-year windows are 5 years apart (2014, 2019, 2024), so the next one is 2029.

        return round(float(slope * next_year + intercept), 1)
        # Plug the next year into the line to get the estimate.

        self.data = pd.read_csv(path)
        # Loads the three-year table and keeps it inside the analyzer.
        self.data = self.data[self.data["County"].str.endswith(" County")].copy()