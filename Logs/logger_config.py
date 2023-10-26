# logger_config.py

import logging

''' 
This code sets up logging for a test case by configuring the log file path, log level, and log 
format. It creates a log file with the specified name and logs messages with timestamps, log levels,
 and messages in a specific format to that file.
'''
def setup_logging(test_case_name):
    log_file_path = f"C:\\Users\\Optimum.LAPTOP-SQLU1RCT\\PycharmProjects\\FAP\\CAOPTIMUM\\Logs\\{test_case_name}.log"
    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
