# 📂 Data

Nine raw CSV files, the input of every pivot table in the course. All of them are stored with **Git LFS** (see the [main README](../README.md#how-to-use)); the website shows and downloads the real file.

| File | Rows × columns | Size | Used in | What it is |
|---|:-:|--:|---|---|
| [`baseball-team-stats.csv`](baseball-team-stats.csv) | 624 × 29 | 73 KB | Case study 04 | Baseball team seasons 1995 to 2015: wins, losses, runs, ERA |
| [`daily-weather-conditions.csv`](daily-weather-conditions.csv) | 363 × 7 | 12 KB | Case study 02 | One year of daily temperature, wind and precipitation |
| [`imdb-movie-database.csv`](imdb-movie-database.csv) | 3,728 × 18 | 476 KB | Section 2, 3 | Movies with genre, country, language, budget and gross revenue |
| [`san-diego-burrito-ratings.csv`](san-diego-burrito-ratings.csv) | 237 × 16 | 22 KB | Case study 03 | Burrito reviews scored on tortilla, fillings, temperature and more |
| [`sf-salaries.csv`](sf-salaries.csv) | 24,285 × 7 | 1,694 KB | Case study 07 | San Francisco public employees: base, overtime and other pay |
| [`shark-attack-records.csv`](shark-attack-records.csv) | 5,292 × 14 | 1,051 KB | Case study 06 | Recorded shark attacks with activity, age, gender and fatality |
| [`spartan-race-facebook-posts.csv`](spartan-race-facebook-posts.csv) | 393 × 11 | 86 KB | Case study 01 | Facebook posts with type, hour and engagement counts |
| [`stock-market-data.csv`](stock-market-data.csv) | 29,440 × 7 | 1,283 KB | Case study 05 | Daily prices and volume per stock symbol |
| [`us-voter-registration.csv`](us-voter-registration.csv) | 255 × 6 | 12 KB | Case study 08 | Population, registered and confirmed voters per state and age group |

> Two files are not plain UTF-8: `shark-attack-records.csv` and `spartan-race-facebook-posts.csv` use Windows-1252 (`encoding="latin-1"` in pandas). `sf-salaries.csv` carries four empty trailing columns, which Excel shows as blank columns.

---

*Built by [Evgenii Matveev](https://github.com/evgeniimatveev) · Data Analyst / Analytics & MLOps Engineer*
