from rulbased_new import process_execution_steps
from backup_functionalities1 import *
from data_preprocessing import keyword_processing
from remove_later import *
import re
import pandas as pd

# # Here is the nested list with keywords which is extracted from instructions
# instructions_list_2 = [['open', 'google', 'browser'], ['open', 'url'], ['click', 'CAMPUS POWER','option'],['click',"Start your journey",'add_text',"child’s financial needs"],['click','INSTITUTE','option'],
#                        ['click', 'Explore More', 'add_text', 'Stand-up Performances']]


# test_cases_list = process_execution_steps('Flipkart - Web.xlsx','keywords.txt')
test_cases_list = keyword_processing('ksample.xlsx')
print('test case list:', test_cases_list)
for sublist in test_cases_list[1:]:
    print("Started New Test Case: -------------------------------------------------------")
    url = sublist[0][0]
    instructions_list = sublist[1]

    # Use the URL and instructions_list variables as needed
    print("URL:", url)
    print("Instructions List:", instructions_list)
    print()

    # hCommon functionality keywords
    dict_keys = ['click','press', 'open', 'hover', 'navigate', 'insert', 'enter', 'search', 'Open', 'Search', 'Click']

    # Used in data preprocessing to remove
    remove_words = ['option', 'menu', 'Button','button']

    # browser list is mandatory.
    browser_list = ['google browser', 'firefox browser', 'chrome browser', 'browser','Google Browser','Chrome Browser','Browser']

    # do not disturb the code
    combined_list = [' '.join(instruction) for instruction in instructions_list]

    print('combined_list: ', combined_list)
    output_list = []
    # for instruction in combined_list:
    #     words = instruction.split()
    #     key = ' '.join(words[1:])
    #     value = words[0]
    #     output_list.append({key: value})

    for instruction in combined_list:
        words = instruction.split()
        if len(words) >= 1:
            key = ' '.join(words[1:])
            value = words[0]
            output_list.append({key: value})

    # Print the output_list
    for item in output_list:
        print(item)

    print('Before output_list:', output_list)


    def process_output_list(output_list):
        processed_list = []
        for entry in output_list:
            for key, value in entry.items():
                words = key.split()
                if len(words) == 3:
                    unique_words = list(set(words))
                    if len(unique_words) == 3:
                        processed_list.append({key: value})
                    else:
                        processed_key = " ".join(unique_words)
                        processed_list.append({processed_key: value})
                else:
                    processed_list.append({key: value})
        return processed_list


    print('After output_list:', process_output_list(output_list))
    output_list = process_output_list(output_list)
    updated_output_list = []

    for item in output_list:
        key = list(item.keys())[0]
        value = item[key]

        for word in remove_words:
            key = key.replace(word, '')

        updated_output_list.append({key: value})

    print('updated_output_list:', updated_output_list)

    click_list = []
    open_list = []
    insert_list = []
    hover_list = []
    searchbox_list = []

    for item in updated_output_list:
        value = list(item.values())[0]
        key = list(item.keys())[0]

        if value == 'click' or value == 'Click' or value == 'press':
            click_list.append(key)
        elif value == 'open' or value == 'Open':
            open_list.append(key)
        elif value == 'insert' or value == 'enter' or value == 'Enter':
            insert_list.append(key)
        elif value == 'hover' or value == 'Hover':
            hover_list.append(key)
        elif value == 'search' or value == 'searchbox' or value == 'Search':
            searchbox_list.append(key)


    # end of do not disturb the code

    def keyword_variation(string):
        # remove spaces
        string = string.strip()

        # Convert the original string to lowercase
        lowercase_string = string.lower()

        # Create a list to store the variations
        variations = [
            lowercase_string,  # "campus power"
            lowercase_string.title(),  # "Campus Power"
            lowercase_string.capitalize(),  # "Campus power"
            string.upper()  # "CAMPUS POWER"
        ]
        return variations


    driver = ''
    for item in updated_output_list:
        value = list(item.values())[0]
        value = value.lower()
        print(value)
        if value == 'open' or value == 'Open':
            print('open triggered')
            key = list(item.keys())[0]
            print('key:', key)
            if key.lower() in browser_list:
                print('key in browser_list')
                driver = browser_function(output_list)

            if key == 'url' or key == 'URL':
                print('url triggered')
                url_function(driver, url)

        if value == 'search' or value == 'Searchbox' or value == 'Search':
            print('search triggered')
            key = list(item.keys())[0]
            print('key:', key)
            if key in searchbox_list:
                print(type(key))
                browser_search_function(url,key, driver)

        if value == 'click' or value == 'Click' or value== 'press':
            print('click triggered')
            key = list(item.keys())[0]
            print('key:', key)
            if key in click_list:
                print(type(key))
                click_function(url,key, driver)

        if value == 'insert' or value == 'enter':
            print('insert/enter triggered')
            key = list(item.keys())[0]
            if key in insert_list:
                print(type(key))
                insert_function(key, driver)

        if value == 'hover' or value == 'Hover':
            print('hover triggered')
            key = list(item.keys())[0]
            if key in hover_list:
                print(type(key))
                hover_function(key, driver)
