from fetch_data import fetch_epl_data
from prediction import create_poisson_model, simulate_match

df = fetch_epl_data()

poisson_model = create_poisson_model(df)

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

    home_team_win_odds, draw_odds, away_team_win_odds = simulate_match(
        poisson_model, home_team, away_team
    )

    print(
        f"{home_team} {'%.2f' % home_team_win_odds}, X {'%.2f' % draw_odds}, {away_team} {'%.2f' % away_team_win_odds}"
    )
