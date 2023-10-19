import contextlib
import math
import time
import re

import editdistance

from delelte_later import find_input_textarea
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from undetected_chromedriver import ChromeOptions
from bs4 import BeautifulSoup
import concurrent.futures
from nltk.corpus import wordnet
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from collections import defaultdict
import os
import pyautogui
import logging
from lxml import etree

# Set up logging
logging.basicConfig(
    filename='app.log',  # Specify the log file name
    level=logging.DEBUG,  # Set the desired logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set the log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Set the date-time format for log messages
)

path = 'Screenshot'


def take_screenshot(base_folder, test_case, filename):
    try:
        # Create the subfolder for the current test case
        folder = os.path.join(base_folder, test_case)
        if not os.path.exists(folder):
            os.makedirs(folder)

        screenshot = pyautogui.screenshot()
        file_path = os.path.join(folder, filename)
        # screenshot.save(file_path)
    except Exception as e:
        logging.error(f"Failed to take screenshot: {str(e)}")

def previous_function(driver):
    driver.back()

def browser_function(id, each_step_no, prediction):
    try:
        print('Browser Functionality Triggered')
        # chrome_options = webdriver.ChromeOptions()
        chrome_options = ChromeOptions()
        # chrome_options.add_argument(
        #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36")
        # Adding argument to disable the AutomationControlled flag
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-application-cache")  # Disable application cache
        chrome_options.add_argument("--disable-cache")  # Disable in-memory cache
        chrome_options.add_argument("--disk-cache-size=0")
        # chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-blink-features")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--enable-javascript")
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
        print(driver.execute_script("return navigator.userAgent;"))
        # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Store the initial window handle (current tab)
        initial_window_handle = driver.current_window_handle
        logging.info("Browser Functionality Completed")
        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
        return driver
    except:
        logging.info("Browser Functionality Failed")
        take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')


def url_function(driver, url, id, each_step_no, prediction):
    if driver:
        print('URL Functionality Triggered')
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.implicitly_wait(20)
        driver.get(url)
        cookies = driver.get_cookies()
        logging.info("URL Opened Successfully")
        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
        return driver
    else:
        driver = browser_function(id, each_step_no, prediction)
        print('Else URL Functionality Triggered')
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.implicitly_wait(20)
        driver.get(url)
        cookies = driver.get_cookies()
        logging.info("URL Opened Successfully")
        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
        return driver
    # except:
    #     logging.info("URL Open Failed")
    #     take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')



def browser_search_function(driver, url, key, id, each_step_no, prediction):
    try:
        driver.get('https://www.google.co.in')
        wait = WebDriverWait(driver, 20)  # Maximum wait time of 10 seconds
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='APjFqb']")))
        search_box.click()
        search_box.send_keys(url)
        search_button = wait.until(EC.element_to_be_clickable((By.NAME, "btnK")))
        search_button.click()
        logging.info("Browser Searching Completed successfully")
        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
        time.sleep(5)
    except:
        logging.info("Browser Searching Failed")
        take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')


