import pandas as pd

from data_preparation_functions import get_fixture_for_today
from prediction_functions import create_model, weights_dc, simulate_match
from suggest_bets import suggest_bets

countries = ["ENG", "ESP", "GER", "ITA", "FRA"]

predictions = pd.DataFrame()

for country in countries:
    data = pd.read_csv(f"data/{country}.csv").assign(
        Date=lambda df: pd.to_datetime(df.Date)
    )

    my_weights = weights_dc(data.Date, xi=0.0019)

    model = create_model(
        data.Home, data.Away, data.HomeGoals, data.AwayGoals, my_weights
    )

    fixture = get_fixture_for_today(data)

    prediction = simulate_match(model, fixture)

    predictions = pd.concat([predictions, prediction], ignore_index=True)

predictions.to_csv("predictions.csv", index=False)

suggest_bets(predictions, bankroll=1000)
