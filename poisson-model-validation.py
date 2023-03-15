import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from prediction_functions import (
    create_model_data,
    fit_model,
    calculates_weights,
    predict,
)

data = pd.read_csv("data/epl_2021.csv").assign(Date=lambda df: pd.to_datetime(df.Date))

train_data, test_data = train_test_split(data, random_state=0)

model_data = create_model_data(train_data.HomeTeam, train_data.AwayTeam, train_data.FTHG, train_data.FTAG)

weights = calculates_weights(train_data.Date)
weights = pd.concat([weights, weights])

model = fit_model(model_data)

predictions = predict(test_data.HomeTeam, test_data.AwayTeam, model)

predicted_outcomes = np.where(
    predictions.home_team_win > predictions.away_team_win,
    "H",
    np.where(
        predictions.away_team_win > predictions.home_team_win,
        "A",
        "D",
    ),
)

accuracy = accuracy_score(test_data.FTR, predicted_outcomes)
print("Accuracy:", accuracy)  # 0.5494

# Calculate actual outcomes of BTTS and over 2.5 goals
both_actual_outcomes = np.where(
    (test_data.FTHG > 0) & (test_data.FTAG > 0),
    1,
    0,
)

over_actual_outcomes = np.where(
    (test_data.FTHG + test_data.FTAG > 2),
    1,
    0,
)

threshold = 0.5
predicted_btts = np.where(predictions.btts > threshold, 1, 0)
predicted_over_2_5 = np.where(predictions.over > threshold, 1, 0)

btts_accuracy = accuracy_score(both_actual_outcomes, predicted_btts)
print("BTTS Accuracy:", btts_accuracy)

over_2_5_accuracy = accuracy_score(over_actual_outcomes, predicted_over_2_5)
print("Over 2.5 Accuracy:", over_2_5_accuracy)