def click_function(driver, clickable_url, keyword, id, each_step_no, prediction):

    try:
        alert = Alert(driver)
        alert.accept()  # Use .dismiss() to click "Cancel" if needed
    except Exception:
        # If there is no alert, an exception will be raised (no need to handle it)
        pass

    # if 'checkbox' or 'check box' in keyword:
    #     checkbox = driver.find_element_by_xpath("//input[@type='checkbox']")
    #     checkbox.click()

    print('Click Function Triggered:')
    keyword = keyword.replace('nan', '')
    # if len(driver.window_handles) > 1:
    #     print('Window has now shifted new')
    #     # Switch to the new tab
    #     driver.switch_to.window(driver.window_handles[-1])
    time.sleep(4)
    global double_quoted_word
    print('click functionality triggered')

    print('keyword in the begin:', keyword)

    # Search for "add_text" within double quotes
    match = re.search(r'"([^"]*add_text[^"]*)"', keyword)
    keyword = keyword
    # If a match is found, remove the double quotes from the matched group
    if match:
        keyword = keyword.replace(match.group(0), match.group(1).replace('"', ''))
        print('keyword:', keyword)

    # Extract the double-quoted string using regular expressions
    double_quotes_match = re.search(r'"([^"]+)"', keyword)
    double_quoted_keyword = ''
    if double_quotes_match:
        double_quoted_word = double_quotes_match.group(1)
        double_quoted_keyword = double_quoted_word
    try:
        # Simulate pressing the Escape key
        body_element = driver.find_element("tag name", "body")
        body_element.send_keys(Keys.ESCAPE)
    except:
        pass


    # Check if the instruction string contains 'add_text'
    if 'add_text' in keyword:
        print('add_text is available in the keyword')
        # Split the string into left and right parts, excluding 'add_text'
        parts = keyword.split('add_text')
        keyword = parts[0].strip()
        keyword = keyword.replace('"', '')
        additional_info = parts[1].strip()
    else:
        keyword = keyword
        additional_info = None

    # Construct the XPath query to find the desired element based on the additional information

    try:
        search_element = WebDriverWait.until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(@*, {double_quoted_keyword})]")))
        search_element.click()
    except:
        pass

    if additional_info:
        try:
            def compute_distance(location1, location2):
                """Calculate the Euclidean distance between two points."""
                return math.sqrt((location1['x'] - location2['x']) ** 2 + (location1['y'] - location2['y']) ** 2)

            def click_nearest_target_to_sub_text(target_text, sub_text=None):
                print('started -----------------------------------------------------------------')

                # Set up WebDriverWait
                wait = WebDriverWait(driver, 30)  # 30 seconds timeout

                # If sub_text is provided, find its location
                if sub_text:
                    # Let's first take a snippet of the sub_text to locate a potential match
                    snippet = sub_text[:20]  # assuming the first 20 characters can be a good snippet; adjust as necessary

                    # Find potential elements that might have the sub_text
                    potential_sub_elements = wait.until(
                        EC.presence_of_all_elements_located((By.XPATH, f"//*[contains(text(), '{snippet}')]")))

                    # Filter elements to check if they match the whole sub_text
                    matching_elements = [elem for elem in potential_sub_elements if sub_text in elem.text]

                    if not matching_elements:
                        print("No matching sub_text found!")
                        return

                    sub_element = matching_elements[
                        0]  # choosing the first match; adjust logic if there are multiple valid matches
                    sub_location = sub_element.location
                else:
                    sub_location = None

                # Wait until at least one target_text element is present
                wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{target_text}')]")))

                # Find all elements that have the target_text
                target_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{target_text}')]")

                if not target_elements:
                    print("No target elements found!")
                    return

                if sub_location:
                    # If sub_location is found, find the target_text element closest to the sub_text
                    nearest_element = min(target_elements, key=lambda elem: compute_distance(elem.location, sub_location))
                else:
                    # If no sub_location, simply click on the first target_text found
                    nearest_element = target_elements[0]

                # Click on the nearest target_text
                nearest_element.click()


            click_nearest_target_to_sub_text(double_quoted_keyword, additional_info)
        except:
            logging.info("Click Functionality Failed")
            take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')



        # If we need all xpaths then we will uncomment and use it

        # print('click url:', driver.current_url)
        # html_code = driver.page_source
        # prettified_html = pretty_code(html_code)
        # print('Double Quoted Keyword:', double_quoted_keyword, '&', 'additional info:', additional_info)
        # original_xpath = find_element(prettified_html, double_quoted_keyword, additional_info)
        # print('full_Xpath: ', original_xpath)
        # final_xpath = mod_xpath(original_xpath)
        # print('final_xpath:', final_xpath)
        #
        # if final_xpath == ['E/l/e/m/e/n/t/ /n/o/t/ /f/o/u/n/d/.']:
        #     print("Elements not found entered")
        #     # Perform the "Tab" key press using ActionChains
        #     action_chains = ActionChains(driver)
        #     action_chains.send_keys(Keys.TAB).perform()
        #
        #     # Optional: Add a small delay to ensure the focus changes
        #     time.sleep(1)
        #
        #     # Perform a click at the currently focused element (where the focus is after pressing "Tab")
        #     driver.switch_to.active_element.click()
        #     logging.info("click functionality complted Successfully")
        # else:
        #     for i in final_xpath:
        #         # Wait for the keyword element to appear
        #         item = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, i)))
        #         item.click()
        #         logging.info("click functionality complted Successfully")
        #         try:
        #             print('dropdown entered')
        #             dropdown = Select(item)
        #             text_to_select = double_quoted_keyword
        #             dropdown.select_by_visible_text(text_to_select)
        #             logging.info("click functionality complted Successfully")
        #         except:
        #             pass
        #
        #         # Print success message
        #         print("Program executed successfully.")
        #         # Sleep
        #         time.sleep(5)




    elif 'official link' in keyword or 'original link' in keyword or 'link' in keyword:
        try:
            print('This official link block is executed')
            url = clickable_url
            # Wait for the search results to appear
            wait = WebDriverWait(driver, 20)
            search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g")))
            from urllib.parse import urlparse

            def extract_domain(url):
                parsed_url = urlparse(url)
                domain = parsed_url.netloc
                return domain

            domain = extract_domain(url)
            print('domain', domain)
            # Find and click the first link that corresponds to Flipkart
            for result in search_results:
                link = result.find_element(By.XPATH, ".//a")
                if domain in link.get_attribute("href"):
                    link.click()
                    logging.info("click functionality complted Successfully")
                    break
        except:
            logging.info("Click Functionality Failed")
            take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
    else:
        try:
            target_element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{double_quoted_keyword}')]")))
            target_element.click()
        except NoSuchElementException:
            try:
                target_element1 = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, f"//*contains(text(),'{double_quoted_keyword}')]")))
                target_element1.click()
            except NoSuchElementException:
                try:
                    print('click url:', driver.current_url)
                    html_code = driver.page_source
                    prettified_html = pretty_code(html_code)
                    # # with open('output.html', 'w', encoding='utf-8') as file:
                    # #     file.write(prettified_html)
                    # # print('Double Quoted Keyword:', double_quoted_keyword, '&', 'additional info:', additional_info)
                    original_xpath = find_element(prettified_html, double_quoted_keyword, additional_info)
                    print('full_Xpath: ', original_xpath)
                    final_xpath = mod_xpath(original_xpath)
                    print('final_xpath:', final_xpath)
                #
                #     def click_element(xpath):
                #         try:
                #             # Wait for the keyword element to appear
                #             val = WebDriverWait(driver, 20).until(
                #                 EC.presence_of_element_located((By.XPATH, xpath)))
                #             val.click()
                #             driver.quit()
                #             return f"Clicking on XPath: {xpath} was successful"
                #         except Exception as e:
                #             driver.quit()
                #             return f"Error while clicking on XPath: {xpath}. Error: {e}"
                #
                #     with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                #         # This will execute the tasks concurrently using threads
                #         for result in executor.map(click_element, final_xpath):
                #             print(result)
                # except NoSuchElementException:
                #     pass

                    for i in final_xpath:
                        print('Triggered i 2')
                        try:
                            # Wait for the keyword element to appear
                            val = WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.XPATH, i)))
                            val.click()
                            logging.info("click functionality complted Successfully")
                        except:
                            try:
                                if 'button' in keyword:
                                    button = driver.find_element_by_xpath(
                                        '//input[(contains(@value, "Submit") and @type="button") or (contains(@value, "Submit") and @type="btn")]')
                                    button.click()
                            except:
                                logging.info("click Functionality Failed")
                                take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
                except:
                    pass

            except NoSuchElementException:
                logging.info("click Functionality Failed")
                take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')

                # from multiprocessing import Pool
                # def selenium_function(url):
                #     # initialize driver
                #     driver = webdriver.Chrome()
                #     driver.get(url)
                #     # continue selenium operations...
                #     driver.quit()
                #
                # if __name__ == "__main__":
                #     urls = ["http://www.google.com", "http://www.bing.com", "http://www.yahoo.com",
                #             "http://www.duckduckgo.com"]
                #     with Pool(4) as p:  # the number in Pool() is the number of cores you want to use
                #         p.map(selenium_function, urls)

        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')

    #     take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')




    # try:
    #     # Find the element with the text "Red"
    #     red_element = prettified_html.find(text=f'{double_quoted_keyFword}')
    #
    #     # Get the XPath of the "Red" element
    #     def get_xpath(element):
    #         elements = [e.name for e in element.parents][::-1]
    #         return '/'.join(elements)
    #
    #     red_xpath = get_xpath(red_element)
    #
    #     print("XPath of the 'Red' element:", red_xpath)
    # except:
    #     pass
    #
    # # In case after hover if Click Function is Triggered and Hover is not invisible
    # try:
    #     action = ActionChains(driver)
    #     body_element = driver.find_element_by_tag_name("body")
    #     action.move_to_element(body_element).perform()
    # except:
    #     pass

    # # Parse the HTML content using BeautifulSoup
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    #
    # # Find all the <input> elements with type="login" or type="submit" and name containing "login" or "submit" on the webpage
    # # buttons = soup.find_all('input', {'type': ['login', 'submit'], 'name': ['login', 'submit']})
    # buttons = soup.find_all('input')
    # print('buttons:', buttons)
    # Iterate over the buttons and perform a click action if the values match
    # for button in buttons:
    #     print('for loop in button started:')
    #     button_type = button.get('type', '')
    #     button_name = button.get('name', '')
    #     button_value = button.get('value', '')
    #
    #     # Perform a click action on matching buttons
    #     if 'login' in button_value.lower() or 'submit' in button_value.lower():
    #         # Perform click action using Selenium
    #         wait = WebDriverWait(driver, 20)
    #         element = wait.until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, f"[type={button_value}]")))
    #         element.click()


