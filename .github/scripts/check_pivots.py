"""Re-compute the author's Excel pivot tables with pandas and compare them with the pivot CSVs
that were exported from Excel. A pivot passes when every number in the Excel export is reproduced.

    uv run --no-project --with pandas python .github/scripts/check_pivots.py
"""
import csv
import io
import os
import sys

import pandas as pd

TOL = 1e-6
results = []  # (name, compared, mismatches, examples)


def num(text):
    """'$1,234 ' -> 1234.0, '12%' -> None, '' -> None"""
    t = str(text).replace("$", "").replace(",", "").strip()
    try:
        return float(t)
    except ValueError:
        return None


def rows_of(path):
    with open(path, encoding="utf-8-sig", errors="replace", newline="") as fh:
        return list(csv.reader(fh))


def record(name, expected, actual):
    """expected / actual: dict key -> tuple of numbers"""
    bad = []
    for key, exp in expected.items():
        act = actual.get(key)
        if act is None or any(abs(a - e) > TOL for a, e in zip(act, exp)):
            bad.append(f"{key}: Excel {exp} vs pandas {act}")
    results.append((name, len(expected), len(bad), bad[:3]))


def read_raw(name, encoding="utf-8"):
    try:
        return pd.read_csv(f"data/{name}.csv", encoding=encoding)
    except UnicodeDecodeError:
        return pd.read_csv(f"data/{name}.csv", encoding="latin-1")


# 1. Baseball: wins and losses per team in the season 2000 (filters: Year = 2000)
raw = read_raw("baseball-team-stats")
g = raw[raw["Year"] == 2000].groupby("Team (Full)")[["W", "L"]].sum()
exp = {}
for r in rows_of("04-case-studies/04-baseball-team-stats/baseball-pivot-2000.csv")[7:]:
    if len(r) >= 4 and r[1].strip() and "Total" not in r[0] and num(r[2]) is not None:
        exp[r[1].strip()] = (num(r[2]), num(r[3]))
record("Baseball: wins / losses per team, 2000", exp, {k: (float(v.W), float(v.L)) for k, v in g.iterrows()})

# 2. Shark attacks: number of cases per victim age
raw = read_raw("shark-attack-records", "latin-1")
raw["Age"] = pd.to_numeric(raw["Age"], errors="coerce")
cnt = raw.dropna(subset=["Age"]).groupby("Age")["Case Number"].count()
exp = {}
for r in rows_of("04-case-studies/06-shark-attack-records/shark-pivot-age.csv")[1:]:
    if len(r) >= 2 and num(r[0]) is not None and num(r[1]) is not None:
        exp[num(r[0])] = (num(r[1]),)
record("Shark attacks: cases per age", exp, {float(k): (float(v),) for k, v in cnt.items()})

# 3. Shark attacks: cases per activity, women only (filter: Gender = F)
raw = read_raw("shark-attack-records", "latin-1")
# Excel pivots ignore the case of text ("Boogie boarding" = "Boogie Boarding") but NOT trailing spaces
# ("Body surfing" and "Body surfing " stay two rows); pandas is case-sensitive, so lower-case only
raw["Activity"] = raw["Activity"].astype(str).str.lower()
cnt = raw[raw["Gender"] == "F"].groupby("Activity")["Case Number"].count()
exp = {}
for r in rows_of("04-case-studies/06-shark-attack-records/shark-pivot-activity-female.csv")[3:]:
    if len(r) == 2 and r[0] != "Grand Total" and num(r[1]) is not None:
        exp[r[0].lower()] = (num(r[1]),)
record("Shark attacks: cases per activity, women", exp, {k: (float(v),) for k, v in cnt.items()})

# 4. Stock market: daily Open / High / Low / Close / Volume of AAPL (filter: Symbol = AAPL)
raw = read_raw("stock-market-data")
a = raw[raw["Symbol"] == "AAPL"].groupby("Date")[["Open", "High", "Low", "Close", "Volume"]].sum()
exp = {}
for r in rows_of("04-case-studies/05-stock-market-data/stock-pivot-aapl.csv")[3:]:
    vals = [num(x) for x in r[1:6]]
    if r and r[0] and r[0] != "Grand Total" and len(r) >= 6 and None not in vals:
        exp[r[0]] = tuple(vals)
record("Stocks: AAPL Open/High/Low/Close/Volume per day", exp, {str(k): tuple(float(x) for x in v) for k, v in a.iterrows()})

# 5. US voters: citizen population, registered and confirmed voters per state
raw = read_raw("us-voter-registration")
s = raw.groupby("State")[["Citizen Population", "Registered Voters", "Confirmed Voters"]].sum()
exp = {}
for r in rows_of("04-case-studies/08-us-voter-pivot/voter-pivot-by-state.csv")[1:]:
    vals = [num(x) for x in r[1:4]]
    if r and r[0] and r[0] != "Grand Total" and None not in vals:
        exp[r[0]] = tuple(vals)
record("US voters: three totals per state", exp, {k: tuple(float(x) for x in v) for k, v in s.iterrows()})

# 6. IMDb: gross revenue and budget of the best-earning films
raw = read_raw("imdb-movie-database")
m = raw.groupby("Title")[["Gross Revenue", "Budget"]].sum()
exp = {}
for r in rows_of("02-pivot-tables/imdb-top-grossing-pivot.csv")[1:]:
    vals = [num(x) for x in r[1:3]]
    if r and r[0] and r[0] != "Grand Total" and None not in vals:
        exp[r[0]] = tuple(vals)
record("IMDb: gross revenue and budget per film", exp, {k: tuple(float(x) for x in v) for k, v in m.iterrows()})

width = max(len(n) for n, *_ in results)
failed = 0
lines = ["| Excel pivot | Numbers checked | Mismatches |", "|---|--:|--:|"]
for name, n, bad, ex in results:
    status = "OK " if bad == 0 and n > 0 else "FAIL"
    failed += status == "FAIL"
    print(f"{status} {name:<{width}}  {n:>5} rows compared, {bad} mismatching")
    for e in ex:
        print("      ", e)
    lines.append(f"| {name} | {n} rows | {'✅ 0' if status.strip() == 'OK' else '❌ ' + str(bad)} |")
summary = os.environ.get("GITHUB_STEP_SUMMARY")
if summary:
    with open(summary, "a", encoding="utf-8") as fh:
        fh.write("## Excel pivots re-computed with pandas\n\n" + "\n".join(lines) + "\n")
print(f"\n{len(results) - failed} of {len(results)} pivot tables reproduced exactly")
sys.exit(1 if failed else 0)
