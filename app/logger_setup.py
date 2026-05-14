"""
Logging configuration.
"""
import logging

def setup_logging():
    # TODO 1: Set up basic logging with level INFO using logging.basicConfig()
    logging.basicConfig(level=logging.INFO,
                         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # TODO 2: Create a named logger using logging.getLogger() and return it
    logger = logging.getLogger("churn_api")
    return logger
