import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy.stats import poisson
from datetime import datetime


def weights_dc(dates, xi=0.0019):
    date_diffs = datetime.now() - dates
    date_diffs = date_diffs.dt.days
    weights = np.exp(-1 * xi * date_diffs)
    return weights


def create_model(home_team, away_team, home_goals, away_goals, weights=None):
    model_data = pd.concat(
        [
            pd.DataFrame(
                data={
                    "team": home_team,
                    "opponent": away_team,
                    "goals": home_goals,
                    "home": 1,
                }
            ),
            pd.DataFrame(
                data={
                    "team": away_team,
                    "opponent": home_team,
                    "goals": away_goals,
                    "home": 0,
                }
            ),
        ]
    )

    if weights is None:
        model_weights = weights
    else:
        model_weights = pd.concat([weights, weights])

    return smf.glm(
        formula="goals ~ home + team + opponent",
        data=model_data,
        family=sm.families.Poisson(),
        var_weights=model_weights,
    ).fit()


def simulate_match(model, home_team, away_team, max_goals=6):
    df = pd.DataFrame()

    home_team = home_team.values
    away_team = away_team.values

    for i in range(0, len(home_team)):
        expg1 = model.predict(
            pd.DataFrame(
                data={"team": home_team[i], "opponent": away_team[i], "home": 1},
                index=[1],
            )
        ).values[0]

        expg2 = model.predict(
            pd.DataFrame(
                data={"team": away_team[i], "opponent": home_team[i], "home": 0},
                index=[1],
            )
        ).values[0]

        team_pred = [
            [poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)]
            for team_avg in [expg1, expg2]
        ]

        matrix = np.outer(np.array(team_pred[0]), np.array(team_pred[1]))

        home_team_win = np.sum(np.tril(matrix, -1))
        draw = np.sum(np.diag(matrix))
        away_team_win = np.sum(np.triu(matrix, 1))
        btts = np.sum(matrix[1:, 1:])
        btts_no = 1 - np.sum(matrix[1:, 1:])
        over_2_5 = (
            np.sum(matrix[2:])
            + np.sum(matrix[:2, 2:])
            - np.sum(matrix[2:3, 0])
            - np.sum(matrix[0:1, 2])
        )
        under_2_5 = np.sum(matrix[:2, :2]) + matrix.item((0, 2)) + matrix.item((2, 0))

        temp_df = pd.DataFrame(
            data={
                "home_team": home_team[i],
                "away_team": away_team[i],
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

        df = pd.concat([df, temp_df], ignore_index=True).round(2)

    return df
