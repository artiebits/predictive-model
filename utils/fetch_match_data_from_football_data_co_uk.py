import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_data(competition_name: str, competition_page: str) -> pd.DataFrame:
    base_url = "https://www.football-data.co.uk/"
    res = requests.get(f"{base_url}{competition_page}")
    soup = BeautifulSoup(res.content, "lxml")

    # Find the table containing links to the match_data
    table = soup.find_all("table", attrs={"align": "center", "cellspacing": "0", "width": "800"})[1]
    body = table.find_all("td", attrs={"valign": "top"})[1]

    # Extract links and link texts from the table
    links = [link.get("href") for link in body.find_all("a")]
    links_text = [link_text.text for link_text in body.find_all("a")]

    # Filter the links for the given competition name and exclude unwanted match_data
    data_urls = [f"{base_url}{links[i]}" for i, text in enumerate(links_text) if text == competition_name][:-12]

    # Fetch match_data from the urls and concatenate them into a single DataFrame
    dfs = []
    for url in data_urls:
        season = url.split("/")[4]
        print(f"Getting fbref_data for {competition_name} season {season}")
        temp_df = pd.read_csv(url)
        temp_df["Season"] = season
        temp_df = (
            temp_df.dropna(axis="columns", thresh=temp_df.shape[0] - 30)
            .assign(
                Day=lambda df: df.Date.str.split("/").str[0],
                Month=lambda df: df.Date.str.split("/").str[1],
                Year=lambda df: df.Date.str.split("/").str[2],
            )
            .assign(Date=lambda df: df.Month + "/" + df.Day + "/" + df.Year)
            .assign(Date=lambda df: pd.to_datetime(df.Date))
            .dropna()
        )
        dfs.append(temp_df)

    df = pd.concat(dfs)

    return df.dropna(axis=1).dropna().sort_values(by="Date")


def fetch_laliga_data():
    return fetch_data("La Liga Primera Division", "spainm.php")


def fetch_serie_a_data():
    return fetch_data("Serie A", "italym.php")


def fetch_epl_data():
    return fetch_data("Premier League", "englandm.php")


def fetch_bundesliga_data():
    return fetch_data("Bundesliga 1", "germanym.php")


# epl_data = fetch_epl_data()
# epl_data.to_csv("fdcuk_data/ENG.csv")
#
# laliga_data = fetch_laliga_data()
# laliga_data.to_csv("fdcuk_data/ESP.csv")

bundesliga_data = fetch_bundesliga_data()
bundesliga_data.to_csv("../fdcuk_data.csv")

# serie_a_data = fetch_serie_a_data()
# serie_a_data.to_csv("fdcuk_data/ITA.csv")