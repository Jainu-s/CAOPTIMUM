import re

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


# import spacy
# from spacy.matcher import Matcher
#
# # Load the English language model for spaCy
# nlp = spacy.load("en_core_web_sm")
#
# def extract_button_and_item_from_string(sentence):
#     doc = nlp(sentence)
#
#     # Initialize matcher
#     matcher = Matcher(nlp.vocab)
#     # Define pattern for 'click [button name] button' structure
#     pattern = [{"LOWER": "click"}, {}, {"LOWER": "button"}]
#     matcher.add("BTN_PATTERN", [pattern])
#
#     matches = matcher(doc)
#     for match_id, start, end in matches:
#         # This gets the word right after "click", which is assumed to be the button name
#         button_name = doc[start+1].text
#         # This gets the noun chunk closest to the matched pattern, assumed to be the item
#         item_name = [chunk.text for chunk in doc.noun_chunks if chunk.root.i > end or chunk.root.i < start][0]
#         return {'Button': button_name, 'Item': item_name}
#
#     return None
#
# # sentence = "For the student section, please press the Register button."
# # result = extract_button_and_item_from_string(sentence)
#
# sentence = 'we named green as button name which is near to kulcha'
# result = extract_button_and_item_from_string(sentence)
#
# if result:
#     print(f"For the '{result['Item']}' item, click the '{result['Button']}' button.")
# else:
#     print(f"Could not extract information from: {sentence}")



