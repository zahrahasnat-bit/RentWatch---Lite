import pytest
# pytest is the testing tool. It runs every function that starts with test_.

from analyzer import AffordabilityAnalyzer, CountyNotFoundError


@pytest.fixture
def analyzer():
    return AffordabilityAnalyzer("rentwatch_all_years.csv")
    # A fixture is shared setup. Each test below receives a fresh analyzer.


def test_burden_formula(analyzer):
    rows = analyzer.burden_for("Essex")
    row = rows[rows["Year"] == 2024].iloc[0]
    expected = round(row["Median Gross Rent"] * 12 / row["Renter Household Income"] * 100, 1)
    # Calculates the formula by hand: rent x 12 / income x 100.
    assert row["Rent Burden (%)"] == expected
    assert row["Rent Burden (%)"] == pytest.approx(38.5, abs=0.1)
    # Also checks against a value we verified: Essex County was 38.5% in 2024.


def test_unknown_county_raises_error(analyzer):
    with pytest.raises(CountyNotFoundError):
        analyzer.burden_for("Atlantis")
        # The test passes only if this line raises our custom error.


def test_ranking_is_highest_first(analyzer):
    ranked = analyzer.rank_counties()
    values = ranked["Rent Burden (%)"].tolist()
    assert len(values) == 14
    assert values == sorted(values, reverse=True)
    # The list must have 14 counties and be sorted from highest to lowest.


def test_growth_gap_and_reliability(analyzer):
    gap = analyzer.growth_gap().set_index("County")
    assert gap.loc["Franklin County", "Growth Gap (pts)"] == pytest.approx(14.5, abs=0.1)
    assert not gap.loc["Dukes County", "Reliable"]
    assert not gap.loc["Nantucket County", "Reliable"]
    # Franklin's gap is the largest verified value, and Dukes and Nantucket are flagged.


def test_projection_returns_a_number(analyzer):
    estimate = analyzer.project_burden("Essex")
    assert isinstance(estimate, float)
    assert 0 < estimate < 100
    # The projection should be a sensible percentage.