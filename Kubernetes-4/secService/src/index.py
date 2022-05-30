import time
import os
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BACKEND_URL = os.environ.get ("BACKEND_URL")
MAX_TIMEOUT = 180


def get_date():
    logger.info(f"{BACKEND_URL=}")
    timeout = 5
    while True:
        try:
            response = requests.get(BACKEND_URL)
            response.raise_for_status()
        except Exception as ex:
            if timeout < MAX_TIMEOUT:
                timeout *= 2
            logger.warning(f"Error when receiving data: {ex}. {timeout=} ")
        else:
            timeout = 5
            logger.info(f"Received content: {response.content.decode()}")
        time.sleep(timeout)

if __name__ == '__main__':
    get_date()
