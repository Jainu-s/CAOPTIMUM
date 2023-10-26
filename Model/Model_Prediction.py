# MODEL PREDICTION
import re

import joblib
import pandas as pd

#
# def model_prediction(df):
#
#     # Find the column with "Steps" or "steps"
#     steps_column = None
#     for column in df.columns:
#         if 'Steps' in column or 'steps' in column:
#             steps_column = column
#             break
#
#     if steps_column is None:
#         print("No column with 'Steps' or 'steps' found in the dataframe.")
#     else:
#         # Create a new dataframe to store the splitted data
#         new_rows = []
#
#         # Loop through each row
#         for index, row in df.iterrows():
#             try:
#                 # Split the text based on the given formats and remove numbering
#                 text = row[steps_column]
#                 print('text:', text)
#                 steps = re.split(r'\d+[\.)]', text)
#                 steps = [step.strip() for step in steps if step.strip()]
#
#                 # Find the URL in the row
#                 url = None
#                 for col in row.index:
#                     print('col:', col)
#                     if 'http' in str(row[col]):
#                         url = str(row[col])
#                         break
#
#                 # Clean the URL to remove any text
#                 if url:
#                     url = re.search(r'(https?://\S+)', url)
#                     if url:
#                         url = url.group(0)
#
#                 # Create a new row for each splitted text and URL
#                 for step_text in steps:
#                     new_row = {'Text': step_text, 'URL': url}
#                     new_rows.append(new_row)
#             except:
#                 pass
#         new_df = pd.DataFrame(new_rows, columns=['Text', 'URL', 'Data'])
#         print(new_df)
#
#         # Load the saved model and vectorizer
#         loaded_model = joblib.load('naive_bayes_model.joblib')
#         loaded_vectorizer = joblib.load('vectorizer.joblib')
#
#         # Transform the new data using the loaded vectorizer
#         new_data = new_df['Text']
#         url = new_df['URL']
#         new_data_vector = loaded_vectorizer.transform(new_data)
#
#         # Make predictions on the new data
#         predictions = loaded_model.predict(new_data_vector)
#
#         # Create a DataFrame with document and prediction pairs
#         results_df = pd.DataFrame({'Document': range(1, len(predictions) + 1),
#                                    'Url': url,
#                                    'Text': new_data,
#                                    'Prediction': predictions})
#
#         # Save the results to a CSV file
#         results_df.to_csv('predictions.csv', index=False)
#         print("Predictions saved to predictions.csv")
#         return results_df

import pandas as pd
import re
import joblib
import pandas as pd
import re
import joblib

import pandas as pd
import re
import joblib

'''
This code takes a DataFrame loaded from a CSV file, processes the text data in one of its columns,
 and makes predictions on that text using a previously trained Naive Bayes classifier. It splits 
 the text, cleans the URL, and assigns labels. The results are saved to a CSV file named
  "predictions.csv," and the resulting DataFrame is returned
'''

def model_prediction(df):
    print(df.columns)
    # Find the column with "Steps" or "steps"
    steps_column = None
    for column in df.columns:
        if 'steps' in column.lower():
            steps_column = column
            break

    if steps_column is None:
        print("No column with 'Steps' or 'steps' found in the dataframe.")
        return None

    # Create a new dataframe to store the splitted data
    new_rows = []

    # Loop through each row
    for index, row in df.iterrows():
        try:
            # Split the text based on the given formats and remove numbering
            text = row[steps_column]
            steps = re.split(r'\d+[\.)]', text)
            steps = [step.strip() for step in steps if step.strip()]

            # Find the URL in the row
            url = None
            for col in row.index:
                if 'http' in str(row[col]):
                    url = str(row[col])
                    break

            # Clean the URL to remove any text
            if url:
                url = re.search(r'(https?://\S+)', url)
                if url:
                    url = url.group(0)

            # assign label
            label = row['Label']

            # Create a new row for each splitted text, URL, and label
            for step_text in steps:
                new_row = {'Text': step_text, 'URL': url, 'Label': label}
                new_rows.append(new_row)
        except:
            pass

    new_df = pd.DataFrame(new_rows, columns=['Text', 'URL', 'Label'])


    # Load the saved model and vectorizer
    loaded_model = joblib.load(r'C:\Users\Optimum.LAPTOP-SQLU1RCT\PycharmProjects\FAP\CAOPTIMUM\Model\naive_bayes_model.joblib')
    loaded_vectorizer = joblib.load(r'C:\Users\Optimum.LAPTOP-SQLU1RCT\PycharmProjects\FAP\CAOPTIMUM\Model\vectorizer.joblib')

    # Transform the new data using the loaded vectorizer
    new_data = new_df['Text']
    new_data_vector = loaded_vectorizer.transform(new_data)

    # Make predictions on the new data
    predictions = loaded_model.predict(new_data_vector)

    # Create a DataFrame with document, URL, text, label, and prediction pairs
    results_df = pd.DataFrame({'Document': range(1, len(predictions) + 1),
                               'URL': new_df['URL'],
                               'Text': new_data,
                               'Label': new_df['Label'],
                               'Prediction': predictions})

    # Save the results to a CSV file
    results_df.to_csv('predictions.csv', index=False)
    print("Predictions saved to predictions.csv")
    return results_df



df = pd.read_csv('excel_to_df.csv')
print(model_prediction(df))


