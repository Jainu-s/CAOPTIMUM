import contextlib
import datetime
import math
import random
import time
import re
import sys

import execjs
import nltk

sys.path.insert(1,r'C:\Users\abdul\PycharmProjects\Project TWIC')
import main

import editdistance
import math
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from delelte_later import find_input_textarea
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium_stealth import stealth
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
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException, \
    WebDriverException
from nlp_pattern_identifier import extract_button_and_item_from_string
from collections import defaultdict
import os
import pyautogui
import logging
from lxml import etree
import math
import pickle
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from PIL import Image
import pytesseract
from Config.config import extract_text_from_image
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')


# Set up logging
from Logs.logger_config import setup_logging
import logging



SPass_path = r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot\Test Case Passed'
SFail_path = r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot\Test Case Failed'
sleep_time = 3

# Temporary Xpath for Victoria Secret
account_xpath = '/html/body/div[2]/header/nav[1]/div[2]/ul/li[1]/div/a/div'
cart_bag_xpath = '/html/body/div[2]/header/nav[1]/div[2]/ul/li[2]/div/a/div'
checkout_xpath =  '/html/body/reach-portal/div[3]/div/section/div[4]/div/div/div/article/div/div[2]/button'
accept_continue = '//*[@id="buttons-aurus-overlay"]/div[2]/div[2]/button'
signin_xpath = '/html/body/reach-portal/div[3]/div/section/div[4]/div/div/div/article/div/div[1]/div[1]/a/span'
search_xpath = '/html/body/div[2]/header/div[2]/div/span/input'
close_xpath = '/html/body/reach-portal/div[3]/div/section/div[4]/div/header/button/div'
# check_box = '/html/body/div[2]/main/div/div/div/form/fieldset/span[5]/label/div'
check_box = '/html/body/esw-root/div/main/esw-checkout/esw-checkout-accordion/div/div[1]/esw-shipping-accordion/div[2]/form/esw-gdpr-consent/div/esw-checkbox/div'



def random_delay(min_seconds=2, max_seconds=5):
    time.sleep(random.uniform(min_seconds, max_seconds))

def random_mouse_movement():
    x, y = pyautogui.position()
    pyautogui.moveTo(x + random.randint(-100, 100), y + random.randint(-100, 100), duration=0.5)

def set_random_window_size(driver, width_range=(1024, 1920), height_range=(768, 1080)):
    width = random.randint(*width_range)
    height = random.randint(*height_range)
    driver.set_window_size(width, height)

