import re

''' This code defines a function to extract button names and item names from a given input string. 
It identifies the button name enclosed in double quotes and removes stopwords 
(common words like 'click,' 'select,' etc.) from the remaining text, resulting in cleaned button
 and item names. The provided test demonstrates this functionality.'''


# Basic list of stopwords for our context. Expand as needed.
stopwords = set(['click', 'clik', 'select', 'on', 'and', 'under', 'clicking','given','laptop'])


def extract_button_and_item_from_string(line):
    # Extract double quoted words for buttons
    button = re.findall(r'\"(.*?)\"', line)
    button_name = button[0] if button else None

    # Extract items
    item_name = line
    if button_name:
        item_name = item_name.replace(button_name, '')  # Remove button name from line
    words = item_name.split()
    item_name = ' '.join(word for word in words if word.lower() not in stopwords)

    # Remove any kind of quotes and extra spaces
    item_name = re.sub(r'[\"\']', '', item_name).strip()

    return button_name, item_name


# Test
line = 'click on "Continue" button'
button, item_name = extract_button_and_item_from_string(line)
print(f"Button: {button}, Item: {item_name}")


