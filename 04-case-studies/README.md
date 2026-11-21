# 🧪 Section 4: Case Studies

Eight real datasets, one question each. Every folder holds the **pivot tables exported from Excel**: PDFs of the finished pivots and, for some, the pivot as a CSV. The raw data sits in [`data/`](../data/).

| # | Case study | Raw data (rows × columns) | What the pivot answers | Exported pivots | CI |
|:-:|------------|---------------------------|------------------------|-----------------|----|
| 01 | **Spartan Race Facebook Posts** | [`spartan-race-facebook-posts.csv`](../data/spartan-race-facebook-posts.csv) (393 × 11) | Which hour of the day gets the most posts, and which post type earns the most shares, reactions, likes and comments? | [`pivot-11.pdf`](01-spartan-race-facebook-posts/pivot-11.pdf) (1 p), [`pivot-12.pdf`](01-spartan-race-facebook-posts/pivot-12.pdf) (1 p) | PDF only |
| 02 | **Daily Weather Conditions** | [`daily-weather-conditions.csv`](../data/daily-weather-conditions.csv) (363 × 7) | Average maximum temperature per day, and max / min temperature and wind speed per date. | [`pivot-08.pdf`](02-daily-weather-conditions/pivot-08.pdf) (11 p), [`pivot-10.pdf`](02-daily-weather-conditions/pivot-10.pdf) (11 p) | PDF only |
| 03 | **San Diego Burrito Ratings** | [`san-diego-burrito-ratings.csv`](../data/san-diego-burrito-ratings.csv) (237 × 16) | Average tortilla, filling, temperature and synergy scores per burrito type. | [`pivot-07.pdf`](03-san-diego-burrito-ratings/pivot-07.pdf) (3 p) | PDF only |
| 04 | **Baseball Team Stats** | [`baseball-team-stats.csv`](../data/baseball-team-stats.csv) (624 × 29) | Wins and losses per year, and per division and team for a chosen season. | [`pivot-06.pdf`](04-baseball-team-stats/pivot-06.pdf) (1 p), [`baseball-pivot-2000.csv`](04-baseball-team-stats/baseball-pivot-2000.csv) | ✅ re-computed |
| 05 | **Stock Market Data** | [`stock-market-data.csv`](../data/stock-market-data.csv) (29,440 × 7) | Daily open, high, low, close and volume per symbol (AAPL, AMZN), with percent change. | [`pivot-04.pdf`](05-stock-market-data/pivot-04.pdf) (2 p), [`pivot-05.pdf`](05-stock-market-data/pivot-05.pdf) (2 p), [`stock-pivot-aapl.csv`](05-stock-market-data/stock-pivot-aapl.csv) | ✅ re-computed |
| 06 | **Shark Attack Records** | [`shark-attack-records.csv`](../data/shark-attack-records.csv) (5,292 × 14) | Cases per activity and per victim age, with the share of the total. | [`pivot-03.pdf`](06-shark-attack-records/pivot-03.pdf) (1 p), [`shark-pivot-activity-female.csv`](06-shark-attack-records/shark-pivot-activity-female.csv), [`shark-pivot-age.csv`](06-shark-attack-records/shark-pivot-age.csv) | ✅ re-computed |
| 07 | **SF Salaries** | [`sf-salaries.csv`](../data/sf-salaries.csv) (24,285 × 7) | Average base pay and total overtime and other pay per job title and per employee. | [`pivot-01.pdf`](07-sf-salaries/pivot-01.pdf) (34 p), [`pivot-02.pdf`](07-sf-salaries/pivot-02.pdf) (100 p) | PDF only |
| 08 | **U.S. Voter Pivot** | [`us-voter-registration.csv`](../data/us-voter-registration.csv) (255 × 6) | Citizen population, registered and confirmed voters per state and age group. | [`pivot-us.pdf`](08-us-voter-pivot/pivot-us.pdf) (10 p), [`voter-pivot-by-state.csv`](08-us-voter-pivot/voter-pivot-by-state.csv) | ✅ re-computed |

> "✅ re-computed" means the manual CI run rebuilds that pivot with pandas from the raw CSV and compares every number with the Excel export (see the [main README](../README.md#continuous-integration)). The other cases have only PDFs, which cannot be compared automatically.

---

[← Pivot Charts](../03-pivot-charts/) &nbsp;·&nbsp; [Course map →](../README.md)

*Built by [Evgenii Matveev](https://github.com/evgeniimatveev) · Data Analyst / Analytics & MLOps Engineer*
