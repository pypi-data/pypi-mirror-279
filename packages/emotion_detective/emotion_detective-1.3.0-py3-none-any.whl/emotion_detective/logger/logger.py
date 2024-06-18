import os
import logging

def setup_logging():
    """
    Sets up logging for the application.

    This function configures a logger to output log messages to both a file and the console. 
    The log messages include a timestamp, the log level, and the message.

    The log file is saved as 'logs/emotion_detective.txt'.

    Returns:
        logging.Logger: Configured logger instance.
        
    Author: Andrea Tosheva
    """
    # Set up logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Check if logs folder exists, create if it doesn't
    logs_folder = 'logs'
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    # Check if log file exists, create if it doesn't
    log_file = os.path.join(logs_folder, 'emotion_detective.txt')
    if not os.path.exists(log_file):
        with open(log_file, 'w'):
            pass

    # Create file handler and set formatter
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Create console handler and set formatter
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
