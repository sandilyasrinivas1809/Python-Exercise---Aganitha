
#==============================================================================
# Importing the modules
#==============================================================================
import os
import logging
from datetime import datetime

# Creating a folder inside the code folder named 'logs' if it does not exist
LOG_PATH = r"logs"
LOG_FOLDER = rf"{LOG_PATH}"
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

'''
Creating one folder inside the Log folder based on the date on which the code 
runs so that all the corresponding log files from all the code snippets can be 
stored there
'''
# creating folder and filename with datetime to save output
NOW = datetime.now().strftime("%Y%m%d")
DAY_RUN_LOGS_FOLDER = rf"{LOG_FOLDER}\{NOW}_logs"
if not os.path.exists(DAY_RUN_LOGS_FOLDER):
    os.makedirs(DAY_RUN_LOGS_FOLDER)


def debug_logger():

    """

    Returns
    -------
    main_logger : TYPE
        DESCRIPTION.

    """
    main_logger_file_name = f"{DAY_RUN_LOGS_FOLDER}/{datetime.now():'%Y%m%d %H%M%S'}_debug.log" 
    main_logger = logging.getLogger("MAIN")
    main_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - [%(name)s][%(levelname)s] - %(message)s')
    streamhandler = logging.StreamHandler()
    streamhandler.setLevel(logging.INFO)
    streamhandler.setFormatter(formatter)
    filehandler = logging.FileHandler(main_logger_file_name)
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    if main_logger.hasHandlers():
        main_logger.handlers.clear()
    main_logger.addHandler(streamhandler)
    main_logger.addHandler(filehandler)
    return main_logger

def normal_logger():
    """

    Returns
    -------
    normal_logger : TYPE
        DESCRIPTION.

    """
    main_logger_file_name = f"{DAY_RUN_LOGS_FOLDER}/{datetime.now():'%Y%m%d %H%M%S'}_info.log" 
    main_logger = logging.getLogger("MAIN")
    main_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - [%(name)s][%(levelname)s] - %(message)s')
    filehandler = logging.FileHandler(main_logger_file_name)
    filehandler.setLevel(logging.INFO)
    filehandler.setFormatter(formatter)
    if main_logger.hasHandlers():
        main_logger.handlers.clear()
    main_logger.addHandler(filehandler)
    return main_logger