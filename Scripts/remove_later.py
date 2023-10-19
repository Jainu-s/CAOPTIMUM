import time
import re
import getxpath
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC











# def fill_spaces_with_sequence(html_code):
#     lines = html_code.split('\n')
#     max_spaces = 0
#     for line in lines:
#         num_spaces = len(line) - len(line.lstrip(' '))
#         max_spaces = max(max_spaces, num_spaces)
#
#     filled_code = ''
#     for i, line in enumerate(lines):
#         num_spaces = len(line) - len(line.lstrip(' '))
#         space_sequence = ''.join(str(j+1) for j in range(num_spaces))
#         filled_line = space_sequence + line.lstrip(' ')
#         filled_code += filled_line + '\n'
#
#     return filled_code

# HTML code
from bs4 import BeautifulSoup

html_code = '''
<!DOCTYPE html>
<html>

<head>
    <title>
        Simple web Development Template
    </title>
</head>

<body>
    <nav class="navbar background">
        <ul class="nav-list">
            <div class="logo">
                <img src="logo.png">
            </div>
            <li><a href="#web">Web Technology</a></li>
            <li><a href="#program">C Programming</a></li>
            <li><a href="#course">Courses</a></li>
        </ul>

        <div class="rightNav">
            <input type="text" name="search" id="search">
            <button class="btn btn-sm">Search</button>
        </div>
    </nav>

    <section class="firstsection">
        <div class="box-main">
            <div class="firstHalf">
                <h1 class="text-big" id="web">
                    Web Technology
                </h1>

                <p class="text-small">
                    HTML stands for HyperText Markup
                    Language. It is used to design
                    web pages using a markup language.
                    HTML is the combination of Hypertext
                    and Markup language. Hypertext
                    defines the link between the web
                    pages. A markup language is used
                    to define the text document within
                    tag which defines the structure of
                    web pages. HTML is a markup language
                    that is used by the browser to
                    manipulate text, images, and other
                    content to display it in the required
                    format.
                </p>


            </div>
        <div>
            <p> Jainmiah Shaik </p>
        </div>
        </div>
    </section>

    <section class="secondsection">
        <div class="box-main">
            <div class="secondHalf">
                <h1 class="text-big" id="program">
                    C Programming
                </h1>
                <p class="text-small">
                    C is a procedural programming language.
                    It was initially developed by Dennis
                    Ritchie as a system programming
                    language to write operating system.
                    The main features of C language include
                    low-level access to memory, simple set
                    of keywords, and clean style, these
                    features make C language suitable for
                    system programming like operating system
                    or compiler development.
                </p>


            </div>
        </div>
    </section>

    <section class="section">
        <div class="paras">
            <h1 class="sectionTag text-big">Java</h1>

            <p class="sectionSubTag text-small">
                Java has been one of the most
                popular programming language
                for many years. Java is Object
                Oriented. However it is not
                considered as pure object oriented
                as it provides support for primitive
                data types (like int, char, etc) The
                Java codes are first compiled into byte
                code (machine independent code). Then
                the byte code is run on Java Virtual
                Machine (JVM) regardless of the
                underlying architecture.
            </p>


        </div>

        <div class="thumbnail">
            <img src="img.png" alt="laptop image">
        </div>
    </section>

    <footer class="background">
        <p class="text-footer">
            Copyright ©-All rights are reserved
        </p>


    </footer>
</body>

</html>
'''

# filled_html_code = fill_spaces_with_sequence(html_code)
# print(filled_html_code)



# def fill_spaces_with_sequence(html_code):
#     lines = html_code.split('\n')
#     max_spaces = 0
#     first_line_index = ''  # Variable to store the tags at the beginning of each line
#
#     for line in lines:
#         num_spaces = len(line) - len(line.lstrip(' '))
#         max_spaces = max(max_spaces, num_spaces)
#
#         # Check if the line starts with specific HTML tags and has no leading spaces
#         if num_spaces == 0 and line.lstrip().startswith(('<html', '<div', '<span', '<head', '<body')):
#             tag = line.split()[0]  # Extract the tag from the line
#             first_line_index += tag + ' '  # Add the tag to first_line_index variable
#
#     filled_code = ''
#     for i, line in enumerate(lines):
#         num_spaces = len(line) - len(line.lstrip(' '))
#         space_sequence = ''.join(str(j+1) for j in range(num_spaces))
#         filled_line = space_sequence + line.lstrip(' ')
#         filled_code += filled_line + '\n'
#
#     print('First line index:', first_line_index)  # Print the first_line_index variable
#     return filled_code
#
#
# # Rest of your code remains the same
#
# filled_html_code = fill_spaces_with_sequence(html_code)
# print(filled_html_code)

#######################################################################
import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://www.flipkart.com"

# Send a GET request to the URL
response = requests.get(url)

# Get the HTML content from the response
html_content = response.text

# Create a BeautifulSoup object to parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Prettify the HTML code
prettified_html = soup.prettify()

#######################################################################3
# Print the beautified HTML code
# print(prettified_html)


