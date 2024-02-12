import logging
import fredapi as fa
import pandas as pd
import shelve
import time
import atexit
from typing import List, Callable, Tuple
from functools import reduce

logging.basicConfig(level=logging.DEBUG)

# Replace with your FRED API key
api_key = ''

store = shelve.open("store.db")

# On program exit, close the shelve
atexit.register(store.close)


# Initialize FRED API
def init_fred(api_key):
    """Initialize FRED API"""
    return fa.Fred(api_key=api_key)


def category(fred, category_id):
    """Retrieve series list from FRED"""
    str_id = str(category_id)

    # If the category is in the store, return it
    # Otherwise, fetch it from FRED
    if str_id in store:
        logging.debug(f"Fetching category {category_id} from store...")
        return store[str_id]
    else:
        # Sleep for 1 second to avoid rate limiting
        time.sleep(1)
        logging.debug(f"Fetching category {category_id} from FRED...")
        series = fred.search_by_category(category_id=category_id)
        store[str_id] = series
        return series


def fetch_all_series(fred):
    """Fetch all series from FRED"""
    all_series: List[Tuple[str, str, str, str]] = []

    for i in range(100):
        # Log the length of the series list
        logging.debug(f"Series list length: {len(all_series)}")
        try:
            logging.debug(f"Fetching series for category {i}...")
            series = category(fred, i)

            # Zip the series ID and title together
            data = zip(series["id"], series["title"], series["units"], series["notes"])
            all_series.extend(data)
            logging.info(f"Fetched {len(series)} series for category {i}")
        except Exception as e:
            logging.warning(f"Error fetching series: {e}")
            # Set store to empty list to avoid fetching the same category again
            store[str(i)] = []
            continue

    return all_series


def convert_to_dataframe(series_list):
    """Convert series list to DataFrame"""
    return pd.DataFrame(series_list, columns=["Series ID"])


def save_to_csv(df):
    """Save DataFrame to CSV file"""
    df.to_csv("series.csv", index=True)


def compose(functions: List[Callable]):
    """Compose functions"""

    # Debug log the type of the input and output of each function being called and the index of the function
    def debug_compose(*args, **kwargs):
        for i, f in enumerate(functions):
            logging.debug(f"Function {i}: {f.__name__}")
            logging.debug(f"Input: {args}, {kwargs}")
            result = f(*args, **kwargs)
            logging.debug(f"Output: {result}")
            args = (result,)

        return result

    return debug_compose


def main():
    print(dir(init_fred(api_key)))
    ops: List[Callable] = [
        init_fred,
        fetch_all_series,
        convert_to_dataframe,
        save_to_csv,
    ]
    program = compose(ops)
    program(api_key)


if __name__ == "__main__":
    main()
