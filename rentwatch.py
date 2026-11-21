import argparse
# argparse is Python's built-in tool for reading options typed after the program name,
# like --county or --rank.

from analyzer import AffordabilityAnalyzer, CountyNotFoundError
# Brings in the analyzer class and our custom error from analyzer.py.


def main():
    parser = argparse.ArgumentParser(
        description="RentWatch Lite: rent affordability for Massachusetts counties."
    )
    # Creates the argument reader. The description appears when someone types --help.

    parser.add_argument("--county", help="Show burden numbers for one county, e.g. --county Essex")
    # Lets the user type --county followed by a name. Stored as args.county.

    parser.add_argument("--rank", action="store_true", help="Rank all counties by rent burden")
    # action="store_true" makes this a simple on/off switch with no value: --rank.

    parser.add_argument("--severe", action="store_true", help="With --rank, rank by severe burden instead")
    # Optional switch that changes what --rank sorts by.

    parser.add_argument("--year", type=int, help="With --rank, the year to rank: 2014, 2019 or 2024 (default: latest)")
    # Lets the user pick which year to rank. type=int turns what they type into a number.

    parser.add_argument("--gap", action="store_true", help="Show rent growth vs renter income growth, 2014 to 2024")
    # Switch for the growth gap table.

    args = parser.parse_args()
    # Reads what the user typed and stores each option on "args".

    if not (args.county or args.rank or args.gap):
        parser.print_help()
        return
        # If the user typed no options, show the help text and stop.

    analyzer = AffordabilityAnalyzer()
    # Loads the data once.

    gap = analyzer.growth_gap()
    unreliable = set(gap.loc[~gap["Reliable"], "County"])
    # The set of counties flagged unreliable (Dukes and Nantucket).
    # ~ means "not", so this keeps rows where Reliable is False.

    try:
        # try/except: if our code raises CountyNotFoundError, we print a friendly
        # message instead of letting the program crash.

        if args.county:
            name = analyzer._find_county(args.county)
            # Converts what the user typed ("essex") to the exact name ("Essex County").
            # It raises CountyNotFoundError if the county doesn't exist.

            print(f"\n{name}")
            print(analyzer.burden_for(name).to_string(index=False))
            # Prints the county's rows, one per year. index=False hides the row numbers.

            if name in unreliable:
                print("\nNote: this county has very wide margins of error, so these numbers are unreliable.")
                print("No projection shown.")
                # We don't project for unreliable counties.
            else:
                estimate = analyzer.project_burden(name)
                next_year = analyzer.last_year + 5
                print(f"\nRough estimate of rent burden in {next_year}: {estimate}%")
                print("(Straight-line estimate from only 3 data points. Treat it as an estimate.)")

        if args.rank:
            year = args.year if args.year else analyzer.last_year
            # Uses the year the user typed, or the latest year if they didn't type one.

            if year not in analyzer.years:
                print(f"\nError: year must be one of {analyzer.years}")
                return
                # Stops with a friendly message if the year isn't in the data.

            column = "Severe Rent Burden (%)" if args.severe else "Rent Burden (%)"
            # Picks which measure to rank by, depending on whether --severe was given.

            print(f"\nCounties ranked by {column}, {year}")
            print(analyzer.rank_counties(year=year, by=column).to_string())
            # Keeps the numbers on the left, because they are the ranks 1 to 14.

        if args.gap:
            print(f"\nRent growth vs renter income growth, {analyzer.first_year} to {analyzer.last_year}")
            print("Growth Gap = rent growth minus income growth (positive: rent grew faster)")
            print(gap.to_string(index=False))
            if unreliable:
                print("\nReliable = False means the change is within the margin of error: "
                      + ", ".join(sorted(unreliable)))

    except CountyNotFoundError as error:
        print(f"\nError: {error}")
        # Our friendly message, listing the valid counties.


if __name__ == "__main__":
    main()
    # Only runs main() when you run this file directly.