import logging
from typing import Any, Optional
import os

class Logger:
    """Class for logging all the events"""
    def __init__(self, 
                 log_file:str, 
                 log_level:int=logging.INFO) -> None:
        """
        Constructor for the class logger

        @params log_file: file name to be written
        @params log_level: if its info, warning etc.,
        """
        self.log_file = log_file
        self.log_level = log_level

        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        # Configure the logging system in the constructor
        logging.basicConfig(filename=self.log_file, level=self.log_level, format='%(asctime)s - %(levelname)s: %(message)s')

    def log(self, 
            message:Any, 
            log_level=logging.INFO) -> None:
        """
        Method to log the message.

        @params message: message to be logged
        @params log_level: WARNING, INFO etc.,
        """
        # Log a message with the specified log level
        logging.log(log_level, message)