def apply_driver_tweaks(driver):
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
            })
        """
    })

def take_screenshot(base_folder, test_case, filename=None, driver=None):
    try:
        # Create the subfolder for the current test case
        folder = os.path.join(base_folder, test_case)
        if not os.path.exists(folder):
            os.makedirs(folder)

        # If filename is not provided, generate one based on timestamp
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        # Take a screenshot and save it
        screenshot_path = os.path.join(folder, filename)
        pyautogui.screenshot().save(screenshot_path)

        # Save the HTML source if driver is provided
        if driver:
            html_filename = os.path.splitext(filename)[0] + ".html"  # Convert the filename to .html extension
            html_file_path = os.path.join(folder, html_filename)
            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)

    except Exception as e:
        logging.error(f"Failed to take screenshot: {str(e)}")


# def take_screenshot(base_folder, test_case, filename=None,driver=None):
#     try:
#         # Create the subfolder for the current test case
#         folder = os.path.join(base_folder, test_case)
#         if not os.path.exists(folder):
#             os.makedirs(folder)
#
#         screenshot = pyautogui.screenshot()
#         file_path = os.path.join(folder, filename)
#         screenshot.save(file_path)
#
#         html_code = driver.page_source
#         with open(f'{file_path}/{test_case}.html', 'w', encoding='utf-8') as f:
#             f.write(html_code)
#     except Exception as e:
#         logging.error(f"Failed to take screenshot: {str(e)}")

def previous_function(driver, url, text,id,each_step_no,prediction):
    try:
        driver.back()
        driver.refresh()
        logging.info("Back to Page Functionality Successful")
        time.sleep(sleep_time)
        take_screenshot(SPass_path,id,'successful.png',driver)
    except:
        logging.info("Back to Page Functionality Failed")
        take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')
        



def browser_function(id, each_step_no, prediction):
    #try:
    print('Browser Functionality Triggered')

    chrome_options = ChromeOptions()
    # chrome_options.accept_untrusted_certs = True
    chrome_options.add_extension(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Chrome Extensions\extension_1_0_1_0.crx')
    # chrome_options.add_extension(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Chrome Extensions\cookies_blocker_extension_1_7_0_0.crx')
    chrome_options.add_extension(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Chrome Extensions\popup_block_extension_0_6_6_0.crx')
    # # chrome_options.add_extension(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\All Files\extension_1_0_1_0.crx')
    # referer_url = "https://www.google.co.in"
    # chrome_options.add_argument(f"--referer={referer_url}")
    # # chrome_options.headless = True
    # chrome_options.add_argument("start-maximized")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--ignore-ssl-errors')
    # chrome_options.add_argument('--allow-insecure-localhost')
    # caps = chrome_options.to_capabilities()
    # caps["acceptInsecureCerts"] = True
    # chrome_options.add_argument('--disable-web-security')
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument("--disable-application-cache")
    # chrome_options.add_argument("--disable-cache")
    # chrome_options.add_argument("--disk-cache-size=0")
    # chrome_options.add_argument("--disable-blink-features")
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--disable-popup-blocking")
    # chrome_options.add_argument("--enable-javascript")
    # prefs = {"profile.default_content_setting_values.notifications": 2}
    # chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path=r'C:\Users\abdul\PycharmProjects\Automation_Optimum\chrome webdriver\chromedriver.exe',options=chrome_options)
    #driver = webdriver.Chrome(executable_path=r'C:\Users\abdul\PycharmProjects\Automation_Optimum\chrome webdriver\chromedriver.exe')
    # apply_driver_tweaks(driver)
    # set_random_window_size(driver)
    # random_mouse_movement()
    #
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    #
    # chrome_options.add_argument(f"user-agent={user_agent}")

    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    #     "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
    # })
    # print(driver.execute_script("return navigator.userAgent;"))

    # stealth(driver = driver,
    #         user_agent = user_agent,
    #         languages=["en-US", "en"],
    #         vendor="Google Inc.",
    #         platform="Win32",
    #         webgl_vendor="Intel Inc.",
    #         renderer="Intel Iris OpenGL Engine",
    #         fix_hairline=True,
    #         )


    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Store the initial window handle (current tab)
    initial_window_handle = driver.current_window_handle
    logging.info("Browser Functionality Completed")
    time.sleep(sleep_time)
    take_screenshot(SPass_path,id,'successful.png',driver)
    print('browser driver:',driver)
    return driver
    # except:
    #     logging.info("Browser Functionality Failed")
    #     take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')
        


def url_function(driver, url, id, each_step_no, prediction):
    try:
        if driver:
            print('URL Functionality Triggered')
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.implicitly_wait(20)
            driver.get(url)
            cookies = driver.get_cookies()
            logging.info("URL Opened Successfully")
            take_screenshot(SPass_path,id,'successful.png',driver)
            driver.maximize_window()
            # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
            print('if driver in url:',driver)
            return driver
        else:
            driver = browser_function(id, each_step_no, prediction)
            print('Else URL Functionality Triggered')
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            driver.implicitly_wait(20)
            driver.get(url)
            driver.maximize_window()
            logging.info("URL Opened Successfully")
            take_screenshot(SPass_path,id,'successful.png',driver)
            print('else driver in url:', driver)
            # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
            return driver
    except:
        logging.info("URL Open Failed")
        take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')
        



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
        take_screenshot(SPass_path,id,'successful.png',driver)
        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
        time.sleep(5)
        return driver.curent_url
    except:
        logging.info("Browser Searching Failed")
        take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')
        


def handle_alert(driver):
    try:
        alert = driver.switch_to.alert
        alert.accept()
        logging.info('Alert Popup')
    except:
        pass


def click_function(driver, clickable_url, keyword, id, each_step_no, prediction):
    screenshot_folder = 'screenshot_comp/'
    clean_screenshot_comp()
    screenshot_name1 = f'screenshot_before.png'
    driver.save_screenshot(os.path.join(screenshot_folder, screenshot_name1))

    # Get the list of window handles
    window_handles = driver.window_handles

    # Check if there are at least two windows open
    if len(window_handles) >= 2:
        # Switch to the new window
        new_window_handle = window_handles[-1]
        driver.switch_to.window(new_window_handle)
        print("Switched to the new window.")
    else:
        print("There are not enough windows open.")

    time.sleep(2)

    try:
        button, item = extract_button_and_item_from_string(keyword)
        print('Button:', button, 'item:', item)
    except:
        button = re.findall(r'["\'](.*?)["\']', keyword)
        item = keyword


    print('keyword:',keyword)

    # Identify distance between two words apply click functionality
    def compute_distance(location1, location2):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((location1['x'] - location2['x']) ** 2 + (location1['y'] - location2['y']) ** 2)

    def generate_bigrams(text):
        """Generate bigrams from a given text."""
        words = text.split()
        return [' '.join(words[i:i + 2]) for i in range(len(words) - 1)]

    def click_nearest_target_to_sub_text(target_text, sub_text=None):

        print('started -----------------------------------------------------------------')
        wait = WebDriverWait(driver, 30)
        sub_location = None

        # If sub_text is provided, generate its bigrams
        if sub_text:
            bigrams = generate_bigrams(sub_text)

            matching_elements = []
            for bigram in bigrams:
                # Find potential elements that might contain the bigram
                potential_sub_elements = wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, f"//*[contains(text(), '{bigram}')]")))

                # Filter elements to check if they contain the whole bigram
                matching_elements.extend([elem for elem in potential_sub_elements if bigram in elem.text])

            if matching_elements:
                # Here we're choosing the first match from the bigrams
                sub_element = matching_elements[0]
                sub_location = sub_element.location

        # Wait until at least one target_text element is present
        wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{target_text}')]")))
        target_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{target_text}')]")
        if not target_elements:
            print("No target elements found!")
            return

        if sub_location:
            nearest_element = min(target_elements, key=lambda elem: compute_distance(elem.location, sub_location))
        else:
            # If no sub_location (either not provided or not found), simply click on the first target_text found
            nearest_element = target_elements[0]

        nearest_element.click()
        time.sleep(2)

    # def click(click_word):
    #
    #     # Word to search for and click on
    #     word_to_search = click_word
    #
    #     # JavaScript code to search for the word and click on it
    #     script = f'''
    #         var wordToSearch = "{word_to_search}";
    #         var found = false;
    #         var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    #
    #         while (walker.nextNode()) {{
    #             var node = walker.currentNode;
    #             if (node.textContent.includes(wordToSearch)) {{
    #                 found = true;
    #                 node.parentElement.click(); // Click on the parent element containing the word
    #                 break;
    #             }}
    #         }}
    #
    #         return found;
    #     '''
    #
    #     # Execute the JavaScript code in the browser
    #     is_word_found = driver.execute_script(script)
    #
    #     if is_word_found:
    #         print(f"Clicked on the word '{word_to_search}' in the DOM.")
    #         return driver
    #     else:
    #         print(f"The word '{word_to_search}' was not found in the DOM.")

    def click(click_word):
        try:
            # Word to search for and click on
            word_to_search = click_word

            # JavaScript code to search for the word and click on it
            script = f'''
                var wordToSearch = "{word_to_search}";
                var found = false;
                var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);

                while (walker.nextNode()) {{
                    var node = walker.currentNode;
                    if (node.textContent.includes(wordToSearch)) {{
                        found = true;
                        node.parentElement.click(); // Click on the parent element containing the word
                        break;
                    }}
                }}

                return found;
            '''

            # Execute the JavaScript code in the browser
            is_word_found = driver.execute_script(script)

            if is_word_found:
                print(f"Clicked on the word '{word_to_search}' in the DOM.")
                return driver
            else:
                print(f"The word '{word_to_search}' was not found in the DOM.")

        except Exception as e:
            print(f"An error occurred: {e}")



    def javascript_click(click_word, nearby=None):

        # Convert click_word and nearby to lowercase
        click_word_lower = click_word.lower()
        nearby_lower = nearby.lower() if nearby else ""

        # JavaScript code to search for the click_word (case-insensitive)
        # and find the closest clickable parent element to the nearby word
        script = f'''
            var clickWord = "{click_word_lower}";
            var nearbyWord = "{nearby_lower}";
            var closestDistance = Number.MAX_VALUE;
            var closestElement = null;

            var elements = document.querySelectorAll('*');
            elements.forEach(function(element) {{
                var textContentLower = element.textContent.toLowerCase();
                if (textContentLower.includes(clickWord)) {{
                    var nearbyIndex = textContentLower.indexOf(nearbyWord);
                    if (nearbyIndex !== -1) {{
                        var distance = Math.abs(textContentLower.indexOf(clickWord) - nearbyIndex);
                        if (distance < closestDistance && isClickable(element)) {{
                            closestDistance = distance;
                            closestElement = element;
                        }}
                    }}
                }}
            }});

            if (closestElement) {{
                closestElement.click();
                return true;
            }} else {{
                return false;
            }}

            function isClickable(element) {{
                return (element.tagName.toLowerCase() === 'a' || element.tagName.toLowerCase() === 'button');
            }}
        '''

        # Execute the JavaScript code in the browser
        is_word_found = driver.execute_script(script)

        if is_word_found:
            print(
                f"Clicked on the closest '{click_word}' (case-insensitive) to '{nearby}' that is clickable in the DOM.")
        else:
            print(f"No clickable '{click_word}' (case-insensitive) was found in the DOM.")

    # def javascript_click(click_word, nearby=None):
    #
    #     if nearby is None:
    #         click(click_word)
    #     else:
    #
    #         # Word to search for and click on (converted to lowercase)
    #         word_to_search = click_word.lower()  # Convert the search word to lowercase
    #         nearby_lower = nearby.lower() if nearby else ""
    #
    #         # JavaScript code to search for the word (case-insensitive) and click on the closest clickable parent element
    #         script = f'''
    #             var wordToSearch = "{word_to_search}";
    #             var nearbyWord = "{nearby_lower}";
    #             var found = false;
    #             var closestDistance = Number.MAX_VALUE; // Initialize closest distance as a very large number
    #             var closestElement = null;
    #
    #             var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    #
    #             while (walker.nextNode()) {{
    #                 var node = walker.currentNode;
    #                 var textContentLower = node.textContent.toLowerCase();  // Convert text content to lowercase
    #                 if (textContentLower.includes(wordToSearch) && textContentLower.includes(nearbyWord)) {{
    #                     var parentElement = node.parentElement;
    #                     while (parentElement) {{
    #                         if (isClickable(parentElement)) {{
    #                             var distance = Math.abs(textContentLower.indexOf(wordToSearch) - textContentLower.indexOf(nearbyWord));
    #                             if (distance < closestDistance) {{
    #                                 closestDistance = distance;
    #                                 closestElement = parentElement;
    #                             }}
    #                             found = true;
    #                             break;
    #                         }}
    #                         parentElement = parentElement.parentElement;
    #                     }}
    #                 }}
    #                 if (found) {{
    #                     break;
    #                 }}
    #             }}
    #
    #             if (closestElement) {{
    #                 closestElement.click(); // Click on the closest clickable parent element
    #                 return true;
    #             }} else {{
    #                 return false;
    #             }}
    #
    #             function isClickable(element) {{
    #                 return (element.tagName.toLowerCase() === 'a' || element.tagName.toLowerCase() === 'button');
    #             }}
    #         '''
    #
    #         # Execute the JavaScript code in the browser
    #         is_word_found = driver.execute_script(script)
    #
    #         if is_word_found:
    #             print(
    #                 f"Clicked on the closest '{click_word}' (case-insensitive) to '{nearby}' that is clickable in the DOM.")
    #             return driver
    #         else:
    #             print(f"No clickable '{click_word}' (case-insensitive) was found in the DOM.")

    def click_single_element(button):
        print(f"Click - All Triggered for '{button}'")

        # Find all elements with the specified text, making it not case-sensitive
        target_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{button.lower()}')]")))

        # for element in target_elements:
        #     driver.execute_script("arguments[0].scrollIntoView();", element)
        #
        #     element.click()

        for element in target_elements:
            element.click()

    def click_single_element2(button):
        print(f"Click - 2 (All) Triggered for '{button}'")

        # Find all elements with the specified text, making it not case-sensitive
        xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{button.lower()}')]"

        target_elements2 = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))

        # for element in target_elements2:
        #     driver.execute_script("arguments[0].scrollIntoView();", element)
        #
        #     element.click()

        for element in target_elements2:
            element.click()


    def find_link_by_attribute_value(html_source, button):
        soup = BeautifulSoup(html_source, 'html.parser')
        for link in soup.find_all('a'):
            for key, value in link.attrs.items():
                if button == value:
                    return link
        return None

    def overlayed_click(button):
        # Find all elements with the text "Login"
        login_elements = driver.find_elements(By.XPATH, f"//*[text()={button}]")

        # Iterate through the elements
        for element in login_elements:
            try:
                # Scroll the element into view
                driver.execute_script("arguments[0].scrollIntoView();", element)

                # Click the "Login" element
                element.click()
            except:
                pass






    def click_single_xpath(xpath):
        target_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,xpath)))
        target_element.click()
        take_screenshot(SPass_path, id, 'successful.png', driver)
        logging.info('Click Functionality Successful')
        time.sleep(2)





    # try:
    button_len = 0

    checkout = 'checkout'
    accept_continue = 'ACCEPT & CONTINUE'
    user = 'user'
    bag = 'bag'
    search = 'search'
    delete = 'delete'


    if (button is not None and 'checkout' in button) or 'CHECKOUT' in item.lower():
        print('CHECKOUT Triggered')
        try:
            click_single_xpath(checkout_xpath)
        except:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')

    elif (button is not None and 'accept & continue' in button) or 'ACCEPT & CONTINUE' in item.lower():
        print('ACCEPT & CONTINUE Triggered')
        try:
            click_single_xpath(accept_continue)
        except:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')

    elif (button is not None and 'user' in button) or 'user' in item.lower():
        print('user Triggered')
        try:
            click_single_xpath(account_xpath)
        except:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')

    elif (button is not None and 'bag' in button) or 'bag' in item.lower():
        print('bag Triggered')
        try:
            click_single_xpath(cart_bag_xpath)
        except:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')

    elif (button is not None and 'search' in button) or 'search' in item.lower():
        print('search Triggered')
        try:
            click_single_xpath(search_xpath)
        except:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')

    elif (button is not None and 'delete' in button) or 'delete' in item.lower():
        print('delete Triggered')
        try:
            click_single_xpath(close_xpath)
        except:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')

    elif (button is not None and 'close' in button) or 'close' in item.lower():
        print('Close Triggered')
        try:
            click_single_xpath(close_xpath)
        except:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')

    elif (button is not None and 'checkbox' in button) or 'checkbox' in item.lower():
        print('Check Box Triggered')
        try:
            click_single_xpath(check_box)
        except:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')



    elif button_len < 10:
        print('Buttons > 1 started')

        try:
            click_single_element(button)
            time.sleep(sleep_time)
            take_screenshot(SPass_path, id, 'successful.png', driver)
            logging.info('Click Functionality Successful')

            # overlayed_click(button)
            # time.sleep(sleep_time)
            # take_screenshot(SPass_path, id, 'successful.png', driver)
            # logging.info('Click Functionality Successful')

        except:
            html_source = driver.page_source

            matched_link = find_link_by_attribute_value(html_source, button)

            if matched_link:
                print(f"Found link: {matched_link}")
                # To click the link using Selenium, you might need to find it again using its attributes.
                href_value = matched_link.attrs.get('href', '')
                link_to_click = driver.find_element(By.CSS_SELECTOR, f"a[href='{href_value}']")
                link_to_click.click()
            else:
                print(f"No link found with any attribute containing the text: {button}")
                try:
                    click_single_element2(button)
                    time.sleep(sleep_time)
                    take_screenshot(SPass_path, id, 'successful.png', driver)
                    logging.info('Click Functionality Successful')
                except:
                    try:
                        overlayed_click(button)
                        time.sleep(sleep_time)
                        take_screenshot(SPass_path, id, 'successful.png', driver)
                        logging.info('Click Functionality Successful')
                    except:

                        try:
                            javascript_click(button)
                            time.sleep(sleep_time)
                            take_screenshot(SPass_path, id, 'successful.png', driver)
                            logging.info('Click Functionality Successful')

                        except:
                            logging.info("Click Funtionality Failed")
                            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')





    else:
        logging.info("Click Funtionality Failed")
        take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')


    # except:
    #     logging.info("Click Funtionality Failed")
    #     take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')





last_tag_value = []




# def insert_function(driver, url, keyword, id, each_step_no, prediction):
#     # Extract the double-quoted word
#     double_quoted_word = re.search(r'"([^"]*)"', keyword).group(1)
#
#     # Extract the rest of the words
#     desired_value = re.sub(fr'"{double_quoted_word}"', '', keyword).split()
#
#     wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
#
#     input_elements = []
#     for word in desired_value:
#         print('word:', word)
#         # Wait for input elements with attributes matching the desired value
#         try:
#             input_elements = wait.until(
#                 EC.presence_of_all_elements_located((By.XPATH, f'//input[@*="{word}"]'))
#             )
#
#         except:
#             pass
#
#     print('Input Elements:', input_elements)
#
#     # Loop through the input elements
#     for input_element in input_elements:
#         print('Input Element:', input_element)
#         # Get all attributes of the input element
#         attributes = input_element.get_attribute('outerHTML')
#
#         # Split the attributes into key-value pairs
#         attribute_pairs = [pair.split('=') for pair in attributes.split(' ')]
#         print('Attribute_pairs:', attribute_pairs)
#
#         # Iterate through the attribute pairs
#         for attribute_pair in attribute_pairs:
#             # Check if the attribute's value matches the desired value
#             if len(attribute_pair) == 2 and attribute_pair[1].strip('\'"') in desired_value:
#                 # Insert text into the input element
#                 input_element.send_keys(double_quoted_word)
#                 break  # Break the inner loop once a match is found




# def insert_function(driver, url, keyword, id, each_step_no, prediction):
#
#     stopwords_list = set(stopwords.words('english'))
#
#     # Extract the double-quoted word
#     double_quoted_word = re.search(r'"([^"]*)"', keyword).group(1)
#
#     # Extract the rest of the words and remove stopwords
#     desired_value = re.sub(fr'"{double_quoted_word}"', '', keyword).split()
#     desired_value = [word for word in desired_value if word.lower() not in stopwords_list]
#
#     wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
#
#     input_elements = []
#     for word in desired_value:
#         print('word:', word)
#         # Wait for input elements with attributes matching the desired value
#         try:
#             input_elements = wait.until(
#                 EC.presence_of_all_elements_located((By.XPATH, f'//input[@*="{word}"]'))
#             )
#
#         except:
#             pass
#
#     print('Input Elements:', input_elements)
#
#     # Loop through the input elements
#     for input_element in input_elements:
#         print('Input Element:', input_element)
#         # Get all attributes of the input element
#         attributes = input_element.get_attribute('outerHTML')
#         print('attributes:',attributes)
#
#         # Split the attributes into key-value pairs
#         attribute_pairs = [pair.split('=') for pair in attributes.split(' ')]
#         print('Attribute_pairs:', attribute_pairs)
#
#         # Iterate through the attribute pairs
#         for attribute_pair in attribute_pairs:
#             # Check if the attribute's value matches the desired value
#             if len(attribute_pair) == 2 and attribute_pair[1].strip('\'"') in desired_value:
#                 # Insert text into the input element
#                 input_element.send_keys(double_quoted_word)
#                 break  # Break the inner loop once a match is found


def remove_hidden_inputs(input_tags):
    filtered_tags = []
    for tag in input_tags:
        if 'style="display: none"' not in str(tag):
            filtered_tags.append(tag)
    return filtered_tags

# def insert_function(driver, url, keyword, id, each_step_no, prediction):
#
#     stopwords_list = set(stopwords.words('english'))
#
#     # Extract the double-quoted word
#     double_quoted_word = re.search(r'"([^"]*)"', keyword).group(1)
#
#     # Extract the rest of the words and remove stopwords
#     desired_value = re.sub(fr'"{double_quoted_word}"', '', keyword).split()
#     desired_value = [word for word in desired_value if word.lower() not in stopwords_list]
#
#     wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
#
#     # Find all input elements on the page
#     input_elements = driver.find_elements(By.XPATH, '//input')
#
#     print('Input Elements Before Removing:', len(input_elements))
#
#     # Remove hidden input elements
#     input_elements = remove_hidden_inputs(input_elements)
#
#     print('Input Elements After Removing:',len(input_elements))
#
#     for input_element in input_elements:
#         # Get all attributes of the input element
#         attributes = input_element.get_attribute('outerHTML')
#
#         # Split the attributes into key-value pairs
#         attribute_pairs = [pair.split('=') for pair in attributes.split(' ')]
#
#         # Check if any attribute's value matches the desired value in a case-insensitive manner
#         for attribute_pair in attribute_pairs:
#             # if len(attribute_pair) == 2 and attribute_pair[1].strip('\'"').lower() in [word.lower() for word in
#             #                                                                            desired_value]:
#
#             if len(attribute_pair) == 2:
#                 attribute_value = attribute_pair[1].strip('\'"').lower()  # Clean and lowercase attribute value
#                 for word in desired_value:
#                     if word.lower() in attribute_value:
#                         # Insert text into the input element
#                         input_element.send_keys(double_quoted_word)
#                         break  # Break the loop once a match is found
#                 # # Insert text into the input element
#                 # input_element.send_keys(double_quoted_word)
#                 # break  # Break the inner loop once a match is found

def insert_function(driver, url, keyword, id, each_step_no, prediction):
    stopwords_list = set(stopwords.words('english'))
    double_quoted_word = re.search(r'"([^"]*)"', keyword).group(1)
    desired_value = re.sub(fr'"{double_quoted_word}"', '', keyword).split()
    desired_value = set(word.lower() for word in desired_value if word.lower() not in stopwords_list)

    wait = WebDriverWait(driver, 10)
    input_elements = driver.find_elements(By.XPATH, '//input')
    print('Input Elements Before Removing:', len(input_elements))
    input_elements = remove_hidden_inputs(input_elements)
    print('Input Elements After Removing:', len(input_elements))

    for input_element in input_elements:
        attributes = input_element.get_attribute('outerHTML')
        attribute_pairs = [pair.split('=') for pair in attributes.split(' ')]
        attribute_values = {pair[0]: pair[1].strip('\'"').lower() for pair in attribute_pairs if len(pair) == 2}

        if any(word in attribute_values.values() for word in desired_value):
            input_element.send_keys(double_quoted_word)
            # You may want to add a break here if you only want to insert the word into the first matching input element.









def icon_search_function(driver):
    html_code = driver.page_source
    prettified_html = pretty_code(html_code)
    # Find all elements that contain the word "search" in attributes or attribute values
    search_elements = prettified_html.find_all(lambda tag: any("search" in value.lower() for value in tag.attrs.values()))



def hover_function(driver, url, keyword, id, each_step_no, prediction):
    button, item = extract_button_and_item_from_string(keyword)

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

        try:
            if 'user' in button:
                # Wait for the keyword element to appear
                dropdown = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, account_xpath)))

                # Create an instance of ActionChains
                actions = ActionChains(driver)

                # Move the mouse cursor to the element to hover over it
                actions.move_to_element(dropdown).perform()

                logging.info("Hover functionality complted Successfully")
                time.sleep(sleep_time)
                take_screenshot(SPass_path, id, 'successful.png', driver)
        except:
            pass

        # url = driver.current_url
        # html_code = driver.page_source
        # prettified_html = pretty_code(html_code)
        # original_xpath = find_element(prettified_html, str(keyword).strip(), None)
        #
        # # original_xpath = find_element(prettified_html,keyword,None)
        # print('full_Xpath: ', original_xpath)
        # final_xpath = mod_xpath(original_xpath)
        # print('final_xpath:', final_xpath)
        #
        #
        # try:
        #     # Wait for the keyword element to appear
        #     dropdown = WebDriverWait(driver, 20).until(
        #         EC.element_to_be_clickable((By.XPATH, button)))
        #
        #     # Create an instance of ActionChains
        #     actions = ActionChains(driver)
        #
        #     # Move the mouse cursor to the element to hover over it
        #     actions.move_to_element(dropdown).perform()
        #
        #     logging.info("Hover functionality complted Successfully")
        #     time.sleep(sleep_time)
        #     take_screenshot(SPass_path, id, 'successful.png', driver)
        # except:
        #
        #     for i in final_xpath:
        #         try:
        #             # Wait for the keyword element to appear
        #             dropdown = WebDriverWait(driver, 20).until(
        #                 EC.element_to_be_clickable((By.XPATH, i)))
        #
        #             # Create an instance of ActionChains
        #             actions = ActionChains(driver)
        #
        #             # Move the mouse cursor to the element to hover over it
        #             actions.move_to_element(dropdown).perform()
        #
        #             logging.info("Hover functionality complted Successfully")
        #             time.sleep(sleep_time)
        #             take_screenshot(SPass_path,id,'successful.png', driver)
        #
        #         except:
        #             pass
        # take_screenshot(path,id,f'{str(each_step_no)+str(id)+prediction}.png')
        # # Continue with other actions after hovering
        # # For example, you can click on a sub-element of the hovered element
        # sub_element = driver.find_element_by_xpath("sub_element_xpath")
        # actions.move_to_element(sub_element).click().perform()
    except:
        logging.info("Hover functionality Failed")
        take_screenshot(SPass_path, id, f'{str(each_step_no) + str(id) + prediction}.png')
       
        


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

def image_compare():
    import cv2
    import numpy as np

    # Load the two images you want to compare
    image1 = cv2.imread(r'/screenshot_comp\screenshot_before.png')
    image2 = cv2.imread(r'/screenshot_comp\screenshot_after.png')

    # Check if the images have the same dimensions
    if image1.shape != image2.shape:
        raise ValueError("The images must have the same dimensions.")

    # Compute the absolute difference between the two images
    difference = cv2.absdiff(image1, image2)

    # Convert the difference image to grayscale
    gray_difference = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)

    # Calculate the percentage of change
    total_pixels = gray_difference.size
    changed_pixels = np.count_nonzero(gray_difference)
    percentage_change = (changed_pixels / total_pixels) * 100

    # Display the percentage change
    print(f"Percentage Change: {percentage_change:.2f}%")

    # Save the difference image
    cv2.imwrite('difference.jpg', difference)
    return percentage_change


def clean_screenshot_comp():
    # Specify the folder where you want to save the screenshots
    screenshot_folder = 'screenshot_comp/'

    # Ensure the screenshot folder exists, and remove existing images
    if not os.path.exists(screenshot_folder):
        os.makedirs(screenshot_folder)
    else:
        # Remove existing image files in the folder
        for file_name in os.listdir(screenshot_folder):
            if file_name.endswith('.png'):
                os.remove(os.path.join(screenshot_folder, file_name))




# Function to check if an XPath has format of 'html/body/style[index] or 'html/body/script[index]
def remove_elements_with_pattern(lst, pattern):
    filtered_list = [elem for elem in lst if not re.match(pattern, elem)]
    return filtered_list

