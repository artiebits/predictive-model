from numpy.random import poisson
from scipy import stats


# Simulate match using Poisson distribution
def simulate_match(home_team, away_team, df):
    subset = df[(df.HomeTeam == home_team) & (df.AwayTeam == away_team)]

    if subset.shape[0] > 4:
        home_team_scored_avg = subset.FTHG.mean()
        away_team_scored_avg = subset.FTAG.mean()

        # Simulate each team's goal by sample from a Poisson distribution
        # stats.mode Returns an array of the modal (most common) value in the array.
        home_team_goals = int(stats.mode(poisson(home_team_scored_avg, 100_000))[0])
        away_team_goals = int(stats.mode(poisson(away_team_scored_avg, 100_000))[0])

        return [home_team_goals, away_team_goals]
    else:
        home_team_scored_avg = df[df.HomeTeam == home_team].FTHG.mean()
        home_team_conceded_avg = df[df.HomeTeam == home_team].FTAG.mean()

        away_team_scored_avg = df[df.AwayTeam == away_team].FTAG.mean()
        away_team_conceded_avg = df[df.AwayTeam == away_team].FTHG.mean()

        home_team_goals = int(
            stats.mode(
                poisson(
                    1 / 2 * (home_team_scored_avg + away_team_conceded_avg), 100_000
                )
            )[0]
        )

        away_team_goals = int(
            stats.mode(
                poisson(
                    1 / 2 * (away_team_scored_avg + home_team_conceded_avg), 100_000
                )
            )[0]
        )

        return home_team_goals, away_team_goals
