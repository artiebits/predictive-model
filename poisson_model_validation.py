import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from utils.data_preparation_functions import load_data
from utils.prediction_functions import (
    create_model_data,
    fit_model,
    calculates_weights,
    predict,
)

data = load_data("match_data/GER.csv")


train_data, test_data = train_test_split(data, random_state=0)


model_data = create_model_data(
    train_data.Home, train_data.Away, train_data.HomeGoals, train_data.AwayGoals
)

weights = calculates_weights(train_data.Date, xi=0.001)

model = fit_model(model_data, weights)

predictions = predict(test_data.Home, test_data.Away, model)

# Calculate actual outcomes of BTTS and over 2.5 goals
btts_actual_outcomes = np.where(
    (test_data.HomeGoals > 0) & (test_data.AwayGoals > 0),
    1,
    0,
)

over_actual_outcomes = np.where(
    (test_data.HomeGoals + test_data.AwayGoals > 2),
    1,
    0,
)

threshold = 0.5
predicted_btts = np.where(predictions.btts > threshold, 1, 0)
predicted_over_2_5 = np.where(predictions.over > threshold, 1, 0)

btts_accuracy = accuracy_score(btts_actual_outcomes, predicted_btts)
print("BTTS Accuracy:", btts_accuracy)

over_2_5_accuracy = accuracy_score(over_actual_outcomes, predicted_over_2_5)
print("Over 2.5 Accuracy:", over_2_5_accuracy)
