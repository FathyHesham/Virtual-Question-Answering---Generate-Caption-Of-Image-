# import libraries
import yaml
from custom_logger.custom_logging import CustomLogger

# Create a custom logger with the name "ConfigLoader"
logger = CustomLogger.create_custom_logger(name = "ConfigLoader")

# Define a class for loading configuration files
class ConfigLoader:
    @staticmethod
    # Define a static method to load the configuration file
    def config_loader(file_name):
        try:
            # Open the configuration file in read mode
            with open(file_name, "r") as file:
                # Load and parse the yaml file
                config = yaml.safe_load(file)
                # Log a success message
                logger.info("Config file loaded successfully.")
                # Return the parsed configuration
                return config
        except FileExistsError:
            # Log an error message if the file is not found
            logger.error(f"config file not found at {file_name}")
            return None
        except yaml.YAMLError as e:
            # Log an error message if there is an error parsing the yaml file
            logger.error(f"error parsing config file : {e}")
            return None
