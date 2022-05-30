import datetime
import time
import os
import signal
from threading import Timer
import logging
from flask import Flask
from flask import abort



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SIGTERM_RECEIVED = False
REQUESTS_COUNT = 0


def graceful_shutdown():
    time_left = SIGTERM_RECEIVED + 20 - time.time()
    if not REQUESTS_COUNT:
        logger.info("Exit with status 0")
        os._exit(0)
    elif time_left < 0:
        logger.error(f"Exit with status 1. {REQUESTS_COUNT} requests are not completed")
        os._exit(1)
    else:
        logger.info(f"{REQUESTS_COUNT} requests in queue. Time left {time_left}")
        timer = Timer(5, graceful_shutdown)
        timer.start()

def handle_sigterm(signum, frame):
    global SIGTERM_RECEIVED
    if not SIGTERM_RECEIVED:
        SIGTERM_RECEIVED = time.time()
        logger.info(f"SIGTERM received")
        graceful_shutdown()

signal.signal(signal.SIGTERM, handle_sigterm)


app = Flask(__name__)

@app.route('/')
def get_date():
    if SIGTERM_RECEIVED:
        abort(503)
    else:
        global REQUESTS_COUNT
        REQUESTS_COUNT += 1
        response = str(datetime.datetime.now())
        time.sleep(13)
        REQUESTS_COUNT -= 1
    return response
