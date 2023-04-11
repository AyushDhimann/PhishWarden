import pandas as pd
import joblib
from ML import preprocessor

# Load the saved model from a file
clf = joblib.load('phishing_model.joblib')

# Define the feature column names expected by the preprocessor
feature_cols = ['url', 'ssl', 'age', 'status_code', 'blacklisted_words']

# Create a DataFrame from the feature data
url = input("Enter the URL: ")#'https://www.aljazeera.com/'
ssl = input("Enter the SSL Status: ")#1
age = input("Enter the Age(in days): ")#100
status_code = input("Enter the Status Code: ")#200www.google.com
blacklisted_words = input("Enter the Blacklisted Words if any: ")#'login,verify'
features = [[url, ssl, age, status_code, blacklisted_words]]
X_test = pd.DataFrame(features, columns=feature_cols)

# Preprocess the website features
X_test = preprocessor.transform(X_test)

# Predict the phishing status of the website
y_pred = clf.predict(X_test)

if y_pred[0] == 1:
    print("The website is predicted to be a phishing website.")
else:
    print("The website is predicted to be a legitimate website.")
