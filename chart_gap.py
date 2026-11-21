import matplotlib.pyplot as plt
# matplotlib is Python's drawing library. plt is the usual nickname.

from analyzer import AffordabilityAnalyzer

a = AffordabilityAnalyzer()
# Loads the data.

gap = a.growth_gap().sort_values("Growth Gap (pts)")
# The growth gap table, sorted from most negative to most positive.
# Horizontal bar charts draw the first row at the bottom, so the biggest positive ends up on top.

labels = [name.replace(" County", "") for name in gap["County"]]
# Shorter labels: "Essex County" -> "Essex".

colors = []
for _, row in gap.iterrows():
    # Loops over each county's row so we can pick a color for its bar.
    if not row["Reliable"]:
        colors.append("lightgray")
        # Gray: very wide margin of error, so the change could be noise.
    elif row["Growth Gap (pts)"] > 0:
        colors.append("indianred")
        # Red: rent grew faster than renter income.
    else:
        colors.append("steelblue")
        # Blue: renter income grew faster than rent.

fig, ax = plt.subplots(figsize=(8, 6))
# Creates the picture (fig) and the drawing area (ax).

colors = ["lightgray" if (abs(g) < 1.0 and c != "lightgray") else c
          for g, c in zip(gap["Growth Gap (pts)"], colors)]
# Any county whose gap is under 1 point (and not already gray) also turns gray,
# since a gap that small isn't a real direction. Optional.

ax.barh(labels, gap["Growth Gap (pts)"], color=colors)
# One horizontal bar per county.

ax.axvline(0, color="black", linewidth=0.8)
# A vertical line at zero: bars to the right mean rent outgrew income.

for position, value in enumerate(gap["Growth Gap (pts)"]):
    offset = 0.4 if value >= 0 else -0.4
    ax.text(value + offset, position, f"{value:+.1f}", va="center",
            ha="left" if value >= 0 else "right")
    # Writes each bar's value, with a + or - sign, just past the end of the bar.

ax.set_xlim(-25, 20)
# Gives the labels room on both sides.

ax.set_xlabel("Rent growth minus renter income growth, 2014 to 2024 (percentage points)")
ax.set_title("Where rent outgrew renter income in Massachusetts")

fig.text(0.01, 0.01,
         "Red: rent grew faster. Blue: income grew faster. Gray: very wide margin of error. "
         "Source: U.S. Census ACS 5-Year Estimates.",
         fontsize=8, color="gray")
# A small footnote explaining the colors.

plt.tight_layout(rect=[0, 0.03, 1, 1])
# Adjusts spacing so nothing is cut off.

plt.savefig("growth_gap_by_county.png", dpi=150)
print("Saved growth_gap_by_county.png")