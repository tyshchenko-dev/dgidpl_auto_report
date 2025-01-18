import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s]: %(message)s",
        handlers=[logging.FileHandler("log.log", "w", "utf-8"), logging.StreamHandler(sys.stdout)],
    )