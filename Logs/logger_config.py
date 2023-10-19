# logger_config.py

import logging

def setup_logging(test_case_name):
    log_file_path = f"C:\\Users\\abdul\\PycharmProjects\\Automation_Optimum\\Logs\\{test_case_name}.log"
    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
