from main_functionalities import *
from CAOPTIMUM.Model.Model_Prediction import *
from data_preprocessing import *
from text_file_input import *
from text_to_excel import text_to_excel_main
import pandas as pd
from CAOPTIMUM.Validation.validation import test_case_validation
from visualization import visualization
from excel_convertion import excel_utitlity
import os

'''This code defines a function that processes test cases from various file formats 
(CSV, DOC, TXT, or XLSX), extracts relevant data, performs predictions using a machine learning 
model, pre-processes the results, associates credentials, and automates browser interactions 
based on predictions, while logging the process and validating test cases.'''

num_cores = os.cpu_count()
print(f"Number of CPU cores: {num_cores}")
import logging
from CAOPTIMUM.Logs.logger_config import setup_logging


setup_logging("module1_test_case")
logging.info("This is a log message from module1.")


# ThCommon functionality keywords
dict_keys = ['click', 'press', 'open', 'hover', 'navigate', 'insert', 'enter', 'search', 'Open', 'Search', 'Click']

# Used in data preprocessing to remove
remove_words = ['option', 'menu', 'Button', 'button']

# browser list is mandatory.
browser_list = ['google browser', 'firefox browser', 'chrome browser', 'browser', 'Google Browser', 'Chrome Browser',
                'Browser']

