from typing import List, Optional
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
api_key: Optional[str] = os.getenv("API_KEY")
store: Optional[shelve.DbfilenameShelf] = None


# Initialize FRED API and other stuff
def init_fred(api_key: str) -> fa.Fred:
    """Initialize F API"""
    return fa.Fred(api_key=api_key)


def get_api_key() -> str:
    """Load API key from environment variables"""
    dotenv.load_dotenv()
    return os.getenv("API_KEY")


def init_store() -> shelve.DbfilenameShelf:
    """Initialize the store"""
    global store
    store = shelve.open("store.db")
    atexit.register(store.close)
    return store


def get_series(
    fred: fa.Fred, category_id: int, store: shelve.DbfilenameShelf
) -> pd.DataFrame:
    """Fetch series from FRED or store"""
    str_id = str(category_id)
    if str_id in store:
        logging.debug(f"Fetching category {category_id} from store...")
        return store[str_id]
    else:
        time.sleep(1)
        logging.debug(f"Fetching category {category_id} from FRED...")
        series = fred.search_by_category(category_id=category_id)
        store[str_id] = series
        return series


def fetch_series(
    fred: fa.Fred, category_id: int, store: shelve.DbfilenameShelf
) -> pd.DataFrame:
    """Fetch series for a category and handle exceptions"""
    try:
        series = get_series(fred, category_id, store)
        data = series[["id", "title", "units"]]
        logging.info(f"Fetched {len(series)} series for category {category_id}")
        return data
    except Exception as e:
        logging.debug(f"Error at category {category_id} fetching series: {e}")
        store[str(category_id)] = []
        return pd.DataFrame()


def fetch_all_series(fred: fa.Fred, store: shelve.DbfilenameShelf) -> pd.DataFrame:
    """Fetch all series from FRED"""
    all_series: List[pd.DataFrame] = []
    for i in range(10000):
        logging.debug(f"Series list length: {len(all_series)}")
        if i > 0 and i % 100 == 0:
            logging.info(f"Saving {len(all_series)} series to CSV...")
            save_to_csv(pd.concat(all_series, ignore_index=True))
        data = fetch_series(fred, i, store)
        all_series.append(data)
    return pd.concat(all_series, ignore_index=True)


def save_to_csv(df: pd.DataFrame) -> None:
    """Save DataFrame to CSV file"""
    logging.info(f"Saving {len(df)} rows to {os.getcwd()}/series.csv...")
    df.to_csv("series.csv", index=True)


def main() -> None:
    api_key: Optional[str] = get_api_key()
    store: shelve.DbfilenameShelf = init_store()
    fred: fa.Fred = init_fred(api_key)
    all_series: pd.DataFrame = fetch_all_series(fred, store)
    save_to_csv(all_series)


if __name__ == "__main__":
    main()
    logging.info("Done!")
