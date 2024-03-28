import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from utils.prediction_functions import (
    create_model_data,
    fit_model,
    calculates_weights,
    predict,
)
from utils.data_preparation_functions import load_data

data = load_data("match_data/GER.csv")

data = data[data["Date"] > "2010-09-01"]

data["advanced_match_stats_path"] = data["MatchURL"].str.split("/").str[-1]

# Iterate over the DataFrame and retrieve Home_Formation and Away_Formation
for index, row in data.iterrows():
    filename = "advanced_match_stats/GER/" + row["advanced_match_stats_path"] + ".csv"
    try:
        formation_df = pd.read_csv(filename)
        home_formation = formation_df["Home_Formation"].iloc[0]
        away_formation = formation_df["Away_Formation"].iloc[0]
        data.at[index, "Home_Formation"] = home_formation
        data.at[index, "Away_Formation"] = away_formation
        data.at[index, "advanced_stat_needed"] = 0
    except FileNotFoundError:
        data.at[index, "advanced_stat_needed"] = 1
        print(f"File {filename} not found.")

data.to_csv("match_data/agg-GER.csv")
