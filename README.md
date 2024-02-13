# FRED Series Fetcher

This Python script fetches series data from the Federal Reserve Economic Data (FRED) API and saves it to a CSV file. It uses the `fredapi` Python library to interact with the FRED API.

## Functions

```python
init_fred(api_key: str) -> fa.Fred
```

This function initializes the FRED API with the provided API key.

```python
get_api_key() -> str
```

This function loads the API key from environment variables.

```python
init_store() -> shelve.DbfilenameShelf
```

This function initializes a shelve store and registers a function to close the store at exit.

```python
get_series(fred: fa.Fred, category_id: int) -> pd.DataFrame
```

This function retrieves a list of series from FRED for a given category ID. If the series list for the category ID is already in the store, it returns the list from the store. Otherwise, it fetches the list from FRED and stores it in the store for future use.

```python
fetch_series(fred: fa.Fred, category_id: int) -> pd.DataFrame
```

This function fetches the series for a category ID from FRED. It handles exceptions that occur when fetching a series and returns an empty DataFrame in case of an error.

```python
fetch_all_series(fred: fa.Fred) -> pd.DataFrame
```

This function fetches all series from FRED. It iterates over a range of category IDs and fetches the series for each category ID using the `fetch_series` function. It saves the fetched series to a CSV file every 100 series.

```python
save_to_csv(df: pd.DataFrame) -> None
```

This function saves a DataFrame to a CSV file. The DataFrame should contain the series data fetched from FRED.

```python
main() -> None
```

This function orchestrates the fetching of series data from FRED. It initializes the FRED API, fetches all series, and saves the series data to a CSV file.

## Usage

1. Install the required Python libraries with `pip install -r requirements.txt`.
2. Set your FRED API key as an environment variable named `API_KEY`.
3. Run the script with `python main.py`.

The script will fetch series data from FRED and save it to a CSV file named `series.csv` in the current directory.

## Example

```csv
,id,title,units
0,ARLLRTL,Loan Loss Reserve to Total Loans for Banks in Arkansas (DISCONTINUED),Percent
1,ARLSTL,Net Loan Losses to Average Total Loans for Banks in Arkansas (DISCONTINUED),Percent
2,ARNIM,Net Interest Margin for Banks in Arkansas (DISCONTINUED),Percent
3,ARNPTL,Nonperforming Loans (past due 90+ days plus nonaccrual) to Total Loans for Banks in Arkansas (DISCONTINUED),Percent
4,ARNUM,Commercial Banks in Arkansas (DISCONTINUED),Number
5,ARPLLRTL,Loan Loss Reserve to Total Loans for Banks Geographically Located in Federal Reserve District 8: St. Louis Portion of Arkansas (DISCONTINUED),Percent
6,ARPLSTL,Net Loan Losses to Average Total Loans for Banks Geographically Located in Federal Reserve District 8: St. Louis Portion of Arkansas (DISCONTINUED),Percent
7,ARPNIM,Net Interest Margin for Banks Geographically Located in Federal Reserve District 8: St. Louis Portion of Arkansas (DISCONTINUED),Percent
8,ARPNPTL,Nonperforming Loans (past due 90+ days plus nonaccrual) to Total Loans for Banks Geographically Located in Federal Reserve District 8: St. Louis Portion of Arkansas (DISCONTINUED),Percent
9,ARPNUM,Commercial Banks for Banks Geographically Located in Federal Reserve District 8: St. Louis Portion of Arkansas (DISCONTINUED),Number
10,ARPROA,Return on Average Assets for Banks Geographically Located in Federal Reserve District 8: St. Louis Portion of Arkansas (DISCONTINUED),Percent
```