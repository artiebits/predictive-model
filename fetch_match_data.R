library(worldfootballR)
library(lubridate)
library(dplyr)

countries <- c("ENG", "ESP", "GER", "ITA")

for (country in countries) {
  print(paste("Getting data for", country))

  data <- worldfootballR::get_match_results(country = country, gender = "M", season_end_year = 2010:2024)

  fixture <- data %>%
    filter(Date >= lubridate::today())

  history <- data %>%
    filter(Date < lubridate::today())

  write.csv(fixture, paste0("data/", country, "-fixture.csv"))
  write.csv(history, paste0("data/", country, ".csv"))
}

print("All data downloaded")
