import os
from datetime import datetime

# -------------------------------
# Project-level constants
# -------------------------------

# Configurations
PARAMS_FILE_PATH = "params.yaml"


# Default date range for stock data ingestion
DEFAULT_START_DATE = "2015-01-01"
DEFAULT_END_DATE = datetime.today().strftime("%Y-%m-%d")

# Target column for prediction
TARGET_COLUMN = "Close"
