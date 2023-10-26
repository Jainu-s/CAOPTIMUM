import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

'''
This code refines text data in a DataFrame by removing unnecessary elements like numbers, URLs, 
and specific keywords, and it tokenizes the text into words while preserving relevant content. 
It stores the processed text along with other columns in a new DataFrame and saves it as 
"Preprocessed.csv."
'''
def keyword_processing(df):

    # Define the stop words to be removed
    stop_words = set(stopwords.words('english'))

    # Define the specific words to be removed
    specific_words = ['click', 'press', 'open', 'hover', 'navigate', 'insert', 'enter', 'Open',
                      'Click', 'option', 'menu', 'google browser', 'firefox browser',
                      'chrome browser',
                      'browser', 'Google Browser', 'Chrome Browser', 'Browser', 'select']

    final_list = []
    # Iterate over each row
    for index, row in df.iterrows():
        # Create a list to store the steps for the current row
        steps_list = []

        # Check if the "Text" column has a value
        if pd.notnull(row['Text']):
            # Split the steps based on newlines (\n)
            steps = row['Text'].split('\n')
            # Remove any empty strings and leading/trailing whitespaces
            steps = [step.strip() for step in steps if step.strip()]

            # Remove numbers and parentheses from steps
            steps = [re.sub(r'^\d+\)|\d+\.', '', step) for step in steps]

            # Remove URLs from steps
            steps = [re.sub(r'http[s]?://\S+', '', step) for step in steps]

            filtered_steps = []
            for step in steps:
                if '"' in step:
                    # Split the step based on double quotes using regular expression
                    tokens = re.findall(r'[^"\s]+|"(?:\\.|[^"])*"', step)
                    filtered_step = []
                    add_text_found = False
                    for token in tokens:
                        if token.lower() == 'add_text':
                            # Set the flag to preserve text from "add_text" onwards
                            add_text_found = True
                        if add_text_found:
                            # Preserve the text from "add_text" onwards
                            if token.startswith('"') and token.endswith('"') and len(token) > 1:
                                # Remove double quotes from "add_text" token
                                token = token[1:-1]
                            filtered_step.append(token)
                        else:
                            if token.startswith('"') and token.endswith('"') and len(token) > 1:
                                # Keep the double quoted string as a single token without any modifications
                                filtered_step.append(token)
                            else:
                                # Tokenize the other parts of the step into words
                                words = word_tokenize(token)
                                for word in words:
                                    if (word.lower() not in stop_words and
                                            word.lower() not in specific_words and
                                            len(word) > 1 and
                                            not word.endswith("'s") and
                                            not re.match(r'^[\W\s]+$', word)):
                                        filtered_step.append(word)
                    filtered_steps.append(filtered_step)
                else:
                    # Tokenize the step into words
                    words = word_tokenize(step)
                    filtered_step = []
                    add_text_found = False
                    for word in words:
                        if word.lower() == 'add_text':
                            # Set the flag to preserve text from "add_text" onwards
                            add_text_found = True
                        if add_text_found:
                            # Preserve the text from "add_text" onwards
                            filtered_step.append(word)
                        else:
                            if (word.lower() not in stop_words and
                                    word.lower() not in specific_words and
                                    len(word) > 1 and
                                    not word.endswith("'s") and
                                    not re.match(r'^[\W\s]+$', word)):
                                filtered_step.append(word)
                    filtered_steps.append(filtered_step)

            steps_list = [' '.join(sublist) for sublist in filtered_steps]

        final_list.append(steps_list)

    # Convert final_list to a DataFrame with the desired column names
    new_df = pd.DataFrame(final_list, columns=['Text'])

    # Add additional columns to the new DataFrame
    new_df['Document'] = df['Document']
    new_df['Label'] = df['Label']
    new_df['URL'] = df['URL']
    # new_df['Url'] = df['Url']
    new_df['Prediction'] = df['Prediction']
    new_df.to_csv('Preprocessed.csv', index=False)
    return new_df


