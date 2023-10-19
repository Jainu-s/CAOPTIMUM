import pandas as pd
import re

# Read Excel file and create DataFrame
excel_file = r'Flipkart - Web.xlsx'  # Replace with the actual path to your Excel file
df = pd.read_excel(excel_file)

# Print the original DataFrame
print("Original DataFrame:",df)


# Select a single row from the DataFrame
row_indices = range(len(df))  # I have taken only 0th Index for now
# selected_row = df.iloc[row_index]
dataframes = []
for row_index in row_indices:
    selected_row = df.iloc[row_index]


    # Column which I want to work with
    column_name = 'Execution Steps'
    text = selected_row[column_name]


    # Split text based on digits like 1), 2), 3)....so on
    split_text = []
    current_segment = ""
    for char in text:
        if char.isdigit():
            if current_segment:
                split_text.append(current_segment.strip())
            current_segment = char
        else:
            current_segment += char
    if current_segment:
        split_text.append(current_segment.strip())

    # Convert the list to a new DataFrame
    new_df = pd.DataFrame(split_text, columns=['split_text'])
    for column in new_df.columns:
        new_df[column] = new_df[column].apply(lambda x: re.sub(r'[^a-zA-Z\s]', '', str(x)).lower())


    # import keyword corpus
    keywords_file = r'C:\Users\abdul\PycharmProjects\Automation_Optimum\keywords.txt'  # Replace with the actual path to your text file

    with open(keywords_file, 'r') as file:
        keywords = file.read().splitlines()
        keywords = keywords[0].split(',')
        keywords = [element.lower() for element in keywords]
        print('keywords:',keywords)


    new_column_name = 'Corpus_Keywords'

    # for index, row in new_df.iterrows():
    #     key_list = []
    #     for keyword in keywords:
    #         print(type(keyword))
    #         if keyword in row['split_text']:
    #             key_list.append(keyword)
    #     print(key_list)
    #     new_df.at[index, 'keywords'] = ', '.join(key_list)


    for index, row in new_df.iterrows():
        key_list = []
        for match in re.finditer(r'\b(?:' + '|'.join(keywords) + r')\b', row['split_text'], re.IGNORECASE):
            key_list.append(match.group())
        print(key_list)
        new_df.at[index, 'keywords'] = ', '.join(key_list)

    dataframes.append(new_df)
    print(new_df)


# Combine all the dataframes into a single dataframe
combined_df = pd.concat(dataframes)
print('combined_df:',combined_df)
# Write the combined dataframe to a CSV
combined_df.to_csv("flipkart.csv", index=True)