last_tag_value = []


def insert_function(driver, url, keyword, id, each_step_no, prediction):
    try:
        try:
            alert = Alert(driver)
            alert.accept()  # Use .dismiss() to click "Cancel" if needed
        except:
            # If there is no alert, an exception will be raised (no need to handle it)
            pass
        try:
            main_window = driver.current_window_handle
            new_window = WebDriverWait(driver, 20).until(EC.new_window_is_opened)
            driver.switch_to.window(new_window)
            logging.info("Switched to New Window Successfully")
        except:
            pass
        time.sleep(6)
        try:
            # Check if a new tab has been opened
            if len(driver.window_handles) > 1:
                # Switch to the new tab
                driver.switch_to.window(driver.window_handles[1])
            print('Insert Functionality Triggered')
        except:
            pass

        # Search for "add_text" within double quotes
        match = re.search(r'"([^"]*add_text[^"]*)"', keyword)
        keyword = keyword
        # If a match is found, remove the double quotes from the matched group
        if match:
            keyword = keyword.replace(match.group(0), match.group(1).replace('"', ''))
            print('keyword:', keyword)

        # Extract the double-quoted string using regular expressions
        double_quotes_match = re.search(r'"([^"]+)"', keyword)
        double_quoted_keyword = ''
        if double_quotes_match:
            double_quoted_word = double_quotes_match.group(1)
            double_quoted_keyword = double_quoted_word
        try:
            # Simulate pressing the Escape key
            body_element = driver.find_element("tag name", "body")
            body_element.send_keys(Keys.ESCAPE)
        except:
            pass

        current_url = driver.current_url
        print(current_url)
        html_code = driver.page_source


        # id, name, type, class_name, place_holder, value = find_input_textarea(html_code, keyword)
        key_name, value_name = find_input_textarea(html_code, keyword, double_quoted_keyword)
        last_tag_value.append(key_name)
        last_tag_value.append(value_name)
        print('key_name:', key_name, 'value_name:', value_name)
        # Define the wait time in seconds
        wait = WebDriverWait(driver, 20)
        element = ''
        # Wait until the element with the specified ID is clickable
        if key_name == 'id':
            try:
                with contextlib.suppress(NoSuchElementException):
                    element = wait.until(EC.element_to_be_clickable((By.ID, value_name)))
                    print('ID Executed')
            except NoSuchElementException:
                pass

        elif key_name == 'name':
            try:
                with contextlib.suppress(NoSuchElementException):
                    element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@{key_name}="{value_name}"]')))
                    # element = wait.until(EC.element_to_be_clickable((By.NAME, value_name)))
                    print('Name Executed')
            except NoSuchElementException:
                pass
        elif key_name == 'type':
            try:
                with contextlib.suppress(NoSuchElementException):
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[type={value_name}]")))
                    print('Type Executed')
            except NoSuchElementException:
                pass
        elif key_name == 'class':
            try:
                with contextlib.suppress(NoSuchElementException):
                    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, value_name)))
                    print('class name Executed')
            except NoSuchElementException:
                pass
        elif key_name == 'placeholder':
            try:
                with contextlib.suppress(NoSuchElementException):
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"[placeholder='{value_name}']")))
                    print('place holder executed')
            except NoSuchElementException:
                pass
        elif key_name == 'value':
            try:
                with contextlib.suppress(NoSuchElementException):
                    element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"[value='{value_name}']")))
                    print('value executed')
            except NoSuchElementException:
                pass
        else:
            try:
                with contextlib.suppress(NoSuchElementException):
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[{key_name}='{value_name}']")))
                    print(f"{key_name} executed")
            except NoSuchElementException:
                pass




        # Set the implicit wait time to 10 seconds
        # try:
        #     # element.click()
        #     # Simulate pressing the down arrow key
        # except:
        #     pass
        # typing_speed = 0.1
        # for char in double_quoted_keyword:
        #     ActionChains(driver).pause(typing_speed).send_keys(char).perform()
        element.send_keys(double_quoted_keyword)
        print('keyword:',keyword)
        if 'location' in keyword.lower():
            try:
                time.sleep(3)
                element.send_keys(Keys.TAB, Keys.ENTER)
            except:
                pass

        # if 'search' or 'Search' in double_quoted_keyword:
        #     element.click()
        time.sleep(10)
        logging.info("Insert functionality complted Successfully")
        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
        # element.send_keys(Keys.RETURN)
        # except:
        #     print('send keys not working')

    except:
        logging.info("Insert functionality Failed")
        take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')


