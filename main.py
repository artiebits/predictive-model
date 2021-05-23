from prediction import simulate_match
from fetch_data import fetch_epl_data

if __name__ == "__main__":
    df = fetch_epl_data()

    upcoming_matches = [
        ["Arsenal", "Brighton"],
        ["Aston Villa", "Chelsea"],
        ["Fulham", "Newcastle"],
        ["Leeds", "West Brom"],
        ["Leicester", "Tottenham"],
        ["Liverpool", "Crystal Palace"],
        ["Man City", "Everton"],
        ["Sheffield United", "Burnley"],
        ["West Ham", "Southampton"],
        ["Wolves", "Man United"],
    ]

    for match in upcoming_matches:
        home_team = match[0]
        away_team = match[1]

        home_team_expected_goals, away_team_expected_goals = simulate_match(
            home_team, away_team, df
        )

        print(
            f"{home_team} vs {away_team} {home_team_expected_goals}-{away_team_expected_goals}"
        )
