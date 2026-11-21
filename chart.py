import matplotlib.pyplot as plt
# matplotlib is Python's drawing library. plt is the usual nickname.

from analyzer import AffordabilityAnalyzer

a = AffordabilityAnalyzer()
# Loads the data.

ranked = a.rank_counties().sort_values("Rent Burden (%)")
# The latest-year ranking, re-sorted lowest to highest.
# Horizontal bar charts draw the first row at the bottom, so the highest ends up on top.

gap = a.growth_gap()
unreliable = set(gap.loc[~gap["Reliable"], "County"])
# Counties flagged unreliable (Dukes and Nantucket), so we can color them differently.

labels = [name.replace(" County", "") for name in ranked["County"]]
# Shorter labels: "Essex County" -> "Essex".

colors = ["lightgray" if name in unreliable else "steelblue" for name in ranked["County"]]
# Gray bars for unreliable counties, blue for the rest.

fig, ax = plt.subplots(figsize=(8, 6))
# Creates the picture (fig) and the drawing area (ax). figsize is width x height in inches.

ax.barh(labels, ranked["Rent Burden (%)"], color=colors)
# One horizontal bar per county.

for position, value in enumerate(ranked["Rent Burden (%)"]):
    ax.text(value + 0.3, position, f"{value:.1f}", va="center")
    # Writes each bar's value just to the right of the bar.

ax.set_xlabel("Typical annual rent as % of typical renter household income")
ax.set_title(f"Rent burden by Massachusetts county, {a.last_year}")

fig.text(0.01, 0.01, "Gray = very wide margin of error, interpret with caution. "
         "Source: U.S. Census ACS 5-Year Estimates.", fontsize=8, color="gray")
# A small footnote at the bottom.

plt.tight_layout(rect=[0, 0.03, 1, 1])
# Adjusts spacing so nothing is cut off.

plt.savefig("burden_by_county.png", dpi=150)
print("Saved burden_by_county.png")