def icon_search_function(driver):
    html_code = driver.page_source
    prettified_html = pretty_code(html_code)
    # Find all elements that contain the word "search" in attributes or attribute values
    search_elements = prettified_html.find_all(lambda tag: any("search" in value.lower() for value in tag.attrs.values()))



def hover_function(driver, url, keyword, id, each_step_no, prediction):
    try:
        try:
            alert = Alert(driver)
            alert.accept()  # Use .dismiss() to click "Cancel" if needed
        except:
            # If there is no alert, an exception will be raised (no need to handle it)
            pass
        # Check if a new tab has been opened
        if len(driver.window_handles) > 1:
            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])

        try:
            # Simulate pressing the Escape key
            body_element = driver.find_element("tag name", "body")
            body_element.send_keys(Keys.ESCAPE)
        except:
            pass

        keyword = keyword.replace('"', '')
        print('keyword:', keyword)
        print('Hover Functionality Triggered')
        url = driver.current_url
        html_code = driver.page_source
        prettified_html = pretty_code(html_code)
        original_xpath = find_element(prettified_html, str(keyword).strip(), None)

        # original_xpath = find_element(prettified_html,keyword,None)
        print('full_Xpath: ', original_xpath)
        final_xpath = mod_xpath(original_xpath)
        print('final_xpath:', final_xpath)

        for i in final_xpath:
            try:
                # Wait for the keyword element to appear
                dropdown = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, i)))

                # Create an instance of ActionChains
                actions = ActionChains(driver)

                # Move the mouse cursor to the element to hover over it
                actions.move_to_element(dropdown).perform()

                time.sleep(5)
                logging.info("Hover functionality complted Successfully")
            except:
                pass
        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
        # # Continue with other actions after hovering
        # # For example, you can click on a sub-element of the hovered element
        # sub_element = driver.find_element_by_xpath("sub_element_xpath")
        # actions.move_to_element(sub_element).click().perform()
    except:
        logging.info("Hover functionality Failed")
        take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')


