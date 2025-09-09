import sys
import os

import pickle
import yaml

from stock_prediction.constants import *
from exception import MyException
from logger import logging


class MainUtils:
    def __init__(self) -> None:
        pass

    def read_yaml_file(self, filename: str) -> dict:
        try:
            with open(filename, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)

        except Exception as e:
            raise MyException(e, sys) from e

    def read_schema_config_file(self) -> dict:
        try:
            schema_config = self.read_yaml_file(os.path.join("config", "schema.yaml"))

            return schema_config

        except Exception as e:
            raise MyException(e, sys) from e

    

    @staticmethod
    def save_object(file_path: str, obj: object) -> None:
        logging.info("Entered the save_object method of MainUtils class")

        try:
            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)

            logging.info("Exited the save_object method of MainUtils class")

        except Exception as e:
            raise MyException(e, sys) from e

    @staticmethod
    def load_object(file_path: str) -> object:
        logging.info("Entered the load_object method of MainUtils class")

        try:
            with open(file_path, "rb") as file_obj:
                obj = pickle.load(file_obj)

            logging.info("Exited the load_object method of MainUtils class")

            return obj

        except Exception as e:
            raise MyException(e, sys) from e
        


    @staticmethod
    def load_params(params_path: str = PARAMS_FILE_PATH) -> dict:
        """Load parameters from a YAML file."""
        try:
            with open(params_path, 'r') as file:
                params = yaml.safe_load(file)
            logging.debug('Parameters retrieved from %s', params_path)
            return params
        
        except FileNotFoundError as e:
            logging.error('File not found: %s', params_path)
            raise MyException(e, sys)
        except yaml.YAMLError as e:
            logging.error('YAML error: %s', e)
            raise MyException(e, sys)
        except Exception as e:
            logging.error('Unexpected error: %s', e)
            raise MyException(e, sys)
