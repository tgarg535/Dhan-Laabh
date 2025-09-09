import sys
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from stock_prediction.constants import *
from exception import MyException
from logger import logging
from stock_prediction.utils.main_utils import MainUtils


def preprocess_stock_data(train_file_path: str, test_file_path: str, scaler_path: str):
    """
    Transforms train/test stock data:
    - Drops non-numeric cols (Date, Ticker, etc.)
    - Scales features with MinMaxScaler
    - Returns numpy arrays with features + target
    """
    logging.info("Entered initiate_data_transformation method")
    try:
        # Load data
        train_data = pd.read_csv(train_file_path)
        test_data = pd.read_csv(test_file_path)
        logging.info(f"Loaded train: {train_file_path}, test: {test_file_path}")

        # Separate features and target
        X_train = train_data.drop(columns=['Date', 'Ticker'], errors="ignore")
        y_train = train_data[TARGET_COLUMN]

        X_test = test_data.drop(columns=['Date', 'Ticker'], errors="ignore")
        y_test = test_data[TARGET_COLUMN]

        # Drop non-numeric columns (like Date, Ticker) and reorder features
        # FIX: Ensure all numeric features are passed to the scaler
        features_for_scaling = ['Open', 'High', 'Low', 'Close', 'Volume']
        X_train = X_train[features_for_scaling]
        X_test = X_test[features_for_scaling]

        # Scale features
        scaler = MinMaxScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Save scaler
        os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
        MainUtils.save_object(scaler_path, scaler)
        logging.info(f"Scaler saved: {scaler_path}")

        # Combine scaled features + target
        # The final array will have 6 columns: 5 features + 1 target
        train_arr = np.c_[X_train_scaled, np.array(y_train)]
        test_arr = np.c_[X_test_scaled, np.array(y_test)]

        return train_arr, test_arr

    except Exception as e:
        raise MyException(e, sys)


def main():
    try:
        params = MainUtils.load_params(PARAMS_FILE_PATH)

        # === Top 10 stocks ===
        TOP_10_STOCKS = params["data_ingestion"]["tickers"]
        train_processed_data_path = "./data/interim/stock_data/train"
        test_processed_data_path = "./data/interim/stock_data/test"
        scaler_path = "./artifacts/scalers/stock_scalers"
        os.makedirs(train_processed_data_path, exist_ok=True)
        os.makedirs(test_processed_data_path, exist_ok=True)
        os.makedirs(scaler_path, exist_ok=True)

        for ticker in TOP_10_STOCKS:
            train_file = f"./data/raw/stock_data/train/{ticker}_train.csv"
            test_file = f"./data/raw/stock_data/test/{ticker}_test.csv"
            scaler_file = os.path.join(scaler_path, f"{ticker}_scaler.pkl")

            train_processed, test_processed = preprocess_stock_data(train_file, test_file, scaler_file)
            MainUtils.save_object(os.path.join(train_processed_data_path, f"{ticker}_train_processed.pkl"), train_processed)
            MainUtils.save_object(os.path.join(test_processed_data_path, f"{ticker}_test_processed.pkl"), test_processed)
            logging.info(f"Processed data saved for {ticker}")

        # === General dataset ===
        train_general_processed_path = "./data/interim/general_stock_data/train"
        test_general_processed_path = "./data/interim/general_stock_data/test"
        general_scaler_path = "./artifacts/scalers/general_stock_scalers"
        os.makedirs(train_general_processed_path, exist_ok=True)
        os.makedirs(test_general_processed_path, exist_ok=True)
        os.makedirs(general_scaler_path, exist_ok=True)

        general_train = "./data/raw/general_stock_data/train/all_stocks_train.csv"
        general_test = "./data/raw/general_stock_data/test/all_stocks_test.csv"
        general_scaler_file = os.path.join(general_scaler_path, "general_stock_scaler.pkl")

        train_processed, test_processed = preprocess_stock_data(general_train, general_test, general_scaler_file)
        MainUtils.save_object(os.path.join(train_general_processed_path, "general_train_processed.pkl"), train_processed)
        MainUtils.save_object(os.path.join(test_general_processed_path, "general_test_processed.pkl"), test_processed)
        logging.info("Processed general stock data saved")

    except Exception as e:
        logging.error(f"Data transformation failed: {e}")
        raise MyException(e, sys)


if __name__ == "__main__":
    main()
