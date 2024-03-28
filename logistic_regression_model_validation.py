import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

from utils.data_preparation_functions import load_data

data = load_data("match_data/agg-GER.csv")
data = data[data["Date"] > "2021-01-01"]

features = [
    "Home",
    "Away",
    "Home_xG",
    "Away_xG",
    # "Home_Formation",
    # "Away_Formation",
    "Referee",
]
X = data[features]

# y = np.where((data["HomeGoals"] > 0) & (data["AwayGoals"] > 0), 1, 0)
y = np.where((data["HomeGoals"] + data["AwayGoals"] > 2), 1, 0)

club_names_encoder = LabelEncoder()
referee_encoder = LabelEncoder()
venue_encoder = LabelEncoder()
home_xg_imputer = SimpleImputer()
away_xg_imputer = SimpleImputer()
formation_encoder = LabelEncoder()

X["Home_xG"] = home_xg_imputer.fit_transform(X[["Home_xG"]])
X["Away_xG"] = away_xg_imputer.fit_transform(X[["Away_xG"]])
X["Home"] = club_names_encoder.fit_transform(X["Home"])
X["Away"] = club_names_encoder.transform(X["Away"])
X["Referee"] = referee_encoder.fit_transform(X["Referee"])

# X["Home_Formation"] = formation_encoder.fit_transform(X["Home_Formation"])
# X["Away_Formation"] = formation_encoder.fit_transform(X["Away_Formation"])

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

model = LogisticRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

scores = cross_val_score(model, X, y, cv=5)
print("Cross-validation scores:", scores)
print("Average cross-validation score:", scores.mean())

accuracy_btts = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy_btts)
