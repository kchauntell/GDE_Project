import logging
import sys


log_level = 'INFO'
log_file = './testapp.log'

if log_level == 'DEBUG':
    logging.basicConfig(level=logging.DEBUG, format='[Time: %(asctime)s, File: %(filename)s:%(lineno)d, Function: %(funcName)s] %(levelname)-s -  %(message)s',
                        handlers = [
                            logging.FileHandler(log_file),
                            logging.StreamHandler(sys.stdout)
                        ]
    )
elif log_level == 'INFO':
    logging.basicConfig(level=logging.INFO, format='%(message)s',
                        handlers = [
                            logging.FileHandler(log_file),
                            logging.StreamHandler(sys.stdout)
                        ]
    )
else:
    print(f"Logging level '{log_level}' not recognized, defaulting to INFO")
    log_level = 'INFO'
    logging.basicConfig(level=logging.INFO, format='%(message)s',
                        handlers=[
                            logging.FileHandler(log_file),
                            logging.StreamHandler(sys.stdout)
                        ]
    )

logger = logging.getLogger(__name__)
logger.setLevel(log_level)