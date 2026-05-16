"""
Logging configuration with Axiom integration.
"""
import logging
import os
import json
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
from axiom_py import Client

load_dotenv()

AXIOM_TOKEN = os.getenv("AXIOM_TOKEN")
AXIOM_DATASET = os.getenv("AXIOM_DATASET")

# Initialize Axiom client at module level
axiom_client = Client(AXIOM_TOKEN)


def setup_logging():
    # Set up basic logging with level INFO
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    # Create and return a named logger
    logger = logging.getLogger("churn_api")
    return logger


def send_to_axiom(event: dict):
    """
    Send a structured event/log to Axiom dataset.
    """
    try:
        event["_time"] = datetime.now(timezone.utc).isoformat()
        axiom_client.ingest_events(
            dataset=AXIOM_DATASET,
            events=[event]
        )
    except Exception as e:
        logging.getLogger("churn_api").error(f"Failed to send to Axiom: {e}")