# def find_element(html_code, target):
#     soup = BeautifulSoup(html_code, 'html.parser')
#     elements = soup.find_all(text=lambda text: target in text.strip())
#
#     if not elements:
#         return "Element not found."
#
#     paths = []
#     for element in elements:
#         path = []
#         current = element
#         while current.parent:
#             tag = current.name
#             index = sum(1 for sibling in current.previous_siblings if sibling.name == tag) + 1
#             path.insert(0, f"{tag}[{index}]")
#             current = current.parent
#         paths.append("/".join(path))
#
#     return "\n".join(paths)
#
#
# html_code = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>My Webpage</title>
# </head>
# <body>
#     <h1>Welcome to My Webpage</h1>
#     <p>This is a sample HTML code.</p>
#     <div>
#         <div> This is sample before 1st div </div>
#         <div>This is 1st div in body </div>
#         <div>
#             <ul>
#                 <li>This is list one</li>
#                 <li>This is 2nd list</li>
#                 <li>This is 3rd list</li>
#             </ul> </div>
#         <div>
#             <p>This for anchor tag</p>
#             <a href='#'>This is the link</a>
#         </div>
#     </div>
#     <div> This is 2nd div in body </div>
#     <div>
#         <span>Some text</span>
#     </div>
# </body>
# </html>
# """
#
# target = "Download Paytm App"
# output = find_element(prettified_html, target)
# print(f"Input: {target}")
# print(f"Output: {output}")
#


# from bs4 import BeautifulSoup
#
# def find_element(html_code, target, sub_text=None):
#     soup = BeautifulSoup(html_code, 'html.parser')
#     target_elements = soup.find_all(text=lambda text: target in text.strip())
#
#     if not target_elements:
#         return "Element not found."
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
#             if div_element and sub_text in div_element.get_text():
#                 paths.append("/".join(path))
#         else:
#             paths.append("/".join(path))
#
#     return "\n".join(paths)
#
#
# html_code = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>My Webpage</title>
# </head>
# <body>
#     <h1>Welcome to My Webpage</h1>
#     <p>This is a sample HTML code.</p>
#     <div>
#         <div> This is sample before 1st div </div>
#         <div>This is 1st div in body </div>
#         <div>
#             <p>Employee Related</p>
#             <a href=#> KNOW MORE </a>
#         </div>
#         <div>
#             <p>Student Related</p>
#             <a href=#> KNOW MORE </a>
#         </div>
#     </div>
#     <div> This is 2nd div in body </div>
#     <div>
#         <div>
#             <div>
#                 <h5>Big Title</h5>
#             </div>
#                 <a href=#> KNOW MORE </a>
#             </div>
#         </div>
#     <div>
#         <span>Some text</span>
#     </div>
# </body>
# </html>
# """
#
# target = "KNOW MORE"
# sub_text = "Student Related"
# output = find_element(html_code, target, sub_text)
# print(f"Input: {target}")
# print(f"Subtext: {sub_text}")
# print(f"Output: {output}")

from bs4 import BeautifulSoup


# def process_xpath(xpath):
#     # Remove "/None[1]" from the xpath
#     xpath = xpath.replace("/None[1]", "")
#
#     # Remove the indexing "[1]" from each element except the last one
#     xpath_parts = xpath.split('/')
#     xpath_parts = [part.split('[')[0] for part in xpath_parts[:-1]]
#
#     # Add back the indexing for the last element if it is not empty
#     last_part = xpath_parts[-1].split('[')[0]
#     if last_part:
#         xpath_parts[-1] = last_part
#
#     # Reconstruct the modified xpath
#     modified_xpath = '/'.join(xpath_parts)
#
#     return modified_xpath
#
#
# def find_element(html_code, target, sub_text=None):
#     soup = BeautifulSoup(html_code, 'html.parser')
#     target_elements = soup.find_all(text=lambda text: target in text.strip())
#
#     if not target_elements:
#         return "Element not found."
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
#                     paths.append("/".join(path))
#             else:
#                 # Check if sub_text is in target_element's direct parent div
#                 direct_parent_div = target_element.find_parent('div')
#                 if direct_parent_div and sub_text in direct_parent_div.get_text():
#                     paths.append("/".join(path))
#         else:
#             paths.append("/".join(path))
#
#     return "\n".join(paths)


def find_element(html_code, target, sub_text=None):
    soup = BeautifulSoup(html_code, 'html.parser')
    target_elements = soup.find_all(text=lambda text: target in text.strip())

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
                if parent_div_element and sub_text in parent_div_element.get_text():
                    paths.append(path)
            else:
                direct_parent_div = target_element.find_parent('div')
                if direct_parent_div and sub_text in direct_parent_div.get_text():
                    paths.append(path)
        else:
            paths.append(path)

    if not paths:
        return ["Element not found."]

    return paths


html_code = """
<!DOCTYPE html>
<html>
<head>
    <title>My Webpage</title>
</head>
<body>
    <h1>Welcome to My Webpage</h1>
    <p>This is a sample HTML code.</p>
    <div>
        <div> This is sample before 1st div </div>
        <div>This is 1st div in body </div>
        <div>
            <p>Employee Related</p>
            <a href=#> KNOW MORE </a>
        </div>
        <div>
            <p>Student Related</p>
            <a href=#> KNOW MORE </a>
        </div>
    </div>
    <div> This is 2nd div in body </div>
    <div>
        <div>
            <h5>Big Title</h5>
            <div>
                <a href=#> KNOW MORE </a>
            </div>
        </div>
    </div>
    <div>
        <span>Some text</span>
    </div>
</body>
</html>
"""

def funct(output):
    results = []
    for i in output:
        # Remove '[1]' only if it appears at the end of each element
        x = [element.replace('[1]', '') if element.endswith('[1]') else element for element in i]

        # Remove 'None' element from the list
        x = [element for element in x if element != 'None']

        result = "/".join(x)
        results.append(result)
        print(result)




# target = "X"
# sub_text = None
# output = find_element(prettified_html, target, sub_text)
# funct(output)
#







