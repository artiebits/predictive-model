library(worldfootballR)
library(lubridate)
library(dplyr)

countries <- c("ENG", "ESP", "GER", "ITA", "FRA")

for (country in countries) {
  print(paste("Getting data for", country))
  fb_match_results(country = country, gender = "M", season_end_year = 2010:2023) %>%
    write.csv(., paste0("data/", country, ".csv"))
}

print("All data downloaded")