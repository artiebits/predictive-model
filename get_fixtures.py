import requests
import json
import os
import unicodedata
import pandas as pd
from datetime import datetime


# Format the date as YYYYMMDD
today = datetime.today().strftime("%Y%m%d")

players_map = {"Djordje Petrovic": "Dorde Petrovic"}


def get_lineups(livescore_id):
    if livescore_id is None:
        raise ValueError("livescore_id is required")

    url = "https://livescore6.p.rapidapi.com/matches/v2/get-lineups"

    querystring = {"Category": "soccer", "Eid": livescore_id}

    headers = {
        "X-RapidAPI-Key": "7cfc571638msh1a5b5a2073472bap16f926jsndad8e3d19dff",
        "X-RapidAPI-Host": "livescore6.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    lineups = {"Team": [], "Player": []}

    for lineup in data.get("Lu", []):
        team = lineup.get("Tnb")
        players = lineup.get("Ps", [])

        for player in players:

            if "Fn" not in player:
                player_name = player["Ln"]
            elif "Fn" in player and "Ln" in player:
                player_name = f"{player['Fn']} {player['Ln']}"
            player_name = (
                unicodedata.normalize("NFKD", player_name)
                .encode("ascii", "ignore")
                .decode("utf-8")
            )

            # Check if the player name exists in the mapping, if so, replace it
            if player_name in players_map:
                player_name = players_map[player_name]

            if player["Pon"] != "COACH" and player["Pon"] != "SUBSTITUTE_PLAYER":
                lineups["Team"].append(team)
                lineups["Player"].append(player_name)

    df = pd.DataFrame(lineups)
    df.to_csv(f"data/lineups/{livescore_id}.csv")


def collect_events(json_file, league, country):
    with open(json_file, "r") as f:
        data = json.load(f)
        events = []
        for stage in data["Stages"]:
            if stage["Snm"] == league and stage["Cnm"] == country:
                events.extend(stage["Events"])
        return events


# Define input JSON file path
json_file = f"data/fixtures/{today}.json"

# Collect events for Premier League, LaLiga, and Serie A
premier_league_events = collect_events(json_file, "Premier League", "England")
# laliga_events = collect_events(json_file, "LaLiga", "Spain")
# seriea_events = collect_events(json_file, "Serie A", "Italy")


df = pd.DataFrame(premier_league_events)

fixture = df.apply(
    lambda x: pd.Series(
        {"Home": x["T1"][0]["Nm"], "Away": x["T2"][0]["Nm"], "LivescoreID": x["Eid"]}
    ),
    axis=1,
)


# Iterate over each row in df_selected
for index, row in fixture.iterrows():
    livescore_id = row["LivescoreID"]

    file_path = f"data/lineups/{livescore_id}.csv"

    if not os.path.isfile(file_path):
        print(f"No lineup file found for {livescore_id}. Fetching lineup data...")
        get_lineups(livescore_id)
    else:
        lineups_df = pd.read_csv(file_path)

        home_team = row["Home"]
        away_team = row["Away"]

        lineups_df["Team"].replace({1: home_team, 2: away_team}, inplace=True)

        home_team_df = pd.read_csv(f"data/teams/{home_team}.csv")
        away_team_df = pd.read_csv(f"data/teams/{away_team}.csv")

        # Merge lineups_df with home_team_df on the "Player" column to get xG_Expected for home_team
        lineups_df = pd.merge(
            lineups_df,
            home_team_df[["Player", "npxG_Per_Minutes"]],
            on="Player",
            how="left",
        )

        # Merge lineups_df with away_team_df on the "Player" column to get xG_Expected for away_team
        lineups_df = pd.merge(
            lineups_df,
            away_team_df[["Player", "npxG_Per_Minutes"]],
            on="Player",
            how="left",
        )

        print(lineups_df)

        team1_xG = lineups_df["npxG_Per_Minutes_x"].sum()
        team2_xG = lineups_df["npxG_Per_Minutes_y"].sum()

        # Creating a new DataFrame with just two rows - one for each team
        final_df = pd.DataFrame(
            {
                "Team": [home_team, away_team],
                "xG": [team1_xG, team2_xG],
            }
        )

        final_df.to_csv(f"data/fixtures/{today}.csv")
