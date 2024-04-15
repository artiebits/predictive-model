library(worldfootballR)
library(lubridate)
library(dplyr)

countries <- c("ENG", "ESP", "GER", "ITA")

for (country in countries) {
  print(paste("Getting data for", country))

  data <- worldfootballR::fb_match_results(country = country, gender = "M", season_end_year = 2010:2025)

  fixture <- data %>%
    filter(Date >= lubridate::today())

  history <- data %>%
    filter(Date < lubridate::today())

  write.csv(fixture, paste0("data/fixtures/", country, ".csv"))
  write.csv(history, paste0("data/match_results/", country, ".csv"))
}

print("All data downloaded")
