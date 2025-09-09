# scripts/data_ingestion.py
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)
import os
from logger import logging
from exception import MyException
import sys
import yfinance as yf
from stock_prediction.utils.main_utils import MainUtils
from stock_prediction.constants import *


def fetch_stock_data(ticker: str, start_date=DEFAULT_START_DATE, end_date=DEFAULT_END_DATE) -> pd.DataFrame:
    """Fetch stock data from Yahoo Finance."""
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        df.reset_index(inplace=True)

        # Flatten multi-level columns
        #Your DataFrame has multi-level (hierarchical) column names. That’s why you’re seeing things like:
        #(Date, ) , (Close, GOOG), (High, GOOG) ...
        df.columns = [col[0] if col[1] == '' else f"{col[0]}" for col in df.columns.values]

        logging.info(f'Data fetched for {ticker} with {len(df)} rows')

        #Some Preprocessing
        return df
    except Exception as e:
        logging.error(f'Failed to fetch data for {ticker}: {e}')
        raise MyException(e, sys)
    

def save_data(train_data: pd.DataFrame, test_data: pd.DataFrame, data_path: str, filename: str) -> None:
    """Save train and test data in separate folders."""
    try:
        train_path = os.path.join(data_path, 'train')
        test_path = os.path.join(data_path, 'test')

        os.makedirs(train_path, exist_ok=True)
        os.makedirs(test_path, exist_ok=True)

        train_data.to_csv(os.path.join(train_path, f"{filename}_train.csv"), index=False)
        test_data.to_csv(os.path.join(test_path, f"{filename}_test.csv"), index=False)

        logging.info(f'Train and test data saved for {filename} in {data_path}')
    except Exception as e:
        logging.error(f'Error saving {filename} data: {e}')
        raise MyException(e, sys)

def main():
    try:
        # Load parameters
        params = MainUtils.load_params(PARAMS_FILE_PATH)
        test_size = params['data_ingestion']['test_size']
        TOP_10_STOCKS = params['data_ingestion']['tickers']

        all_stocks_data = []

        # Fetch data for top 10 stocks individually
        for ticker in TOP_10_STOCKS:
            df = fetch_stock_data(ticker)
            df['Ticker'] = ticker  # add Ticker as a proper column
            all_stocks_data.append(df)

            # Split and save individual stock data
            split_idx = int(len(df) * (1 - test_size))
            train_data, test_data = df.iloc[:split_idx], df.iloc[split_idx:]

            save_data(train_data, test_data, data_path='./data/raw/stock_data', filename=ticker)

        # Create generalized dataset for all stocks
        general_df = pd.concat(all_stocks_data, axis=0)
        general_df = general_df.sort_values(by=["Date", "Ticker"]).reset_index(drop=True)

        # Split and save generalized dataset
        split_idx = int(len(general_df) * (1 - test_size))
        train_data, test_data = general_df.iloc[:split_idx], general_df.iloc[split_idx:]
        save_data(train_data, test_data, data_path='./data/raw/general_stock_data', filename='all_stocks')

        logging.info('Data ingestion completed successfully for all stocks.')

    except Exception as e:
        logging.error(f'Failed to complete the data ingestion process: {e}')
        raise MyException(e, sys)

if __name__ == '__main__':
    main()
