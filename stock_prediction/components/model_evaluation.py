import sys
import os
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from stock_prediction.utils.main_utils import MainUtils
from exception import MyException
from logger import logging
from stock_prediction.constants import *

def reshape_for_lstm(data, sequence_length):
    """
    Convert processed stock data into sequences for LSTM.
    Last column is assumed to be the target.
    """
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i + sequence_length, :-1])
        y.append(data[i + sequence_length, -1])
    return np.array(X), np.array(y)

def plot_and_save(original_prices, predicted_prices, model_name, save_path):
    """
    Generates a plot of original vs. predicted prices and saves it.
    """
    try:
        plt.figure(figsize=(14, 7))
        plt.plot(original_prices, color='blue', label=f'Original {model_name} Price')
        plt.plot(predicted_prices, color='red', linestyle='--', label=f'Predicted {model_name} Price')
        plt.title(f'Original vs. Predicted Stock Prices for {model_name}')
        plt.xlabel('Time (Trading Days)')
        plt.ylabel('Price (Scaled)')
        plt.legend()
        plt.grid(True)

        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        plt.close()
        logging.info(f"Plot saved successfully at {save_path}")
    except Exception as e:
        logging.error(f"Failed to plot and save image: {e}")
        raise MyException(e, sys)


def main():
    try:
        logging.info("Starting model evaluation process.")
        
        # Load parameters and tickers from your params file
        params = MainUtils.load_params(PARAMS_FILE_PATH)
        tickers = params['data_ingestion']['tickers']
        sequence_length = params['lstm_model'].get('time_step', 60)
        
        # --- Evaluate and plot for individual tickers ---
        for ticker in tickers:
            logging.info(f"Evaluating model for {ticker}...")
            
            model_path = f"./flask_app/artifacts/models/best_models/best_model_{ticker}.h5"
            test_data_path = f"./data/interim/stock_data/test/{ticker}_test_processed.pkl"
            
            if not os.path.exists(model_path) or not os.path.exists(test_data_path):
                logging.warning(f"Skipping {ticker}. Model or test data not found.")
                continue

            # Load the model and interim test data
            model = load_model(model_path)
            test_data = MainUtils.load_object(test_data_path)
            
            # --- FIX: Added validation for data shape before reshaping and predicting
            num_features_in_data = test_data.shape[1] - 1
            num_features_in_model = model.input_shape[-1]
            
            if num_features_in_data != num_features_in_model:
                logging.error(
                    f"Data shape mismatch for {ticker}. "
                    f"Model trained with {num_features_in_model} features, "
                    f"but test data has {num_features_in_data} features. "
                    f"Please check your preprocessing pipeline. Skipping."
                )
                continue

            # Reshape data for evaluation
            X_test, y_test = reshape_for_lstm(test_data, sequence_length)
            
            # Make predictions
            predictions = model.predict(X_test)
            
            # Plot and save
            plot_save_path = f"./flask_app/artifacts/model_eval/evaluation_{ticker}.png"
            plot_and_save(y_test, predictions, ticker, plot_save_path)
        
        # --- Evaluate and plot for generalized model ---
        logging.info("Evaluating generalized model...")
        model_path_general = "./flask_app/artifacts/models/best_models/best_model_general.h5"
        test_data_path_general = "./data/interim/general_stock_data/test/general_test_processed.pkl"

        if not os.path.exists(model_path_general) or not os.path.exists(test_data_path_general):
            logging.warning("Skipping generalized model. Model or test data not found.")
            return

        model_general = load_model(model_path_general)
        test_data_general = MainUtils.load_object(test_data_path_general)
        
        # --- FIX: Added validation for data shape for generalized model
        num_features_in_data_general = test_data_general.shape[1] - 1
        num_features_in_model_general = model_general.input_shape[-1]

        if num_features_in_data_general != num_features_in_model_general:
            logging.error(
                f"Data shape mismatch for generalized model. "
                f"Model trained with {num_features_in_model_general} features, "
                f"but test data has {num_features_in_data_general} features. "
                f"Please check your preprocessing pipeline. Skipping."
            )
            return

        X_test_general, y_test_general = reshape_for_lstm(test_data_general, sequence_length)
        predictions_general = model_general.predict(X_test_general)

        plot_save_path_general = "./flask_app/artifacts/model_eval/evaluation_general.png"
        plot_and_save(y_test_general, predictions_general, "General", plot_save_path_general)
        
        logging.info("All models evaluated and plots saved.")

    except Exception as e:
        logging.error(f"Model evaluation failed: {e}")
        raise MyException(e, sys)

if __name__ == "__main__":
    main()

