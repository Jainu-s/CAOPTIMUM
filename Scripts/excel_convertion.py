# import pandas as pd
# import re
#
# def excel_utitlity(excel_file_path):
#
#     def find_test_id_column(df):
#         for column in df.columns:
#             if "test id" in column.lower() or "test case id" in column.lower() or "id" in column.lower():
#                 return column
#         return None
#
#     def find_steps_column(df):
#         for column in df.columns:
#             if "steps" in column.lower():
#                 return column
#         return None
#
#     # Replace 'your_file_path.xlsx' with the actual file path of your Excel sheet
#     file_path = excel_file_path
#
#
#     # Read the Excel files into DataFrames using openpyxl engine
#     df = pd.read_excel(file_path, engine='openpyxl')
#     credentials_df = pd.read_excel(file_path, engine='openpyxl')
#
#     # Find the columns with test IDs and steps
#     test_id_column = find_test_id_column(df)
#     steps_column = find_steps_column(df)
#
#     # Create a new DataFrame using the identified column names
#     new_df = df[[test_id_column, steps_column]]
#
#     # Split the steps column into new rows
#     new_df[steps_column] = new_df[steps_column].apply(lambda x: re.split(r'\d+\)|\d+\.', x))
#
#     # Explode the steps column to create new rows
#     new_df = new_df.explode(steps_column)
#
#     # Forward-fill the test IDs for the new rows
#     new_df[test_id_column] = new_df[test_id_column].ffill()
#
#     # Rename the columns to 'ID' and 'STEPS'
#     new_df.rename(columns={test_id_column: 'Label'}, inplace=True)
#
#     return new_df



import pandas as pd
import re

def find_url(s):
    if not isinstance(s, (str, bytes)):
        return []  # Return an empty list if s is not a string or bytes-like object

    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return url_pattern.findall(s)

def excel_utitlity(excel_file_path):

    def find_test_id_column(df):
        for column in df.columns:
            if "test id" in column.lower() or "test case id" in column.lower() or "id" in column.lower():
                return column
        return None

    def find_steps_column(df):
        for column in df.columns:
            if "steps" in column.lower():
                return column
        return None

    # Replace 'your_file_path.xlsx' with the actual file path of your Excel sheet
    file_path = excel_file_path

    # Read the Excel files into DataFrames using try-except to handle errors
    df = pd.read_excel(file_path, engine='openpyxl')

    # Find the columns with test IDs and steps
    test_id_column = find_test_id_column(df)
    steps_column = find_steps_column(df)

    if test_id_column is None or steps_column is None:
        print("Error: Test ID or Steps column not found in the Excel file.")
        return None

    # Create a new DataFrame using the identified column names
    new_df = df[[test_id_column, steps_column]]

    # Split the steps column into new rows
    new_df[steps_column] = new_df[steps_column].apply(lambda x: re.split(r'\d+\)|\d+\.', x))

    # Explode the steps column to create new rows
    new_df = new_df.explode(steps_column)

    # Forward-fill the test IDs for the new rows
    new_df[test_id_column] = new_df[test_id_column].ffill()

    # Rename the columns to 'Label' and 'STEPS'
    new_df.rename(columns={test_id_column: 'Label', steps_column: 'STEPS'}, inplace=True)

    # Add a new column 'URL' to store URLs
    new_df['URL'] = ''


    # Loop through the DataFrame to find and update URLs
    for index, row in df.iterrows():
        for column in df.columns:
            if column != test_id_column and column != steps_column:
                urls = find_url(row[column])
                if urls:
                    url_to_update = urls[0]  # Considering only the first URL if multiple URLs are found
                    test_id = row[test_id_column]
                    # Update the URL in the new_df for the corresponding test ID
                    new_df.loc[new_df['Label'] == test_id, 'URL'] = url_to_update
    new_df.to_csv('new_df.csv',index=False)
    return new_df


# test_case_path = r'C:\Users\abdul\PycharmProjects\Automation_Optimum\CredX _ TestCase _.xlsx'
# print(excel_utitlity(test_case_path))
