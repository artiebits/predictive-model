import pandas as pd
from datetime import datetime


def clean_fixture(fixture, data):
    """
    Filter out matches if home or away team doesn't have historical data.
    """

    def is_team_has_historical_data(team):
        return (len(data[data.Home == team]) > 0) or (len(data[data.Away == team]) > 0)

    for index, row in fixture.iterrows():
        if (
            not is_team_has_historical_data(
                row.Home,
            )
            or not is_team_has_historical_data(row.Away)
        ):
            fixture.drop(index, inplace=True)
    return fixture


def get_fixture_for_today(country_code):
    fixture = pd.read_csv(f"data/{country_code}-fixture.csv").assign(
        Date=lambda df: pd.to_datetime(df.Date)
    )
    today = datetime.now().date()
    return fixture[fixture.Date.dt.date == today]
