library(worldfootballR)
library(lubridate)
library(dplyr)

countries <- c("ENG", "ESP", "GER", "ITA", "FRA")

for (country in countries) {
  print(paste("Getting data for", country))

  data <- get_match_results(country = country, gender = "M", season_end_year = 2010:2022)

  fixture <- data %>%
    filter(Date >= lubridate::today()) %>%
    select(Date, Time, Home, Away)

  history <- data %>%
    filter(Date < lubridate::today()) %>%
    select(Date, Home, Away, HomeGoals, AwayGoals)

  write.csv(fixture, paste0("data/", country, "-fixture.csv"))
  write.csv(history, paste0("data/", country, ".csv"))
}

print("All data downloaded")
