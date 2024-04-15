# install.packages("worldfootballR")
# install.packages("stringi")

library(worldfootballR)
library(lubridate)
library(dplyr)
library(stringi)

# Define a function to remove diacritics from strings
remove_diacritics <- function(input_string) {
  return(stri_trans_general(input_string, "Latin-ASCII"))
}

eng_teams <- list(
  # "Chelsea" = "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
  # "Everton" = "https://fbref.com/en/squads/d3fd31cc/Everton-Stats",
  # "Liverpool" = "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats"
  "Crystal Palace" = "https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats"
)

dir.create("data/teams/", showWarnings = FALSE)

for (team_name in names(eng_teams)) {
  url <- eng_teams[[team_name]]
  team_stats <- fb_team_player_stats(url, stat_type = "standard")

  team_stats$Player <- remove_diacritics(team_stats$Player)

  write.csv(team_stats, file = paste0("data/teams/", team_name, ".csv"), row.names = FALSE)

  print(paste0("Downloaded stats of ", url))
}

print("All data downloaded")
