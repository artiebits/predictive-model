from datetime import date

import pandas as pd


def is_team_has_historical_data(team, data):
    return (len(data[data.Home == team]) > 0) or (len(data[data.Away == team]) > 0)


def clean_fixture(fixture, data):
    """
    Filter out matches if home or away team doesn't have historical data.
    """
    for index, row in fixture.iterrows():
        if not is_team_has_historical_data(row.Home, data) or not is_team_has_historical_data(row.Away, data):
            fixture.drop(index, inplace=True)
    return fixture


def load_data(path: str) -> pd.DataFrame:
    """Load the historical data"""
    return pd.read_csv(path, parse_dates=["Date"])


def get_matches_for_today(df: pd.DataFrame) -> pd.DataFrame:
    """Get the matches happening today."""
    today = date.today()
    return df[df["Date"].dt.date == today]
