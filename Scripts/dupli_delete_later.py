from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Selenium browser driver
driver = webdriver.Chrome(executable_path=r'C:\Users\abdul\PycharmProjects\Automation_Optimum\chrome webdriver\chromedriver.exe')  # replace '/path/to/chromedriver' with the path to your ChromeDriver

# Open the webpage
driver.get('https://www.victoriassecret.com/in/')  # replace with your URL

driver.switch_to.default_content()

print(driver.page_source)

element = driver.find_element(By.XPATH, "//*[text()='BEAUTY']")
element.click()
time.sleep(2)