import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def process_execution_steps(excel_file, keywords_file):
    # Read Excel file and create DataFrame
    df = pd.read_excel(excel_file)

    # Create an empty list to store the results
    results = []

    # Define the stop words
    stop_words = set(stopwords.words('english'))

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Get the text from the "Execution Steps" column
        text = row["Execution Steps"]

        # Find the URL in the text using regex
        url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
        url_matches = re.findall(url_pattern, text)
        urls = [match.strip() for match in url_matches]

        # Split text based on digits like 1), 2), 3)....so on
        split_text = []
        current_segment = ""
        for char in text:
            if char.isdigit() or char == '.':
                if current_segment:
                    split_text.append(current_segment.strip())
                current_segment = char
            else:
                current_segment += char
        if current_segment:
            split_text.append(current_segment.strip())

        # Process the split text to find keywords and remove stop words
        with open(keywords_file, 'r') as file:
            keywords = file.read().splitlines()
            keywords = keywords[0].split(',')
            keywords = [element.lower() for element in keywords]

        keyword_list = []
        for segment in split_text:
            # Tokenize the segment
            tokens = word_tokenize(segment)

            # Remove stop words from the tokens
            filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

            # Find keywords in the filtered tokens
            key_list = []
            for token in filtered_tokens:
                if token.lower() in keywords:
                    key_list.append(token.lower())

            keyword_list.append(key_list)

        # Remove consecutive repeated elements in each sublist
        cleaned_list = []
        for sublist in keyword_list:
            if sublist:  # Check if the sublist is not empty
                cleaned_sublist = [sublist[0]]
                for i in range(1, len(sublist)):
                    if sublist[i] != sublist[i - 1]:
                        cleaned_sublist.append(sublist[i])
                cleaned_list.append(cleaned_sublist)

        # Append the URL and cleaned list to the results if it's not empty
        if urls or cleaned_list:
            results.append([urls, cleaned_list])

    # Return the results as a list of lists
    return results



