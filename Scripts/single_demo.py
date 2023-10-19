# from bs4 import BeautifulSoup
#
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
#
# html_code = '''
# <!--
# Online HTML, CSS and JavaScript editor to run code online.
# -->
# <!DOCTYPE html>
# <html lang="en">
#
# <head>
#   <meta charset="UTF-8" />
#   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#   <link rel="stylesheet" href="style.css" />
#   <title>Browser</title>
# </head>
#
# <body>
#   <div>
#     <div>
#       <div>
#           <h1>
#             1st Heading
#           </h1>
#       </div>
#       <p>
#         1st Paragraph
#       </p>
#       <div>
#         <span> <a href='www.google.com'>LOGIN</a> Here </span>
#       </div>
#     </div>
#     <div>
#         <div>
#           <h1>
#             2nd <span> Heading </span>
#           </h1>
#         </div>
#         <p>
#             2nd Paragraph
#         </p>
#         <div>
#             <span> <a href='www.google.com'>LOGIN</a> Here </span>
#         </div>
#     </div>
#   </div>
#   <script src="script.js"></script>
# </body>
#
# </html>
# '''
#
# target = 'LOGIN'
# sub_text = '1st'
#
# result = find_element(html_code, target, sub_text)
# print(result)



from bs4 import BeautifulSoup
#
# def mod_xpath(output):
#     results = []
#     for i in output:
#         path_dict = {}
#         for key, value in i.items():
#             if value == 'value':
#                 # Remove '[1]' only if it appears at the end of the element
#                 key = key.replace('[1]', '')
#                 path_dict[key] = 'path'
#             elif value == 'text':
#                 path_dict[key] = 'text'
#         results.append(path_dict)
#     return results
#
#
#
#
#
# from bs4 import BeautifulSoup
#
# def find_element(html_code, target, sub_text=None):
#     soup = BeautifulSoup(html_code, 'html.parser')
#     target_elements = soup.find_all(text=lambda text: target in text.strip())
#
#     if not target_elements:
#         return ["Element not found."]
#
#     paths_with_text = []
#     for target_element in target_elements:
#         path = []
#         current = target_element
#         while current.parent:
#             tag = current.name
#             index = sum(1 for sibling in current.previous_siblings if sibling.name == tag) + 1
#             path.insert(0, f"{tag}[{index}]")
#             current = current.parent
#
#         text = target_element.strip()
#         path_with_text = {
#             "/".join(path): 'value',
#             text: 'text'
#         }
#
#         if sub_text:
#             div_element = target_element.find_parent('div')
#             if div_element:
#                 parent_div_element = div_element.find_parent('div')
#                 if parent_div_element:
#                     parent_text = parent_div_element.get_text()
#                     if all(keyword in parent_text for keyword in sub_text.split()):
#                         paths_with_text.append(path_with_text)
#             else:
#                 direct_parent_div = target_element.find_parent('div')
#                 if direct_parent_div:
#                     parent_text = direct_parent_div.get_text()
#                     if all(keyword in parent_text for keyword in sub_text.split()):
#                         paths_with_text.append(path_with_text)
#         else:
#             paths_with_text.append(path_with_text)
#
#     if not paths_with_text:
#         return ["Element not found."]
#
#     return paths_with_text
#
#
#
# html_code = '''
# <!--
# Online HTML, CSS and JavaScript editor to run code online.
# -->
# <!DOCTYPE html>
# <html lang="en">
#
# <head>
#   <meta charset="UTF-8" />
#   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
#   <link rel="stylesheet" href="style.css" />
#   <title>Browser</title>
# </head>
#
# <body>
#   <div>
#     <div>
#       <div>
#           <h1>
#             1st Heading
#           </h1>
#       </div>
#       <p>
#         1st Paragraph
#       </p>
#       <div>
#         <span> <a href='www.google.com'>LOGIN</a> Here </span>
#       </div>
#     </div>
#     <div>
#         <p> Hello </p>
#         <div>
#           <h1>
#             2nd <span> Heading </span>
#           </h1>
#         </div>
#         <p>
#             2nd Paragraph
#         </p>
#         <div>
#             <span> <a href='www.google.com'>LOGIN</a> Here </span>
#         </div>
#     </div>
#   </div>
#   <script src="script.js"></script>
# </body>
#
# </html>
# '''
#
# target = 'LOGIN'
# sub_text = '2nd Heading 2nd Paragraph'
#
# result = find_element(html_code, target, sub_text)
# print(result)
# print('mod:',mod_xpath(result))


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
                if parent_div_element:
                    parent_text = parent_div_element.get_text()
                    if all(keyword in parent_text for keyword in sub_text.split()):
                        paths.append(path)
            else:
                direct_parent_div = target_element.find_parent('div')
                if direct_parent_div:
                    parent_text = direct_parent_div.get_text()
                    if all(keyword in parent_text for keyword in sub_text.split()):
                        paths.append(path)
        else:
            paths.append(path)

    if not paths:
        return ["Element not found."]

    return paths


# Send a GET request to the HTML page
url = "https://example.com"  # Replace with the URL of the HTML page
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

find_element(soup,'Login')