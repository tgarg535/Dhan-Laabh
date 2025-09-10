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
    Preprocess stock data for training/evaluation:
    - Keeps only numeric features: ['Open','High','Low','Close','Volume']
    - Scales both features and target (Close) with MinMaxScaler
    - Saves the fitted scaler
    - Returns X (scaled features), y (scaled target) for train and test
    """
    logging.info("Entered preprocess_stock_data method")
    try:
        # Load data
        train_data = pd.read_csv(train_file_path)
        test_data = pd.read_csv(test_file_path)
        logging.info(f"Loaded train: {train_file_path}, test: {test_file_path}")

        # Select only required features
        train_close_prices = train_data[["Close"]]
        test_close_prices = test_data[["Close"]]

        # Fit scaler on training set only
        scaler = MinMaxScaler(feature_range=(0,1))
        train_close_prices_scaled = scaler.fit_transform(train_close_prices)
        test_close_prices_scaled = scaler.transform(test_close_prices)

        # Save scaler
        os.makedirs(os.path.dirname(scaler_path), exist_ok=True)
        MainUtils.save_object(scaler_path, scaler)
        logging.info(f"Scaler saved: {scaler_path}")

        X_train, y_train = create_sequences(train_close_prices_scaled)
        X_test, y_test = create_sequences(test_close_prices_scaled)

        return X_train, y_train, X_test, y_test, scaler

    except Exception as e:
        raise MyException(e, sys)
    

# 4. Create training sequences
def create_sequences(dataset, seq_length=60):
    X, y = [], []
    for i in range(seq_length, len(dataset)):
        X.append(dataset[i-seq_length:i, 0])  # shape: (seq_length,)
        y.append(dataset[i, 0])
    
    X = np.array(X)
    y = np.array(y)

    # Reshape X to 3D for LSTM: (samples, timesteps, features)
    X = X.reshape((X.shape[0], X.shape[1], 1))  # 1 feature

    return X, y




def main():
    try:
        params = MainUtils.load_params(PARAMS_FILE_PATH)

        # === Top 10 stocks ===
        TOP_10_STOCKS = params["data_ingestion"]["tickers"]
        train_processed_data_path = "./data/interim/stock_data/train"
        test_processed_data_path = "./data/interim/stock_data/test"
        scaler_path = "./flask_app/artifacts/scalers/stock_scalers"
        os.makedirs(train_processed_data_path, exist_ok=True)
        os.makedirs(test_processed_data_path, exist_ok=True)
        os.makedirs(scaler_path, exist_ok=True)

        for ticker in TOP_10_STOCKS:
            train_file = f"./data/raw/stock_data/train/{ticker}_train.csv"
            test_file = f"./data/raw/stock_data/test/{ticker}_test.csv"
            scaler_file = os.path.join(scaler_path, f"{ticker}_scaler.pkl")

            X_train, y_train, X_test, y_test, scaler = preprocess_stock_data(
                train_file, test_file, scaler_file
            )

            MainUtils.save_object(os.path.join(train_processed_data_path, f"{ticker}_train_processed.pkl"), (X_train, y_train))
            MainUtils.save_object(os.path.join(test_processed_data_path, f"{ticker}_test_processed.pkl"), (X_test, y_test))
            logging.info(f"Processed data saved for {ticker}")

        # === General dataset ===
        train_general_processed_path = "./data/interim/general_stock_data/train"
        test_general_processed_path = "./data/interim/general_stock_data/test"
        general_scaler_path = "./flask_app/artifacts/scalers/general_stock_scalers"
        os.makedirs(train_general_processed_path, exist_ok=True)
        os.makedirs(test_general_processed_path, exist_ok=True)
        os.makedirs(general_scaler_path, exist_ok=True)

        general_train = "./data/raw/general_stock_data/train/all_stocks_train.csv"
        general_test = "./data/raw/general_stock_data/test/all_stocks_test.csv"
        general_scaler_file = os.path.join(general_scaler_path, "general_stock_scaler.pkl")

        X_train, y_train, X_test, y_test, scaler = preprocess_stock_data(
            general_train, general_test, general_scaler_file
        )

        MainUtils.save_object(os.path.join(train_general_processed_path, "general_train_processed.pkl"), (X_train, y_train))
        MainUtils.save_object(os.path.join(test_general_processed_path, "general_test_processed.pkl"), (X_test, y_test))
        logging.info("Processed general stock data saved")

    except Exception as e:
        logging.error(f"Data transformation failed: {e}")
        raise MyException(e, sys)


if __name__ == "__main__":
    main()
