import pandas as pd
from datetime import datetime


def get_fixture_for_today(country_code):
    fixture = pd.read_csv(f"data/{country_code}-fixture.csv").assign(
        Date=lambda df: pd.to_datetime(df.Date)
    )
    today = datetime.now().date()
    return fixture[fixture.Date.dt.date == today]
