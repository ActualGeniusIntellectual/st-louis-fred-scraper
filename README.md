# FRED Series Fetcher

This Python project fetches and stores data series from the Federal Reserve Economic Data (FRED) API. It uses the `fredapi` Python library to interact with the FRED API. The data is stored in a shelve database for caching purposes, and is also saved to a CSV file.

## File Structure

```
.gitignore
LICENSE
main.py
README.md
requirements.txt
```

## Main Functions

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

This function initializes the shelve database used for caching data.

```python
get_series(fred: fa.Fred, category_id: int, store: shelve.DbfilenameShelf) -> pd.DataFrame
```

This function fetches a data series from the FRED API or the shelve database. If the series is not in the database, it is fetched from the API and then stored in the database.

```python
fetch_series(fred: fa.Fred, category_id: int, store: shelve.DbfilenameShelf) -> pd.DataFrame
```

This function fetches a data series for a specific category and handles exceptions. If an error occurs while fetching the series, an empty DataFrame is returned.

```python
fetch_all_series(fred: fa.Fred, store: shelve.DbfilenameShelf) -> pd.DataFrame
```

This function fetches all data series from the FRED API. The data is fetched in batches, and after every 100 batches, the data is saved to a CSV file.

```python
save_to_csv(df: pd.DataFrame) -> None
```

This function saves a DataFrame to a CSV file.

## How to Run

To run this project, you need to have Python installed on your machine. You can install the required dependencies using pip:

```sh
pip install -r requirements.txt
```

Then, you can run the main script:

```sh
python main.py
```

Please make sure to set your FRED API key in your environment variables before running the script.

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