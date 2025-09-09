import sys
import os
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
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

def build_lstm_model(input_shape, units, dropout, dense_units, activation, optimizer, loss):
    """
    Build and compile a valid multi-layer LSTM model.
    The original model architecture had an invalid sequence of layers.
    """
    model = Sequential([
        LSTM(units=units, return_sequences=True, input_shape=input_shape),
        Dropout(dropout),
        LSTM(units=units),
        Dropout(dropout),
        Dense(units=dense_units, activation=activation)
    ])
    model.compile(optimizer=optimizer, loss=loss)
    return model

def initiate_model_training(train_data_path: str, test_data_path: str, params, model_name: str, sequence_length: int = 60):
    """
    Train LSTM model on a specific stock or generalized data.
    """
    logging.info(f"Entered initiate_model_training method for {model_name}")
    try:
        # Load processed data
        train_data = MainUtils.load_object(train_data_path)
        test_data = MainUtils.load_object(test_data_path)

        # Dynamically infer number of features
        num_features = train_data.shape[1] - 1  # Last column is the target

        # Reshape data for LSTM
        X_train, y_train = reshape_for_lstm(train_data, sequence_length)
        X_test, y_test = reshape_for_lstm(test_data, sequence_length)

        logging.info(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
        logging.info(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

        # Build model
        model = build_lstm_model(
            input_shape=(sequence_length, num_features),
            units=params['lstm_model']['units'],
            dropout=params['lstm_model']['dropout'],
            dense_units=params['lstm_model']['dense_units'],
            activation=params['lstm_model']['activation'],
            optimizer=params['lstm_model']['optimizer'],
            loss=params['lstm_model']['loss']
        )

        # Define checkpoint directory and path with unique name
        checkpoint_dir = "./artifacts/models/best_models"
        os.makedirs(checkpoint_dir, exist_ok=True)
        checkpoint_path = os.path.join(checkpoint_dir, f"best_model_{model_name}.h5")
        checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_loss', save_best_only=True, verbose=1)

        logging.info(f"Training model for {model_name}...")
        # Train model
        history = model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=params['lstm_model']['epochs'],
            batch_size=params['lstm_model']['batch_size'],
            callbacks=[checkpoint],
            verbose=2
        )
        
        logging.info(f"Model training for {model_name} completed.")

        # Save the final model (in addition to the best checkpoint)
        final_model_dir = "./artifacts/models/final_models"
        os.makedirs(final_model_dir, exist_ok=True)
        final_model_path = os.path.join(final_model_dir, f"final_model_{model_name}.h5")
        model.save(final_model_path)
        logging.info(f"Final LSTM model saved at {final_model_path}")

        return model, history

    except Exception as e:
        logging.error(f"Model training for {model_name} failed: {e}")
        raise MyException(e, sys)

def main():
    try:
        # Load parameters
        params = MainUtils.load_params(PARAMS_FILE_PATH)
        TOP_10_STOCKS = params['data_ingestion']['tickers']
        sequence_length = params['lstm_model'].get('time_step', 60)

        # --- Train on each individual stock ---
        for ticker in TOP_10_STOCKS:
            train_data_path = f"./data/interim/stock_data/train/{ticker}_train_processed.pkl"
            test_data_path = f"./data/interim/stock_data/test/{ticker}_test_processed.pkl"

            if not os.path.exists(train_data_path):
                logging.warning(f"Skipping {ticker}. Processed training data not found at {train_data_path}")
                continue
            
            initiate_model_training(train_data_path, test_data_path, params, ticker, sequence_length)

        # --- Train on the generalized stock data ---
        logging.info("\n--- Initiating training for generalized stock data ---")
        train_data_path_general = "./data/interim/general_stock_data/train/general_train_processed.pkl"
        test_data_path_general = "./data/interim/general_stock_data/test/general_test_processed.pkl"
        
        if not os.path.exists(train_data_path_general):
            logging.error(f"Generalized processed training data not found at {train_data_path_general}. Skipping.")
        else:
            initiate_model_training(train_data_path_general, test_data_path_general, params, "general", sequence_length)

        logging.info("All model training completed successfully.")

    except Exception as e:
        logging.error(f"Model training failed: {e}")
        raise MyException(e, sys)

if __name__ == "__main__":
    main()