def keyword_variation(string):
    string = string.strip()
    lowercase_string = string.lower()
    variations = [
        lowercase_string,
        lowercase_string.title(),
        lowercase_string.capitalize(),
        string.upper()
    ]

    # Generate variations with "sign-in" if the string contains a space
    if ' ' in string:
        variations += [
            string.replace(' ', '-'),
            string.replace(' ', '-').title(),
            string.replace(' ', '-').capitalize(),
            string.replace(' ', '-').upper()
        ]

    elif string == 'username':
        variations += [
            'user-name', 'User-name', 'User-Name', 'user_name', 'User_name', 'User_Name']
    elif string == 'password':
        variations += [
            'pass-word', 'Pass-word', 'Pass-Word', 'pass_word', 'Pass_word', 'Pass_word']

    return variations


from bs4 import BeautifulSoup, NavigableString


def process_xpath(xpath):
    # Remove "/None[1]" from the xpath
    xpath = xpath.replace("/None[1]", "")

    # Remove the indexing "[1]" from each element except the last one
    xpath_parts = xpath.split('/')
    xpath_parts = [part.split('[')[0] for part in xpath_parts[:-1]]

    # Add back the indexing for the last element if it is not empty
    last_part = xpath_parts[-1].split('[')[0]
    if last_part:
        xpath_parts[-1] = last_part

    # Reconstruct the modified xpath
    modified_xpath = '/'.join(xpath_parts)

    return modified_xpath


