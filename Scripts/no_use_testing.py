from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the driver (assumes you have ChromeDriver downloaded)
# Make sure you have the correct driver version for your Chrome browser.
driver = webdriver.Chrome(executable_path=r'C:\Users\abdul\PycharmProjects\Automation_Optimum\chrome webdriver\chromedriver.exe') # adjust the path as needed

# Open a webpage
driver.get('https://www.victoriassecret.com/in/vs/beauty?scroll=true')  # replace this URL with your desired URL

# Wait up to 10 seconds for an <a> tag to appear, indicating the page has loaded
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a')))

# Find all <a> tags on the webpage
a_tags = driver.find_elements(By.TAG_NAME,'href')
print('tags:',a_tags)

# Print out each <a> tag
for tag in a_tags:
    print(tag.get_attribute('outerHTML'))

# Close the browser
driver.quit()
