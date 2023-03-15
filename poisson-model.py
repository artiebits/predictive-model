import pandas as pd

from data_preparation_functions import get_today_matches
from prediction_functions import (
    fit_model,
    calculates_weights,
    create_model_data,
    predict,
)
from suggest_bets import suggest_bets

countries = ["ENG", "ESP", "GER", "ITA", "FRA"]

predictions = pd.DataFrame()

for country in countries:
    data = pd.read_csv(f"data/{country}.csv").assign(Date=lambda df: pd.to_datetime(df.Date))

    weights = calculates_weights(data.Date, xi=0.0019)

    model_data = create_model_data(data.HomeTeam, data.AwayTeam, data.FTHG, data.FTAG)

    model = fit_model(model_data, weights)

    fixture = get_today_matches(data)

    prediction = predict(fixture.HomeTeam, fixture.AwayTeam, model)

    predictions = pd.concat([predictions, prediction], ignore_index=True)

predictions.to_csv("predictions.csv", index=False)

suggest_bets(predictions, bankroll=1000)