# def find_element(html_code, target, sub_text=None):
#     soup = BeautifulSoup(html_code, 'html.parser')
#     target_elements = soup.find_all(text=lambda text: target in text.strip())
#
#     if not target_elements:
#         return ["Element not found."]
#
#     paths = []
#     for target_element in target_elements:
#         path = []
#         current = target_element
#         while current.parent:
#             tag = current.name
#             index = sum(1 for sibling in current.previous_siblings if sibling.name == tag) + 1
#             path.insert(0, f"{tag}[{index}]")
#             current = current.parent
#
#         if sub_text:
#             div_element = target_element.find_parent('div')
#             if div_element:
#                 parent_div_element = div_element.find_parent('div')
#                 if parent_div_element and sub_text in parent_div_element.get_text():
#                     paths.append(path)
#             else:
#                 direct_parent_div = target_element.find_parent('div')
#                 if direct_parent_div and sub_text in direct_parent_div.get_text():
#                     paths.append(path)
#         else:
#             paths.append(path)
#
#     if not paths:
#         return ["Element not found."]
#
#     return paths


# def find_element(html_code, target, sub_text=None):
#     soup = BeautifulSoup(html_code, 'html.parser')
#     target_elements = soup.find_all(text=lambda text: target in text.strip())
#
#     if not target_elements:
#         return ["Element not found."]
#
#     paths = []
#     for target_element in target_elements:
#         path = []
#         current = target_element
#         while current.parent:
#             tag = current.name
#             index = sum(1 for sibling in current.previous_siblings if sibling.name == tag) + 1
#             path.insert(0, f"{tag}[{index}]")
#             current = current.parent
#
#         if sub_text:
#             div_element = target_element.find_parent('div')
#             if div_element:
#                 parent_div_element = div_element.find_parent('div')
#                 if parent_div_element:
#                     parent_text = parent_div_element.get_text()
#                     if all(keyword in parent_text for keyword in sub_text.split()):
#                         paths.append(path)
#             else:
#                 direct_parent_div = target_element.find_parent('div')
#                 if direct_parent_div:
#                     parent_text = direct_parent_div.get_text()
#                     if all(keyword in parent_text for keyword in sub_text.split()):
#                         paths.append(path)
#         else:
#             paths.append(path)
#
#     if not paths:
#         return ["Element not found."]
#
#     return paths

