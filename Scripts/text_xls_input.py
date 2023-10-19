import pandas as pd
import re

def split_steps_description(data):
    # Find the index of the "Steps Description" heading
    steps_index = data.index("Steps Description:") + 1

    # Get the content under the "Steps Description" heading
    steps_description = data[steps_index].strip()

    # Split the content based on commas, "and," or full stops
    steps = re.split(r',|\sand\s|\.', steps_description)

    # Clean up the steps (remove leading/trailing spaces)
    steps = [step.strip() for step in steps if step.strip()]

    return steps

def text_input(file):
    # Read the text data from an Excel file
    df = pd.read_excel(file)

    # Get the steps description from the DataFrame
    steps_description = df.loc[df['Column'] == "Steps Description", 'Value'].iloc[0].strip()

    # Split the content into steps
    steps = split_steps_description([steps_description])

    # Convert steps to DataFrame
    df_steps = pd.DataFrame(steps, columns=["Steps"])

    # Find credentials in the DataFrame and add them to a dictionary
    credentials_df = df.loc[df['Column'] == "Data"]
    credentials = {}
    for _, row in credentials_df.iterrows():
        key = row['Key'].strip()
        value = row['Value'].strip()
        credentials[key] = value

    # Update the "Data" column based on the keys in the steps
    df_steps['Data'] = df_steps['Steps'].apply(lambda x: ', '.join([credentials[key.strip()] for key in credentials.keys() if key.strip() in x]) or 'N/A')

    # Print the updated DataFrame
    print(df_steps)
    df_steps.to_csv('text_input_file.csv', index=False)
    return df_steps

text_input('credentials.xlsx')
