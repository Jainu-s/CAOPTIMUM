# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from bs4 import BeautifulSoup
#
# # Set up the WebDriver (replace "path_to_chromedriver" with the actual path to your chromedriver executable)
# driver = webdriver.Chrome()
#
# # Replace "your_url" with the URL you want to load
# url = "https://optimumrecruit.uat.peoplestrong.com/"
#
# # Load the webpage
# driver.get(url)
#
# # Wait for the page to load completely
# wait = WebDriverWait(driver, 10)  # Adjust the timeout as per your requirements
#
# # Find all the specified tags and retrieve their attributes
# tags = ["span", "nav", "img", "a", "button", "form", "input"]
# tag_attributes = {}
#
# for tag in tags:
#     tag_attributes[tag] = []
#     try:
#         elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, tag)))
#         for element in elements:
#             attributes = element.get_attribute("outerHTML")
#             soup = BeautifulSoup(attributes, "html.parser")
#             tag_element = soup.find(tag)
#             if tag_element is not None and tag_element.attrs:
#                 tag_attributes[tag].append(tag_element)
#                 #tag_attributes[tag].append(tag_element.attrs)
#     except:
#         pass
# # Print the tags and their attributes
# for tag, attributes in tag_attributes.items():
#     print(f"{tag} - Attributes:")
#     for attrs in attributes:
#         print(attrs)
#     print("\n")
#
# # Close the WebDriver
# driver.quit()



from bs4 import BeautifulSoup

# Sample HTML content
html_content = '''
<!DOCTYPE html>
<html>

<head>
  <title>Complex Div Block</title>
</head>

<body>
  <div style="border: 1px solid #ccc; padding: 20px;">
    <h2>Hello, this is a complex div block!</h2>
    <p>This div contains multiple elements such as span, input, dropdown, and button.</p>

    <!-- Span Element -->
    <div>
      <span style="font-weight: bold;">This is a span element.</span>
    </div>

    <!-- Input Element -->
    <div>
      <label for="inputField">Enter your name:</label>
      <input type="text" id="inputField" placeholder="Your Name" />
    </div>

    <!-- Dropdown Element -->
    <div>
      <div>
      	<label for="dropdown">Select your favorite color:</label>
      	<select id="dropdown">
        	<option value="red">Red</option>
        	<option value="blue">Blue</option>
        	<option value="green">Green</option>
        	<option value="yellow">Yellow</option>
      	</select>
      </div>
      <div>
        <span>Login Here</span>
    </div>

    <!-- Button Element -->
    <div>
      <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; cursor: pointer;">Click Me</button>
    </div>

    <!-- Nested Div -->
    <div style="margin-top: 20px; border: 1px solid #ddd; padding: 10px;">
      <h3>Nested Div Block</h3>
      <p>This is a div inside another div with some text.</p>
    </div>
  </div>
</body>

</html>

'''

# Parse the HTML content using Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the element with the text "Red"
red_element = soup.find(text='Red')

# Get the XPath of the "Red" element
def get_xpath(element):
    elements = [e.name for e in element.parents][::-1]
    return '/'.join(elements)

red_xpath = get_xpath(red_element)

print("XPath of the 'Red' element:", red_xpath)