""" This block is for test_case_path functionality"""
def process_testcase_with_credentials(test_case_path, credentials_path):
    print('started....')
    # Check file extension
    file_extension = os.path.splitext(test_case_path)[1].lower()
    print('file extension:', file_extension)
    if file_extension == '.csv':
        setup_logging("CSV File:")
        logging.info("CSV FILE DETECTED")
        df = pd.read_csv(test_case_path)
        # Create a new column 'Label' and fill it with the extracted number
        df['Label'] = df['Test case / Scenario'].str.extract(r'(\d+)', flags=re.IGNORECASE)
        df['Label'] = df['Label'].ffill()
        # Call the model_prediction() function with the CSV file
        prediction_result = model_prediction(df)
        logging.info("Model Prediction Completed:")
        pre_processed_result = keyword_processing(prediction_result)
        logging.info("Data Pre-Processing Completed:")

    if file_extension == '.doc' or file_extension == '.txt':
        setup_logging("Text/Doc File:")
        logging.info("DOC/TEXT FILE DETEnCTED")
        # Call text_input() to convert paragraph to steps
        text_to_excel_main(test_case_path)
        test_case_path = r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Scripts\text_doc_excel.xlsx'
        df = excel_utitlity(test_case_path)
        print('df:',df)
        prediction_result = model_prediction(df)
        logging.info("Model Prediction Completed:")
        print('prediction_result:', prediction_result)
        pre_processed_result = keyword_processing(prediction_result)
        logging.info("Data Pre-Processing Completed:")
    if file_extension == '.xlsx':
        setup_logging("XLSX File:")
        logging.info("EXCEL FILE DETECTED")
        # old format
        # excel_to_df['Label'] = excel_to_df['Test case / Scenario'].str.extract(r'(\d+)', flags=re.IGNORECASE)
        # excel_to_df['Label'] = excel_to_df['Label'].ffill()

        # new_format
        excel_to_df = excel_utitlity(test_case_path)
        print('excel_to_df_only:',excel_to_df)
        # from transformers_summarizer import llm_summarize
        # excel_to_df = llm_summarize(excel_to_df)
        print('excel_to_df:', excel_to_df.to_csv('excel_to_df.csv', index=True))
        prediction_result = model_prediction(excel_to_df)
        logging.info("Model Prediction Completed:")
        print('prediction_result:', prediction_result)
        pre_processed_result = keyword_processing(prediction_result)
        logging.info("Data Pre-Processing Completed:")

    print('pre_processed_result', pre_processed_result)
    """ This block is for credentials_path functionality"""
    # Convert the dataframe to the desired dictionary structure
    file_extension_credentials_path = os.path.splitext(credentials_path)[1].lower()
    if file_extension_credentials_path == '.xlsx':
        logging.info("Excel Credential File Detected")
        cred_df = pd.read_excel(credentials_path)
        cred_df['ID'] = cred_df['ID'].astype(str)
        # cred_df['ID'] = cred_df['ID'].str.extract(r'(\d+)', flags=re.IGNORECASE)
        print('Before Label:', cred_df)
        cred_df['ID'] = cred_df['ID'].ffill()
        cred_df.to_csv('Credentials_df.csv', index=False)
        result_dict = {}
        for _, row in cred_df.iterrows():
            label = row['ID']
            attribute = row['Attribute']
            attribute_value = row['Data']


            if label not in result_dict:
                result_dict[label] = {}

            if attribute not in result_dict[label]:
                result_dict[label][attribute] = set()

            result_dict[label][attribute].add(attribute_value)


        # Print the resulting dictionary
        print('result dictionary:', result_dict)

        # Assuming your DataFrame is named 'df'
        pre_processed_result['credentials'] = ''  # Create an empty 'credentials' column

        # Iterate over the rows in the dataframe
        # Iterate over the rows in the dataframe
        for index, row in pre_processed_result.iterrows():
            label = str(row['Label'])

            # Check if the label exists in the nested dictionary
            if label in result_dict:
                nested_values = result_dict[label]

                # Iterate over the major keys in the nested dictionary
                for key in nested_values:
                    # Convert the key and text values to lowercase strings for case-insensitive comparison
                    str_key = str(key).lower()
                    str_text = str(row['Text']).lower()

                    if str_key in str_text:
                        # Assign the major key value to the 'Credential' column at the corresponding index
                        credential_value = nested_values[key]

                        # Convert the credential value from set to string and remove curly braces {}
                        credential_value = str(next(iter(credential_value))).replace('{', '').replace('}', '')

                        pre_processed_result.at[index, 'credentials'] = credential_value
                        break

        print('pre_processed_result:', pre_processed_result)
        pre_processed_result.to_csv('pre_processed_result.csv',index=False)

    def save_cookies(driver, filename):
        with open(filename, 'wb') as f:
            pickle.dump(driver.get_cookies(), f)

    def load_cookies(driver, filename):
        with open(filename, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)

    driver = ''
    for index, row in pre_processed_result.iterrows():
        print('row:', row)

        # Store column values in variables
        text = str(row['Text']) + ' ' + '"' + str(row['credentials']) + '"'
        text = text.replace('""', '')
        prediction = row['Prediction']
        each_step_no = row['Document']
        id = row['Label']



        url = row['URL']
        if row['credentials']:

            # Regular expression pattern to match a URL
            url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'

            # Find all URLs in the string
            urls = re.findall(url_pattern, text)

            # Print the extracted URLs
            for url in urls:
                if url:
                    print('url:', url)
                    url = url

        # Example: Print the column values
        print(f"Text: {text}")
        print(f"Prediction: {prediction}")
        print(f"URL: {url}")
        print("-" * 20)

        if prediction == 'browser':
            setup_logging(id)
            logging.info("Browser Triggered:")
            driver = browser_function(id,each_step_no,prediction)


        if prediction == 'url':
            setup_logging(id)
            logging.info("URL Triggered")
            driver = url_function(driver, url,id,each_step_no,prediction)
            # save_cookies(driver, 'cookies.pkl')


        if prediction == 'search':
            setup_logging(id)
            logging.info("Search Triggered")
            # load_cookies(driver, 'cookies.pkl')
            browser_search_function(driver, url, text,id,each_step_no,prediction)
            # save_cookies(driver, 'cookies.pkl')


        if prediction == 'click':
            setup_logging(id)
            logging.info("Click Triggered:")
            # load_cookies(driver, 'cookies.pkl')
            click_function(driver, url, text,id,each_step_no,prediction)
            # save_cookies(driver, 'cookies.pkl')



        if prediction == 'insert':
            setup_logging(id)
            logging.info("Insert/Enter Triggered:")
            # load_cookies(driver, 'cookies.pkl')
            insert_function(driver, url, text,id,each_step_no,prediction)
            # save_cookies(driver, 'cookies.pkl')


        if prediction == 'hover':
            setup_logging(id)
            logging.info("Hover Triggered:")
            # load_cookies(driver, 'cookies.pkl')
            hover_function(driver, url, text,id,each_step_no,prediction)
            # save_cookies(driver, 'cookies.pkl')


        if prediction == 'previous':
            setup_logging(id)
            logging.info("Previous Page Triggered")
            # load_cookies(driver, 'cookies.pkl')
            previous_function(driver, url, text,id,each_step_no,prediction)
            # save_cookies(driver, 'cookies.pkl')

    test_case_validation()
    visualization()



if __name__ == '__main__':

    test_case_path = r'C:\Users\Optimum.LAPTOP-SQLU1RCT\PycharmProjects\FAP\CAOPTIMUM\Testcases\NewVS.xlsx'
    credentials_path = r'C:\Users\Optimum.LAPTOP-SQLU1RCT\PycharmProjects\FAP\CAOPTIMUM\Credentials\Credentials.xlsx'
    process_testcase_with_credentials(test_case_path, credentials_path)
    logging.info("Execution started:")











