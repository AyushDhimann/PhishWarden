import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, precision_score
import joblib
import requests
import time

# Start Time
start_time = time.perf_counter()

from Scraper import url, ssl, age, status_code, blacklisted_words

# Load the saved model
clf = joblib.load('phishing_model.joblib')

# Define the feature column names expected by the preprocessor
feature_cols = ['url', 'ssl', 'age', 'status_code', 'blacklisted_words']

# Create a DataFrame from the feature data
features = [[url, ssl, age, status_code, blacklisted_words]]
test_data = pd.DataFrame(features, columns=feature_cols)

# Load the dataset
data = pd.read_csv('Shuffled.csv')

# Separate the features and target variable
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# Preprocess the numerical features using StandardScaler
numerical_features = ['ssl', 'age', 'status_code']
numerical_transformer = StandardScaler()

# Preprocess the categorical feature using OneHotEncoder
categorical_features = ['url']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Preprocess the text feature using CountVectorizer
text_features = 'blacklisted_words'
text_transformer = CountVectorizer()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features),
        ('text', text_transformer, text_features)
    ])

# Preprocess the data using the preprocessor
X = preprocessor.fit_transform(X)
test_X = preprocessor.transform(test_data)

# Predict the phishing status of the test website
test_y_pred = clf.predict(test_X)

is_phish = ""

if test_y_pred[0] == 1:
    print("The website is predicted to be a phishing website.")
    is_phish = "yes"
else:
    print("The website is predicted to be a legitimate website.")
    is_phish = "no"

# Calculate accuracy and precision
accuracy = accuracy_score(y, clf.predict(X))
precision = precision_score(y, clf.predict(X))

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")

from Encrypt import encrypt_data
result = encrypt_data(is_phish)
cleanedResult = result + "=="
print("Result is ", cleanedResult)

#ext_url = 'https://eokdhydqf6vxow0.m.pipedream.net'
#data = {'is_phish': cleanedResult}

#response = requests.post(ext_url, data=data)

#print(response.status_code)

# Record the end time
end_time = time.perf_counter()

# Calculate the elapsed time
elapsed_time = end_time - start_time

print(f"\033[0;32mTotal Time Taken: {elapsed_time:.6f} seconds\033[0;32m")
