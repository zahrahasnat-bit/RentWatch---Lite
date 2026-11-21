from analyzer import AffordabilityAnalyzer, CountyNotFoundError

a = AffordabilityAnalyzer("rentwatch_all_years.csv")
# Creates the analyzer and loads the data.

print(a.burden_for("essex"))
# Lowercase and no "County" on purpose, to test the name matching.

print(a.rank_counties())
# Latest-year ranking by rent burden.

print(a.rank_counties(by="Severe Rent Burden (%)"))
# Same, but by severe burden.

print(a.growth_gap())
# Should match the table you pasted, including the Reliable column.

print(a.project_burden("Franklin"))
# A single number: the rough estimate for 2029.

try:
    a.burden_for("Atlantis")
except CountyNotFoundError as error:
    print("Caught:", error)
    # Should print a friendly message listing the valid counties instead of crashing.