def find_element(html_code, target, sub_text=None):
    soup = BeautifulSoup(html_code, 'html.parser')
    target_elements = soup.find_all(
        text=lambda text: target.lower() in text.strip().lower() if isinstance(text, str) else False)
    # print('target_elements outer:', target_elements)
    if not target_elements:
        target_elements = soup.find(
            text=lambda text: target.lower() in text.strip().lower() if isinstance(text, str) else False)
        # print('target_elements inner:', target_elements)
        if not target_elements:
            return ["Element not found."]

    paths = []
    for target_element in target_elements:
        path = []
        current = target_element
        while current.parent:
            tag = current.name
            index = sum(1 for sibling in current.previous_siblings if sibling.name == tag) + 1
            path.insert(0, f"{tag}[{index}]")
            current = current.parent

        if sub_text:
            div_element = target_element.find_parent('div')
            if div_element:
                parent_div_element = div_element.find_parent('div')
                if parent_div_element:
                    parent_text = parent_div_element.get_text(separator=' ')
                    if all(keyword.lower() in parent_text.lower() for keyword in sub_text.split()):
                        paths.append(path)
            else:
                direct_parent_div = target_element.find_parent('div')
                if direct_parent_div:
                    parent_text = direct_parent_div.get_text(separator=' ')
                    if all(keyword.lower() in parent_text.lower() for keyword in sub_text.split()):
                        paths.append(path)
        else:
            paths.append(path)

    print('paths list:',paths)

    if not paths:
        return ["Element not found."]
    # paths = [item for item in paths if not re.match(r'.*(script|style)\[\d+\]$', item) and item != 'html/head/style' and item != 'html/head/script']
    # Remove elements that match the given XPath pattern and have sub-elements

    return paths


def mod_xpath(output):
    results = []
    for i in output:
        print('i:', i)
        # Remove '[1]' only if it appears at the end of each element
        x = [element.replace('[1]', '') if element.endswith('[1]') else element for element in i]

        # Remove 'None' element from the list
        x = [element for element in x if element != 'None']

        result = "/".join(x)
        if '/None' in result:
            processed_selector = result.split('/None')[0]
            results.append(processed_selector)
        else:
            results.append(result)
    print('results:',results)
    # Remove elements with 'html/head/style[index]' pattern
    updated_list = remove_elements_with_pattern(results, r'html/head/(style|script)\[\d+\]')

    print('filtered_xpaths:', updated_list)
    return updated_list


def pretty_code(html_code):
    import requests
    from bs4 import BeautifulSoup

    # # Send a GET request to the URL
    # response = requests.get(url)
    #
    # # Get the HTML content from the response
    # html_content = response.text

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_code, "html.parser")

    # Prettify the HTML code
    prettified_html = soup.prettify()

    return prettified_html





# Function to check if an XPath has format of 'html/body/style[index] or 'html/body/script[index]
def remove_elements_with_pattern(lst, pattern):
    filtered_list = [elem for elem in lst if not re.match(pattern, elem)]
    return filtered_list

