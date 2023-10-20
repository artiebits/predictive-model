import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import poisson


def calculates_weights(dates, xi=0.00186):
    current_date = dates.max()  # use the most recent date as reference
    t = (current_date - dates).dt.days  # get the time difference in days
    return np.exp(-xi * t)  # apply the exponential function


def create_model_data(
    home_team,
    away_team,
    home_goals,
    away_goals,
) -> pd.DataFrame:
    home_df = pd.DataFrame(
        data={
            "team": home_team,
            "opponent": away_team,
            "goals": home_goals,
            "home": 1,
        }
    )
    away_df = pd.DataFrame(
        data={
            "team": away_team,
            "opponent": home_team,
            "goals": away_goals,
            "home": 0,
        }
    )
    return pd.concat([home_df, away_df])


def fit_model(model_data: pd.DataFrame, weights_df=None) -> sm.regression.linear_model.RegressionResultsWrapper:
    if weights_df is None:
        model_weights = weights_df
    else:
        model_weights = pd.concat([weights_df, weights_df])

    return smf.glm(
        formula="goals ~ home + team + opponent",
        data=model_data,
        family=sm.families.Poisson(),
        var_weights=model_weights,
    ).fit()


def predict(h_teams, a_teams, model, max_goals=6) -> pd.DataFrame:
    home_teams = h_teams.tolist()
    away_teams = a_teams.tolist()

    df = pd.DataFrame()

    for i in range(0, len(home_teams)):
        expg1 = model.predict(
            pd.DataFrame(
                data={
                    "team": home_teams[i],
                    "opponent": away_teams[i],
                    "home": 1,
                },
                index=[1],
            )
        ).values[0]
        expg2 = model.predict(
            pd.DataFrame(
                data={
                    "team": away_teams[i],
                    "opponent": home_teams[i],
                    "home": 0,
                },
                index=[1],
            )
        ).values[0]

        team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)] for team_avg in [expg1, expg2]]

        matrix = np.outer(np.array(team_pred[0]), np.array(team_pred[1]))

        home_team_win = np.sum(np.tril(matrix, -1))
        draw = np.sum(np.diag(matrix))
        away_team_win = np.sum(np.triu(matrix, 1))
        btts = np.sum(matrix[1:, 1:])
        btts_no = 1 - btts
        over_2_5 = np.sum(matrix[2:]) + np.sum(matrix[:2, 2:]) - np.sum(matrix[2:3, 0]) - np.sum(matrix[0:1, 2])
        under_2_5 = np.sum(matrix[:2, :2]) + matrix.item((0, 2)) + matrix.item((2, 0))

        temp_df = pd.DataFrame(
            data={
                "home_team": home_teams[i],
                "away_team": away_teams[i],
                "home_team_win": home_team_win,
                "draw": draw,
                "away_team_win": away_team_win,
                "btts": btts,
                "btts_no": btts_no,
                "over": over_2_5,
                "under": under_2_5,
                "expg1": expg1,
                "expg2": expg2,
            },
            index=[1],
        )
        df = pd.concat([df, temp_df])
    return df
