import contextlib
import datetime
import math
import random
import time
import re
import sys

import execjs

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


# Set up logging
from Logs.logger_config import setup_logging
import logging



SPass_path = r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot\Test Case Passed'
SFail_path = r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Screenshot\Test Case Failed'
sleep_time = 3

# Temporary Xpath for Victoria Secret
account_xpath = '/html/body/div[2]/header/nav[1]/div[2]/ul/li[1]/div/a/div'
cart_bag_xpath = '//*[@id="masthead-utility-nav-tab-shopping-bag"]/div/svg/g/path[1]'
checkout_xpath =  '/html/body/reach-portal/div[3]/div/section/div[4]/div/div/div/article/div/div[2]/button'
accept_continue = '//*[@id="buttons-aurus-overlay"]/div[2]/div[2]/button'
signin_xpath = '/html/body/reach-portal/div[3]/div/section/div[4]/div/div/div/article/div/div[1]/div[1]/a/span'
search_xpath = '/html/body/div[2]/header/div[2]/div/span/input'
close_xpath = '/html/body/reach-portal/div[3]/div/section/div[4]/div/div/div/article/div/div[1]/div[7]/div/div/div[3]/button/div/svg/path'



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
    chrome_options.accept_untrusted_certs = True
    chrome_options.add_extension(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Chrome Extensions\cookies_blocker_extension_1_7_0_0.crx')
    chrome_options.add_extension(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Chrome Extensions\popup_block_extension_0_6_6_0.crx')
    # chrome_options.add_extension(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\All Files\extension_1_0_1_0.crx')
    referer_url = "https://www.google.co.in"
    chrome_options.add_argument(f"--referer={referer_url}")
    # chrome_options.headless = True
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--allow-insecure-localhost')
    caps = chrome_options.to_capabilities()
    caps["acceptInsecureCerts"] = True
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-cache")
    chrome_options.add_argument("--disk-cache-size=0")
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--enable-javascript")
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(executable_path=r'C:\Users\abdul\PycharmProjects\Automation_Optimum\chrome webdriver\chromedriver.exe',options=chrome_options,desired_capabilities=caps)

    apply_driver_tweaks(driver)
    set_random_window_size(driver)
    random_mouse_movement()

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

    chrome_options.add_argument(f"user-agent={user_agent}")

    # driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    #     "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'
    # })
    # print(driver.execute_script("return navigator.userAgent;"))

    stealth(driver = driver,
            user_agent = user_agent,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )


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
        # Wait up to 10 seconds for an <a> tag to appear, indicating the page has loaded
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

        # Get the HTML content of the page
        html_content = driver.page_source

        # Save the HTML content to a file
        with open('webpage_content.html', 'w', encoding='utf-8') as file:
            file.write(html_content)

        time.sleep(3)

        button, item = extract_button_and_item_from_string(keyword)
        print('Button:', button, 'item:', item)
    except:
        pass


    # try:
    #     # Wait for a new window/tab to open
    #     current_tabs = len(driver.window_handles)
    #
    #     # Print window handles
    #     print(driver.window_handles)
    #
    #     # Check if a new tab has been opened and switch to it if it has.
    #     if len(driver.window_handles) > current_tabs:
    #         driver.switch_to.window(driver.window_handles[-1])
    # except:
    #     pass
    print('keyword:',keyword)

    def click_button_by_text(browser, search_text):
        # Find all button elements
        buttons = browser.find_elements(By.TAG_NAME, "button")

        # Add input elements of type 'button' to the list
        buttons.extend(browser.find_elements(By.XPATH, "//input[@type='submit']"))

        for button in buttons:
            if search_text in button.text:
                button.click()
                return
        print(f"No button found with the text: {search_text}")

    if 'button' in keyword or 'Button' in keyword:
        print('button triggered')
        try:
            # Get the page's source code
            html = driver.page_source

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Find all input tags
            input_tags = soup.find_all('input')

            # Loop over the input tags and find the ones with type="submit"
            for tag in input_tags:
                input_type = tag.get('type')
                if input_type == "submit":
                    print('found input type submit')
                    input_id = tag.get('id')
                    input_value = tag.get('value')

                    # If the tag has type="submit", find it in the actual browser using its id and value and click
                    wait = WebDriverWait(driver, 30)
                    if input_id:
                        # If the tag has an id attribute, preferentially use that for more accurate targeting
                        element = wait.until(EC.presence_of_element_located((By.ID, input_id)))
                    else:
                        # Otherwise, fallback to using type and value attributes
                        element = wait.until(
                            EC.presence_of_element_located((By.XPATH, f"//input[@type='submit'][@value='{input_value}']")))

                    element.click()
                    # If you only want to click the first found element, break out of the loop here
                    break
        except:
            try:
                print('Else button triggered')
                click_button_by_text(driver, button)
            except:
                pass



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

    # def click_nearest_target_to_sub_text(target_text, sub_text=None):
    #
    #     print('started -----------------------------------------------------------------')
    #     wait = WebDriverWait(driver, 30)
    #     sub_location = None
    #
    #     if sub_text:
    #         bigrams = generate_bigrams(sub_text)
    #         words = sub_text.split()
    #
    #         matching_elements = []
    #
    #         # First, search using bigrams
    #         for bigram in bigrams:
    #             potential_sub_elements = wait.until(
    #                 EC.presence_of_all_elements_located((By.XPATH, f"//*[contains(text(), '{bigram}')]")))
    #             matching_elements.extend([elem for elem in potential_sub_elements if bigram in elem.text])
    #
    #         # If no matching elements are found using bigrams, try individual words
    #         if not matching_elements:
    #             word_distances = {}
    #
    #             for word in words:
    #                 potential_sub_elements = wait.until(
    #                     EC.presence_of_all_elements_located((By.XPATH, f"//*[contains(text(), '{word}')]")))
    #                 for elem in potential_sub_elements:
    #                     if word in elem.text:
    #                         word_distances[word] = word_distances.get(word, float('inf'))
    #                         dist = compute_distance(elem.location, sub_location)
    #                         if dist < word_distances[word]:
    #                             word_distances[word] = dist
    #
    #             # Find the word with the shortest distance
    #             closest_word = min(word_distances, key=word_distances.get)
    #             sub_location = [elem for elem in potential_sub_elements if closest_word in elem.text][0].location
    #
    #     wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{target_text}')]")))
    #     target_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{target_text}')]")
    #     if not target_elements:
    #         print("No target elements found!")
    #         return
    #
    #     if sub_location:
    #         nearest_element = min(target_elements, key=lambda elem: compute_distance(elem.location, sub_location))
    #     else:
    #         nearest_element = target_elements[0]
    #
    #     nearest_element.click()
    #     time.sleep(2)




    def search_multiple():

        html_code = driver.page_source
        prettified_html = pretty_code(html_code)

        original_xpath = find_element(prettified_html, button, item)
        print('full_Xpath: ', original_xpath)
        final_xpath = mod_xpath(original_xpath)
        print('final_xpath:', final_xpath)


        for i in final_xpath:
            print('Triggered i 2')
            try:
                # Wait for the keyword element to appear
                val = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, i)))
                val.click()

            except:
                pass



    def click_single_element1():
        print("Click - 1 Triggered")
        # Find all elements with the specified text

        target_element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{button}')]")))

        target_element1.click()

        time.sleep(2)

    def click_single_element2():

        print("Click - 2 Triggered")
        target_element2 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f"//*contains(text(),'{button}')]")))
        target_element2.click()
        time.sleep(2)


    def click_single_xpath(xpath):
        target_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH,xpath)))
        target_element.click()
        time.sleep(2)


    def find_link_by_attribute_value(html_source, button):
        soup = BeautifulSoup(html_source, 'html.parser')
        for link in soup.find_all('a'):
            for key, value in link.attrs.items():
                if button == value:
                    return link
        return None

    try:
        print('Button:',button)
    except:
        pass
    print('Keyword:',keyword)



    # Wait until at least one 'ADD' button is present and then get all 'ADD' buttons
    try:
        wait = WebDriverWait(driver, 20)  # wait for up to 20 seconds
        add_button = wait.until(EC.presence_of_element_located((By.XPATH,  f"//*[contains(text(), '{button}')]")))
        print('add_button:',add_button)
    except:
        pass

    try:
        add_buttons = driver.find_elements(By.XPATH, f"//*[contains(text(), '{button}')]")
    except:
        add_buttons = 0


    print('Length of the add_buttons:',add_buttons)
    # Print the number of 'ADD' buttons
    try:
        buttons_len = len(add_buttons)
        print('Buttons Length:', buttons_len)
        print('Button:',button)
        # try:
        #     if 'checkout' in button.lower():
        #         click_single_xpath(chekout_xpath)
        # except:
        #     print('checout failed')
        #     try:
        #         if 'ACCEPT & CONTINUE' in button:
        #             click_single_xpath(terms_conditions)
        #     except:
        #         print('Accept & Continue failed')
        #         try:
        #             if 'user account' in button.lower():
        #                 click_single_xpath(account_xpath)
        #         except:
        #             try:
        #                 if 'cart' or 'bag' in button.lower():
        #                     click_single_xpath(cart_bag_xpath)
        #             except:


        if 'CHECKOUT' in button:
            print('CHECKOUT Triggered')
            click_single_xpath(checkout_xpath)

        elif 'ACCEPT & CONTINUE' in button:
            print('ACCEPT & CONTINUE Triggered')
            click_single_xpath(accept_continue)

        elif 'user' in button.strip():
            print('user Triggered')
            click_single_xpath(account_xpath)

        elif 'bag' in button.strip():
            print('bag Triggered')
            click_single_xpath(cart_bag_xpath)

        elif 'search' in button.strip():
            print('search Triggered')
            click_single_xpath(search_xpath)

        elif 'delete' in button.strip():
            print('delete Triggered')
            click_single_xpath(close_xpath)


        elif buttons_len > 1:
            print('Buttons > 1 started')

            try:
                click_single_element1()
                time.sleep(sleep_time)
                take_screenshot(SPass_path, id, 'successful.png', driver)
                logging.info('Click Functionality Successful')

            except:
                try:
                    click_single_element2()
                    time.sleep(sleep_time)
                    take_screenshot(SPass_path, id, 'successful.png',driver)
                    logging.info('Click Functionality Successful')
                except:
                    try:
                        click_nearest_target_to_sub_text(button, item)
                        time.sleep(sleep_time)
                        take_screenshot(SPass_path, id, 'successful.png', driver)
                        logging.info('Click Functionality Successful')
                    except:

                        try:
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

                        except:
                            try:
                                click_single_element2()
                                time.sleep(sleep_time)
                                take_screenshot(SPass_path, id, 'successful.png', driver)
                                logging.info('Click Functionality Successful')

                            except:
                                logging.info("Click Funtionality Failed")
                                take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')


        elif buttons_len == 1:
            print('Buttons == 1 started')

            try:
                click_single_element1()
                time.sleep(sleep_time)
                take_screenshot(SPass_path, id, 'successful.png', driver)
                logging.info('Click Functionality Successful')
            except:
                try:
                    click_single_element2()
                    time.sleep(sleep_time)
                    take_screenshot(SPass_path, id, 'successful.png', driver)
                    logging.info('Click Functionality Successful')
                except:
                    try:
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
                    except:
                        take_screenshot((SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png'))
                        logging.info('Click Functionality Failed')

        elif buttons_len == 0:

            try:
                click_single_element1()
                time.sleep(sleep_time)
                take_screenshot(SPass_path, id, 'successful.png', driver)
                logging.info('Click Functionality Successful')
            except:
                try:
                    click_single_element2()
                    time.sleep(sleep_time)
                    take_screenshot(SPass_path, id, 'successful.png', driver)
                    logging.info('Click Functionality Successful')
                except:
                    try:
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
                    except:
                        take_screenshot((SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png'))
                        logging.info('Click Functionality Failed')



        else:
            logging.info("Click Funtionality Failed")
            take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')


    except:
        logging.info("Click Funtionality Failed")
        take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')
       
        




    # def click_function(driver, clickable_url, keyword, id, each_step_no, prediction):
#     button, item = extract_button_and_item_from_string(keyword)
#     print('Button:', button, 'Item:',item)
#
#     try:
#         alert = Alert(driver)
#         alert.accept()  # Use .dismiss() to click "Cancel" if needed
#     except Exception:
#         # If there is no alert, an exception will be raised (no need to handle it)
#         pass
#
#
#     print('Click Function Triggered:')
#     keyword = keyword.replace('nan', '')
#
#     time.sleep(4)
#     global double_quoted_word
#
#
#     # Construct the XPath query to find the desired element based on the additional information
#     try:
#         def compute_distance(location1, location2):
#             """Calculate the Euclidean distance between two points."""
#             return math.sqrt((location1['x'] - location2['x']) ** 2 + (location1['y'] - location2['y']) ** 2)
#
#         def click_nearest_target_to_sub_text(target_text, sub_text=None):
#             print('started -----------------------------------------------------------------')
#
#             # Set up WebDriverWait
#             wait = WebDriverWait(driver, 30)  # 30 seconds timeout
#
#             # If sub_text is provided, find its location
#             if sub_text:
#                 # Let's first take a snippet of the sub_text to locate a potential match
#                 snippet = sub_text[:20]  # assuming the first 20 characters can be a good snippet; adjust as necessary
#
#                 # Find potential elements that might have the sub_text
#                 potential_sub_elements = wait.until(
#                     EC.presence_of_all_elements_located((By.XPATH, f"//*[contains(text(), '{snippet}')]")))
#
#                 # Filter elements to check if they match the whole sub_text
#                 matching_elements = [elem for elem in potential_sub_elements if sub_text in elem.text]
#
#                 if not matching_elements:
#                     print("No matching sub_text found!")
#                     return
#
#                 sub_element = matching_elements[
#                     0]  # choosing the first match; adjust logic if there are multiple valid matches
#                 sub_location = sub_element.location
#             else:
#                 sub_location = None
#
#             # Wait until at least one target_text element is present
#             wait.until(EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{target_text}')]")))
#
#             # Find all elements that have the target_text
#             target_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{target_text}')]")
#
#             if not target_elements:
#                 print("No target elements found!")
#                 return
#
#             if sub_location:
#                 # If sub_location is found, find the target_text element closest to the sub_text
#                 nearest_element = min(target_elements, key=lambda elem: compute_distance(elem.location, sub_location))
#             else:
#                 # If no sub_location, simply click on the first target_text found
#                 nearest_element = target_elements[0]
#
#             # Click on the nearest target_text
#             nearest_element.click()
#
#
#         click_nearest_target_to_sub_text(button, item)
#         take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#     except:
#         try:
#             search_element = WebDriverWait.until(
#                 EC.element_to_be_clickable((By.XPATH, f"//*[contains(@*, {button})]")))
#             search_element.click()
#         except:
#             logging.info("Click Functionality Failed")
#             take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#
#
#
#     if 'official link' in keyword or 'original link' in keyword or 'link' in keyword:
#         try:
#             print('This official link block is executed')
#             url = clickable_url
#             # Wait for the search results to appear
#             wait = WebDriverWait(driver, 20)
#             search_results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g")))
#             from urllib.parse import urlparse
#
#             def extract_domain(url):
#                 parsed_url = urlparse(url)
#                 domain = parsed_url.netloc
#                 return domain
#
#             domain = extract_domain(url)
#             print('domain', domain)
#             # Find and click the first link that corresponds to Flipkart
#             for result in search_results:
#                 link = result.find_element(By.XPATH, ".//a")
#                 if domain in link.get_attribute("href"):
#                     link.click()
#                     logging.info("Click Functionality Successfully Completed")
#                     take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#                     break
#         except:
#             logging.info("Click Functionality Failed")
#             take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#     else:
#         try:
#             target_element = WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{button}')]")))
#             target_element.click()
#             take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#         except:
#             try:
#                 target_element1 = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, f"//*contains(text(),'{button}')]")))
#                 target_element1.click()
#                 take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#             except:
#                 try:
#                     print('click url:', driver.current_url)
#                     html_code = driver.page_source
#                     prettified_html = pretty_code(html_code)
#                     # # with open('output.html', 'w', encoding='utf-8') as file:
#                     # #     file.write(prettified_html)
#                     # # print('Double Quoted Keyword:', double_quoted_keyword, '&', 'additional info:', additional_info)
#                     original_xpath = find_element(prettified_html, button, item)
#                     print('full_Xpath: ', original_xpath)
#                     final_xpath = mod_xpath(original_xpath)
#                     print('final_xpath:', final_xpath)
#
#
#                     for i in final_xpath:
#                         print('Triggered i 2')
#                         try:
#                             # Wait for the keyword element to appear
#                             val = WebDriverWait(driver, 20).until(
#                                 EC.presence_of_element_located((By.XPATH, i)))
#                             val.click()
#                             logging.info("click functionality complted Successfully")
#                             take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#                         except:
#                             try:
#                                 if 'button' in keyword:
#                                     button = driver.find_element_by_xpath(
#                                         '//input[(contains(@value, "Submit") and @type="button") or (contains(@value, "Submit") and @type="btn")]')
#                                     button.click()
#                                     take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#                             except:
#                                 logging.info("click Functionality Failed")
#                                 take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')
#                 except:
#                     logging.info("click Functionality Failed")
#                     take_screenshot(path, id, f'{str(each_step_no) + str(id) + prediction}.png')



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



        element.send_keys(double_quoted_keyword)

        if 'search' in keyword.lower():
            element.send_keys(Keys.ENTER)

        print('keyword:',keyword)
        if 'location' in keyword.lower():
            try:
                time.sleep(3)
                element.send_keys(Keys.TAB, Keys.ENTER)
            except:
                pass

        logging.info("Insert functionality complted Successfully")

        logging.info("Insert Funtionality Success")
        time.sleep(sleep_time)
        take_screenshot(SPass_path,id,'successful.png', driver)



    except:
        logging.info("Insert functionality Failed")
        take_screenshot(SFail_path, id, f'{str(each_step_no) + str(id) + prediction}.png')
       



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






# Function to check if an XPath has format of 'html/body/style[index] or 'html/body/script[index]
def remove_elements_with_pattern(lst, pattern):
    filtered_list = [elem for elem in lst if not re.match(pattern, elem)]
    return filtered_list

