# Import the logging library
import logging

# Define a custom logger class
class CustomLogger:
    @staticmethod
    def create_custom_logger(name):
        # Create a logger with the specified name
        logger = logging.getLogger(name)
        # Set the logging level to DEBUG
        logger.setLevel(logging.DEBUG)

        # Create a console handler
        console_handler = logging.StreamHandler()
        # Set the logging level for the console handler to INFO
        console_handler.setLevel(logging.INFO)
        
        # Create a file handler
        file_handler = logging.FileHandler("VQA.log")
        # Set the logging level for the file handler to DEBUG
        file_handler.setLevel(logging.DEBUG)
        
        # Create a custom formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # Add the formatter to the console handler
        console_handler.setFormatter(formatter)
        # Add the formatter to the file handler
        file_handler.setFormatter(formatter)
        
        # Add the console handler to the logger
        logger.addHandler(console_handler)
        # Add the file handler to the logger
        logger.addHandler(file_handler)

        # Return the configured logger
        return logger