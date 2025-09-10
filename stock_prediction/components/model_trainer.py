import sys
import os
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint
from stock_prediction.utils.main_utils import MainUtils
from exception import MyException
from logger import logging
from stock_prediction.constants import *

def build_lstm_model(input_shape, units, dropout, activation, optimizer, loss):
    """
    Build and compile a simple multi-layer LSTM model for single-feature regression.
    """
    model = Sequential([
        LSTM(units=units, return_sequences=True, input_shape=input_shape),
        Dropout(dropout),
        LSTM(units=units, return_sequences=False),
        Dropout(dropout),
        Dense(1, activation=activation)  # Output layer predicts Close
    ])
    model.compile(optimizer=optimizer, loss=loss)
    return model

def initiate_model_training(train_data_path: str, test_data_path: str, params, model_name: str):
    """
    Train LSTM model on a specific stock or generalized dataset.
    Assumes X_train/X_test are already 3D and y_train/y_test are 1D.
    """
    logging.info(f"Training model for {model_name}")
    try:
        # Load preprocessed data (X_train, y_train), (X_test, y_test)
        X_train, y_train = MainUtils.load_object(train_data_path)
        X_test, y_test = MainUtils.load_object(test_data_path)

        logging.info(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
        logging.info(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

        # Build LSTM model
        input_shape = (X_train.shape[1], X_train.shape[2])  # (timesteps, features)
        model = build_lstm_model(
            input_shape=input_shape,
            units=params['lstm_model']['units'],
            dropout=params['lstm_model']['dropout'],
            activation=params['lstm_model']['activation'],
            optimizer=params['lstm_model']['optimizer'],
            loss=params['lstm_model']['loss']
        )

        # Checkpoint to save best model
        checkpoint_dir = "./flask_app/artifacts/models/best_models"
        os.makedirs(checkpoint_dir, exist_ok=True)
        checkpoint_path = os.path.join(checkpoint_dir, f"best_model_{model_name}.h5")
        checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_loss', save_best_only=True, verbose=1)

        # Train model
        history = model.fit(
            X_train, y_train,
            validation_data=(X_test, y_test),
            epochs=params['lstm_model']['epochs'],
            batch_size=params['lstm_model']['batch_size'],
            callbacks=[checkpoint],
            verbose=2
        )

        # Save final model
        final_model_dir = "./flask_app/artifacts/models/final_models"
        os.makedirs(final_model_dir, exist_ok=True)
        final_model_path = os.path.join(final_model_dir, f"final_model_{model_name}.h5")
        model.save(final_model_path)
        logging.info(f"Final model saved at {final_model_path}")

        return model, history

    except Exception as e:
        logging.error(f"Model training failed for {model_name}: {e}")
        raise MyException(e, sys)

def main():
    try:
        params = MainUtils.load_params(PARAMS_FILE_PATH)
        TOP_10_STOCKS = params['data_ingestion']['tickers']

        # Train individual stocks
        for ticker in TOP_10_STOCKS:
            train_path = f"./data/interim/stock_data/train/{ticker}_train_processed.pkl"
            test_path = f"./data/interim/stock_data/test/{ticker}_test_processed.pkl"

            if not os.path.exists(train_path):
                logging.warning(f"Skipping {ticker}. Processed training data not found.")
                continue

            initiate_model_training(train_path, test_path, params, ticker)

        # Train generalized dataset
        train_path_gen = "./data/interim/general_stock_data/train/general_train_processed.pkl"
        test_path_gen = "./data/interim/general_stock_data/test/general_test_processed.pkl"

        if os.path.exists(train_path_gen):
            initiate_model_training(train_path_gen, test_path_gen, params, "general")
        else:
            logging.warning("General dataset not found. Skipping generalized training.")

        logging.info("All model training completed successfully.")

    except Exception as e:
        logging.error(f"Overall model training failed: {e}")
        raise MyException(e, sys)

if __name__ == "__main__":
    main()