import pandas as pd

from utils.data_preparation_functions import get_matches_for_today, load_data
from utils.prediction_functions import (
    fit_model,
    calculates_weights,
    create_model_data,
    predict,
)
from utils.suggest_bets import suggest_bets

countries = ["ENG", "ESP", "GER", "ITA"]

predictions = pd.DataFrame()

for country in countries:
    data = load_data(f"match_data/{country}.csv")

    weights = calculates_weights(data.Date, xi=0.0019)

    model_data = create_model_data(data.Home, data.Away, data.HomeGoals, data.AwayGoals)

    model_data["goals"] = model_data["goals"].astype(int)

    model = fit_model(model_data, weights)

    fixture = load_data(f"match_data/{country}-fixture.csv")
    fixture = get_matches_for_today(fixture)

    prediction = predict(fixture.Home, fixture.Away, model)

    predictions = pd.concat([predictions, prediction], ignore_index=True)

predictions.to_csv("predictions.csv", index=False)

suggest_bets(predictions, bankroll=1000)
