# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
#
# # Set the path to your ChromeDriver executable
# chrome_driver_path = 'chrome webdriver/chromedriver.exe'
#
# # Set up the Selenium service
# selenium_service = Service(chrome_driver_path)
#
# # Set up the Selenium driver
# driver = webdriver.Chrome(service=selenium_service)
#
# # Load the URL
# url = 'https://www.godaddy.com/'  # Replace with your desired URL
# driver.get(url)
#
# # Wait for the page to load completely (optional)
# driver.implicitly_wait(10)  # Adjust the wait time as needed
#
# # Get the page source code
# html_code = driver.page_source
#
# # Close the Selenium WebDriver
# driver.quit()
#
# # Create a BeautifulSoup object
# soup = BeautifulSoup(html_code, 'html.parser')
#
# # Prettify the code
# beautified_code = soup.prettify()
#
# # Find all input and textarea tags
# input_tags = soup.find_all(['input', 'textarea'])
#
# # Retrieve attributes of each tag
# for tag in input_tags:
#     tag_name = tag.name
#     attributes = tag.attrs
#     #print(f"Tag Name: {tag_name}")
#     #print("Attributes:")
#     for attr in attributes:
#         #print(f"  - {attr}: {attributes[attr]}")
#     #print()


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def find_input_textarea(html_code,sentence,double_quoted_word):

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_code, 'html.parser')

    # Find all input and textarea tags
    input_tags = soup.find_all(['input', 'textarea','select'])
    #print('input_tags:',input_tags)

    def remove_hidden_inputs(input_tags):
        filtered_tags = []
        for tag in input_tags:
            if 'style="display: none"' not in str(tag):
                filtered_tags.append(tag)
        return filtered_tags

    filtered_inputs = remove_hidden_inputs(input_tags)


    # This for those input tags which doesn't have meaningful values so we try with keys and current requirement for money
    money_synonyms = ['cash', 'currency', 'dollars', 'funds', 'amount', 'rupee']

    # Match each value in the tag attributes with the search sentence using fuzzy token set ratio
    all_attr_list = []
    for each_tag in filtered_inputs:
        for key, value in each_tag.attrs.items():
            # if key.lower() or value.lower() in money_synonyms:
            #     print('Curreny Triggered')
            #     return key,value
            for word in sentence.split():
                if value is not None:
                #if key != 'type':
                    if value:
                        if value != double_quoted_word.replace('"', ''):
                            #print('value:',value,'value type:',type(value),'sentence:',sentence,'sentence type:',type(sentence))
                            att_score = fuzz.token_set_ratio(str(value),sentence)
                            sent_score = fuzz.token_set_ratio(word,value)
                            if att_score > sent_score and att_score > 70:
                                all_attr_list.append([key,value,att_score])
                            elif sent_score > att_score and  sent_score > 70:
                                all_attr_list.append([key,value, sent_score])
                            elif word in value:

                                found_sublists = [sublist for sublist in all_attr_list if [key,value] == sublist[:2]]
                                print('found_sublist:',found_sublists)
                                if not found_sublists:

                                    all_attr_list.append([key,value])
                                    return key,value

                                else:
                                    return key,value

                        elif value == double_quoted_word.replace('"', ''):
                            value = ''
                            #print('key here---------:',key,'value here-------------:',value)
                            return key,value



    print('all_attr_list:',all_attr_list)

    if all_attr_list:
        max_sublist = max(all_attr_list, key=lambda x: x[2])
        max_key, max_value, max_number = max_sublist
        #print(max_key, max_value, max_number)
        if max_value == 'password' or 'Password':
            return max_key, max_value
    else:
        #print("The list is empty.")
        return None,None

        # #print('all_attr_list:',all_attr_list)




