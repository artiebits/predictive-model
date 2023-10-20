library(worldfootballR)
library(lubridate)
library(dplyr)

test_df <- read.csv("fbref_data/GER.csv")

# Create a directory to store the individual result files
dir.create("advanced_match_stats/GER", showWarnings = FALSE)

# Iterate through each record in the dataset
for (i in 50:nrow(test_df)) {
  match_url <- test_df$MatchURL[i]

  # Call fb_advanced_match_stats
  advanced_match_stats <- fb_advanced_match_stats(match_url = match_url, stat_type = "summary", team_or_player = "player")

  # Extract the desired part of the matchURL for the filename
  filename <- sub(".*/", "", match_url)

  # Generate a unique filename for this result
  filename <- paste0("advanced_match_stats/GER/", filename, ".csv")

  # Save the result in a CSV file with the unique filename
  write.csv(advanced_match_stats, file = filename, row.names = FALSE)

  print(paste0(filename, " downloaded ", i))
#   "advanced_match_stats/GER/Nurnberg-Werder-Bremen-March-19-2011-Bundesliga.csv downloaded 482"
}

print("All data downloaded")
