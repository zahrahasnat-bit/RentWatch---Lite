import sys
# sys lets us read what the user typed after the file name.

import matplotlib.pyplot as plt
from analyzer import AffordabilityAnalyzer, CountyNotFoundError

a = AffordabilityAnalyzer()

county_input = sys.argv[1] if len(sys.argv) > 1 else "Essex"
# sys.argv[1] is the first word typed after the file name. If none, use Essex.

try:
    name = a._find_county(county_input)
    # Turns "essex" into "Essex County", or raises CountyNotFoundError.
except CountyNotFoundError as error:
    print(f"Error: {error}")
    sys.exit(1)
    # Prints the friendly message and stops.

rows = a.burden_for(name)
# This county's rows: one per year.

fig, ax = plt.subplots(figsize=(7, 5))

for column, label in [("Rent Burden (%)", "Rent burden (rent vs renter income)"),
                      ("Severe Rent Burden (%)", "Severe burden (share paying 50%+)")]:
    ax.plot(rows["Year"], rows[column], marker="o", label=label)
    # One line per measure. marker="o" puts a dot at each year.
    for year, value in zip(rows["Year"], rows[column]):
        ax.annotate(f"{value:.1f}", (year, value), textcoords="offset points",
                    xytext=(0, 8), ha="center")
        # Writes each point's value just above it.

ax.set_xticks(list(rows["Year"]))
# Tick marks only at the years we have: 2014, 2019, 2024.

ax.set_ylabel("Percent")
ax.set_title(f"{name}: rent burden over time")
ax.legend()
fig.text(0.01, 0.01, "Source: U.S. Census ACS 5-Year Estimates (2010-14, 2015-19, 2020-24).",
         fontsize=8, color="gray")
plt.tight_layout(rect=[0, 0.03, 1, 1])

filename = f"{name.replace(' ', '_').lower()}_over_time.png"
# Example: essex_county_over_time.png

plt.savefig(filename, dpi=150)
print("Saved", filename)