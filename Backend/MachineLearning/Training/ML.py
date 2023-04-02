# Import necessary libraries
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.compose import ColumnTransformer
import joblib

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

# Train the model on the full dataset
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X, y)

# Save the trained model to a file
joblib.dump(clf, 'phishing_model.joblib')

# Create a new dataframe with the features of the website you want to test
test_data = pd.DataFrame({
    'url': ['google.com'],
    'ssl': [1],
    'age': [5400],
    'status_code': [200],
    'blacklisted_words': ['']
})

# Preprocess the test data using the preprocessor
test_X = preprocessor.transform(test_data)

# Predict the phishing status of the test website
test_y_pred = clf.predict(test_X)

# Print the predicted phishing status of the test website
print('Predicted phishing status:', test_y_pred[0])

#
# # Load the dataset
# data = pd.read_csv('Shuffled.csv')
#
# # Separate the features and target variable
# X = data.iloc[:, :-1]
# y = data.iloc[:, -1]
#
# # Preprocess the numerical features using StandardScaler
# numerical_features = ['ssl', 'age', 'status_code']
# numerical_transformer = StandardScaler()
#
# # Preprocess the categorical feature using OneHotEncoder
# categorical_features = ['url']
# categorical_transformer = OneHotEncoder(handle_unknown='ignore')
#
# # Preprocess the text feature using CountVectorizer
# text_features = 'blacklisted_words'
# text_transformer = CountVectorizer()
#
# preprocessor = ColumnTransformer(
#     transformers=[
#         ('num', numerical_transformer, numerical_features),
#         ('cat', categorical_transformer, categorical_features),
#         ('text', text_transformer, text_features)
#     ])
#
# # Preprocess the data using the preprocessor
# X = preprocessor.fit_transform(X)
#
# # Train the model on the full dataset
# clf = RandomForestClassifier(n_estimators=100, random_state=42)
# clf.fit(X, y)
#
# # Make predictions on the same dataset to evaluate the model performance
# y_pred = clf.predict(X)
# accuracy = accuracy_score(y, y_pred)
# print('Accuracy on the full dataset:', round(accuracy * 100, 2), '%')
#
# # Calculate the F1 score of the model on the full dataset
# f1 = f1_score(y, y_pred)
# print('F1 score on the full dataset:', round(f1 * 100, 2), '%')