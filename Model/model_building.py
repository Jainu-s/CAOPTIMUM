
#Build Model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
data = pd.read_csv('ml_model.csv')


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['inputs'], data['action'], test_size=0.2, random_state=42)

# Convert text data into numerical features using CountVectorizer
vectorizer = CountVectorizer()
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

# Train the Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train_vectors, y_train)

# Save the trained model to a file
joblib.dump(classifier, r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Model\naive_bayes_model.joblib')
joblib.dump(vectorizer, r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Model\vectorizer.joblib')

# Load the saved model and vectorizer
loaded_model = joblib.load(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Model\naive_bayes_model.joblib')
loaded_vectorizer = joblib.load(r'C:\Users\abdul\PycharmProjects\Automation_Optimum\Model\vectorizer.joblib')

# Make predictions on the test set
y_pred = loaded_model.predict(X_test_vectors)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)



# import pandas as pd
# import re
# import joblib
#
# # Load the Excel sheet
# data = pd.read_csv('testing.csv')
#
# # Find the column containing the word "Steps"
# steps_column = next((col for col in data.columns if 'Steps' in col), None)
#
# if steps_column:
#     # Create a list to store the split steps
#     split_steps = []
#
#     # Iterate over each row in the dataframe
#     for _, row in data.iterrows():
#         # Check if the "Steps" column has a value
#         if pd.notnull(row[steps_column]):
#             # Split the steps based on the step numbering pattern
#             steps = re.split(r'(?<=\d\)|\d\.)', row[steps_column])
#             steps = [step.strip() for step in steps if step.strip()]
#
#             # Remove step numbering and URLs from each step
#             steps = [re.sub(r'^\d+\)|\d+\.', '', step) for step in steps]
#             steps = [re.sub(r'http[s]?://\S+', '', step) for step in steps]
#
#             # Append the non-empty steps for the current row to the overall list
#             split_steps.extend(step.strip() for step in steps if step.strip())
#
#     if split_steps:
#         # Create a new DataFrame with the split steps
#         split_df = pd.DataFrame({steps_column: split_steps})
#
#         # Load the saved model and vectorizer
#         loaded_model = joblib.load('naive_bayes_model.joblib')
#         loaded_vectorizer = joblib.load('vectorizer.joblib')
#
#         # Transform the new data using the loaded vectorizer
#         new_data = split_df[steps_column]
#         new_data_vector = loaded_vectorizer.transform(new_data)
#
#         # Make predictions on the new data
#         predictions = loaded_model.predict(new_data_vector)
#
#         # Create a DataFrame with document and prediction pairs
#         results_df = pd.DataFrame({'Document': range(1, len(predictions) + 1),
#                                    'Text': new_data,
#                                    'Prediction': predictions})
#
#         # Save the results to a CSV file
#         results_df.to_csv('predictions.csv', index=False)
#         print("Predictions saved to predictions.csv")
#     else:
#         print("No text found after splitting the steps.")
# else:
#     print("No column with 'Steps' found in the Excel sheet.")


