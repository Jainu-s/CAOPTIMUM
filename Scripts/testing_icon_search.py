from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def find_and_click_search(url):
    # Set up the Selenium webdriver (make sure you have installed the appropriate browser driver)
    driver = webdriver.Chrome()

    # Fetch the HTML code from the URL using Selenium with explicit wait for page to load
    driver.get(url)
    wait = WebDriverWait(driver, 10)  # Adjust the timeout (in seconds) as needed

    # Wait until the search element is clickable
    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@data-value='search-alias=aps']")))

    # Use ActionChains to perform a click action without interception
    actions = ActionChains(driver)
    actions.click(search_element).perform()

    # Get the final HTML source after interactions (optional)
    page_source = driver.page_source

    # Close the browser window
    driver.quit()

    return page_source

# Example usage
url = "https://amazon.in"  # Replace this with the URL of the webpage you want to fetch
page_source = find_and_click_search(url)
print(page_source)
