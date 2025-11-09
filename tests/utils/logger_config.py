# import logging

# logging.basicConfig(filename='test_logs.log', level=logging.DEBUG, filemode='W', format="%(name)s -> %(levelname)s: %(message)s")
# logging.debug("This is a debug message")
# logging.warning("This is warning.")
# logger = logging.getLogger(__name__)
# FileOutputHandler = logging.FileHandler('test_logs.log')
# logger.addHandler(FileOutputHandler)
# logger.warning('test.')

import logging
import sys

# --- Clear any existing handlers (important for Jupyter/pytest reruns) ---
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# --- Create logger ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# --- File Handler ---
file_handler = logging.FileHandler('test_logs.log', mode='w')
file_handler.setLevel(logging.DEBUG)

# --- Console Handler ---
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# --- Log Format ---
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# --- Add Handlers to Logger ---
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# --- Example logs ---
logger.debug("Debug log: useful for troubleshooting.")
logger.info("Info log: shows normal execution steps.")
logger.warning("Warning log: something might be off.")
logger.error("Error log: something failed.")
logger.critical("Critical log: major failure.")
