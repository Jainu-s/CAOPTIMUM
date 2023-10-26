
#Build Model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

'''
This code performs text classification using a Naive Bayes classifier. It loads a dataset, 
splits it into training and testing sets, converts text data into numerical features, trains the 
classifier, saves the model, and later evaluates its accuracy.
'''

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

