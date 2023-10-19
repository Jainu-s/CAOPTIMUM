# from bs4 import BeautifulSoup
# import requests
#
# def remove_indices(xpath):
#     xpath = xpath.replace("[1]", "")
#     return xpath
#
# def get_tag_xpath(tag):
#     xpath = []
#     while tag and tag.name != '[document]':
#         index = sum(1 for sibling in tag.previous_siblings if sibling.name == tag.name) + 1
#         xpath.insert(0, f"{tag.name}[{index}]")
#         tag = tag.parent
#     return '/'.join(xpath)
#
# def find_xpath_with_keyword(soup, keyword):
#     xpath_list = []
#     for tag in soup.find_all(text=lambda text: keyword in text):
#         tag_xpath = get_tag_xpath(tag.parent)
#         if tag_xpath not in xpath_list:
#             xpath_list.append(tag_xpath)
#     return xpath_list
#
# url = "https://www.icicibank.com"  # Replace with the desired URL
# keyword = "Mutual Fund"  # Replace with the desired keyword
#
# response = requests.get(url)
# html_code = response.content
#
# soup = BeautifulSoup(html_code, 'html.parser')
#
# xpaths_with_keyword = find_xpath_with_keyword(soup, keyword)
#
#
# # for xpath in xpaths_with_keyword:
# # #     xpath = remove_indices(xpath)
# # #     print(xpath)
#
# for xpath in xpaths_with_keyword:
#     xpath = remove_indices(xpath)
#     print(xpath)

import requests

def fetch_html_from_url(url):
    """
    Fetches the HTML content from a given URL.
    :param url: The URL to fetch the HTML from.
    :return: The HTML content as a string.
    """
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        raise Exception(f"Failed to fetch HTML from URL: {url}")


# URL to fetch HTML from
url = "https://www.globalsqa.com/demo-site/"

# Fetch HTML from the URL
html_string = fetch_html_from_url(url)

# Print the HTML content
print(html_string)


html_string1= '''
<!DOCTYPE html>
<html lang="en">
<head>
<title>Page Title</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
/* CSS styles go here */
</style>
</head>
<body>
<div class="header">
  <h1>My Website</h1>
  <p>A <b>responsive</b> website created by me.</p>
</div>

<div class="navbar">
  <a href="#" class="active">Home</a>
  <a href="#">Link</a>
  <a href="#" class="right">Link</a>
</div>

<div class="row">
  <div class="side">
    <h2>About Me</h2>
    <h5>Photo of me:</h5>
    <div class="fakeimg" style="height:200px;">Image</div>
    <p>Some text about me in culpa qui officia deserunt mollit anim..</p>
    <h3>More Text</h3>
    <p>Lorem ipsum dolor sit ame.</p>
    <div class="fakeimg" style="height:60px;">Image</div><br>
    <div class="fakeimg" style="height:60px;">Image</div><br>
    <div class="fakeimg" style="height:60px;">Image</div>
  </div>
  <div class="main">
    <h2>TITLE HEADING</h2>
    <h5>Title description, Dec 7, 2017</h5>
    <div class="fakeimg" style="height:200px;">Image</div>
    <p>Some text..</p>
    <p>Sunt in culpa qui officia deserunt mollit anim id est laborum consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco.</p>
    <br>
    <h2>TITLE HEADING</h2>
    <h5>Title description, Sep 2, 2017</h5>
    <div class="fakeimg" style="height:200px;">Image</div>
    <p>Some text..</p>
    <p>Sunt in culpa qui officia deserunt mollit anim id est laborum consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco.</p>
  </div>
</div>

<div class="footer">
  <h2>Footer</h2>
</div>

</body>
</html>
'''

from lxml import etree, html


from lxml import etree, html


from lxml import etree, html



# def extract_text_full_paths(html_string):
#     """
#     Extract the full paths of the text elements from an HTML string.
#     :param html_string: The HTML string to extract from.
#     :return: A list of unique full paths of the text elements.
#     """
#     # Parse HTML
#     tree = html.fromstring(html_string)
#
#     # Find all text elements in the tree
#     text_elements = tree.xpath('//text()')
#
#     # Extract full paths of the text elements
#     full_paths = set()
#     for element in text_elements:
#         xpath_parts = []
#         node = element.getparent()
#         while node is not None:
#             xpath_parts.insert(0, str(node.tag))
#             node = node.getparent()
#         xpath = "/".join(xpath_parts)
#         full_paths.add(xpath)
#
#     return list(full_paths)

def extract_text_full_paths(html_string):
    """
    Extract the full XPaths of the text elements from an HTML string.
    :param html_string: The HTML string to extract from.
    :return: A list of full XPaths of the text elements.
    """
    # Parse HTML
    tree = html.fromstring(html_string)

    # Find all text elements in the tree
    text_elements = tree.xpath('//text()')

    # Extract full XPaths of the text elements
    full_xpaths = []
    for element in text_elements:
        xpath_parts = []
        node = element.getparent()
        while node is not None:
            xpath_parts.insert(0, str(node.tag))
            node = node.getparent()
        xpath_parts.append('text()')
        xpath = "/".join(xpath_parts)
        full_xpaths.append(xpath)

    return full_xpaths


def extract_text_from_full_paths(html_string):
    """
    Extract the text corresponding to the full paths of the text elements from an HTML string.
    :param html_string: The HTML string to extract from.
    :return: A dictionary mapping the full paths to their corresponding text.
    """
    # Parse HTML
    tree = html.fromstring(html_string)

    # Find all text elements in the tree
    text_elements = tree.xpath('//text()')

    # Extract text and their corresponding full paths
    text_dict = {}
    for element in text_elements:
        text = element.strip()
        if text:
            xpath_parts = []
            node = element.getparent()
            while node is not None:
                xpath_parts.insert(0, node.tag)
                node = node.getparent()
            xpath = "/".join(xpath_parts)
            text_dict[xpath] = text

    return text_dict


print(extract_text_full_paths(html_string))
print(extract_text_from_full_paths(html_string))