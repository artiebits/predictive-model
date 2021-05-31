import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf


def simulate_match(poisson_model, home_team, away_team, max_goals=10):
    home_goals_avg = poisson_model.predict(
        pd.DataFrame(
            data={"team": home_team, "opponent": away_team, "home": 1}, index=[1]
        )
    ).values[0]
    away_goals_avg = poisson_model.predict(
        pd.DataFrame(
            data={"team": away_team, "opponent": home_team, "home": 0}, index=[1]
        )
    ).values[0]
    team_pred = [
        [stats.poisson.pmf(i, team_avg) for i in range(0, max_goals)]
        for team_avg in [home_goals_avg, away_goals_avg]
    ]

    match_prediction = np.outer(np.array(team_pred[0]), np.array(team_pred[1]))

    odds_home_team_win = np.sum(np.tril(match_prediction, -1))
    odds_away_team_win = np.sum(np.triu(match_prediction, 1))
    odds_draw = np.sum(np.diag(match_prediction))

    return odds_home_team_win, odds_draw, odds_away_team_win


def create_poisson_model(df):
    """
    Treat the number of goals scored by each team as two independent Poisson distributions.
    The shape of each distribution is determined by the average number of goals scored by that team.
    """

    df = df[["HomeTeam", "AwayTeam", "FTHG", "FTAG"]]
    df = df.rename(columns={"FTHG": "HomeGoals", "FTAG": "AwayGoals"})

    goal_model_data = pd.concat(
        [
            df[["HomeTeam", "AwayTeam", "HomeGoals"]]
            .assign(home=1)
            .rename(
                columns={
                    "HomeTeam": "team",
                    "AwayTeam": "opponent",
                    "HomeGoals": "goals",
                }
            ),
            df[["AwayTeam", "HomeTeam", "AwayGoals"]]
            .assign(home=0)
            .rename(
                columns={
                    "AwayTeam": "team",
                    "HomeTeam": "opponent",
                    "AwayGoals": "goals",
                }
            ),
        ]
    )

    poisson_model = smf.glm(
        formula="goals ~ home + team + opponent",
        data=goal_model_data,
        family=sm.families.Poisson(),
    ).fit()

    return poisson_model
