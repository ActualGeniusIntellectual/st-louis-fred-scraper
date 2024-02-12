from functools import reduce
from typing import List, Callable, Tuple
import atexit
import logging
import os
import shelve
import time

import dotenv
import fredapi as fa
import pandas as pd

# Set up logging add timestamp and function name
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

dotenv.load_dotenv()

# Load
api_key = os.getenv("API_KEY")

store = shelve.open("store.db")

# On program exit, close the shelve
atexit.register(store.close)


# Initialize FRED API and other stuff
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
    all_series = []

    for i in range(100):
        # Log the length of the series list
        logging.debug(f"Series list length: {len(all_series)}")
        try:
            series = category(fred, i)
            logging.info(f"Series: {series['id']}")

            # Zip the series ID and title and units and notes
            data = series[["id", "title", "units", "notes"]]
            all_series.append(data)
            logging.info(f"Fetched {len(series)} series for category {i}")
        except Exception as e:
            logging.warning(f"Error fetching series: {e}")
            # Set store to empty list to avoid fetching the same category again
            store[str(i)] = []
            continue

    return pd.concat(all_series, ignore_index=True)


def save_to_csv(df):
    """Save DataFrame to CSV file"""
    logging.info(f"Saving {len(df)} rows to {os.getcwd()}/series.csv...")
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
        save_to_csv,
    ]
    program = compose(ops)
    program(api_key)


if __name__ == "__main__":
    main()
