# Football Prediction Model

## Pull data

Pull historical results of English Premier League games from football-data.co.uk dating back to 2005.

```python
from fetch_data import fetch_epl_data
df = fetch_epl_data()
```

Pull data of La Liga games from football-data.co.uk dating back to 2005.

```python
from fetch_data import fetch_laliga_data
df = fetch_laliga_data()
```

## Simulate match using Poisson distribution

```python
from fetch_data import fetch_laliga_data
from prediction import simulate_match

df = fetch_laliga_data()

home_team = "Real Madrid"
away_team = "Villarreal"

home_team_expected_goals, away_team_expected_goals = simulate_match(home_team, away_team, df)
```

### Glossary

- `HomeTeam` = Home Team
- `AwayTeam` = Away Team
- `FTHG` = Full Time Home Team Goals
- `FTAG` = Full Time Away Team Goals
- `FTR` = Full Time Result (`H`=Home Team Win, `D`=Draw, `A`=Away Team Win)
- `MaxH` = Maximum home win odds
- `MaxD` = Maximum draw odds
- `MaxA` = Maximum away win odds
- `AvgH` = Average home win odds
- `AvgD` = Average draw win odds
- `AvgA` = Average away win odds
