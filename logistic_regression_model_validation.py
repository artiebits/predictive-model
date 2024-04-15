import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder

from utils.data_preparation_functions import load_data

data = load_data("data/match_results/ITA.csv")
data = data[data["Date"] > "2018-08-01"]

# Add home/away indicator
features = ["Home", "Away", "Home_xG", "Away_xG", "Referee", "Venue"]

X = data[features]
y = np.where((data["HomeGoals"] + data["AwayGoals"] > 2), 1, 0)

club_names_encoder = LabelEncoder()
referee_encoder = LabelEncoder()
venue_encoder = LabelEncoder()
home_xg_imputer = SimpleImputer()
away_xg_imputer = SimpleImputer()

X["Home"] = club_names_encoder.fit_transform(X["Home"])
X["Away"] = club_names_encoder.transform(X["Away"])
X["Home_xG"] = home_xg_imputer.fit_transform(X[["Home_xG"]])
X["Away_xG"] = away_xg_imputer.fit_transform(X[["Away_xG"]])
X["Referee"] = referee_encoder.fit_transform(X["Referee"])
X["Venue"] = venue_encoder.fit_transform(X["Venue"])

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

model = LogisticRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

scores = cross_val_score(model, X, y, cv=5)
print("Cross-validation scores:", scores)
print("Average cross-validation score:", scores.mean())

accuracy_btts = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy_btts)
