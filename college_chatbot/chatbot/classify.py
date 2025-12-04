import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

# 1. Load the dataset from CSV
data_path = "college_chatbot\\ace_college_query_dataset.csv"  # Make sure this path points to your CSV file
df = pd.read_csv(data_path)

# 2. Basic dataset info
print(f"Total queries: {len(df)}")
print(f"Unique categories: {df['category'].nunique()}")
print("Sample data:")
print(df.head())

# 3. Prepare features (X) and labels (y)
X = df['query']
y = df['category']

# 4. Encode labels to integers for classifier
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# 5. Split dataset into training and testing sets (80%-20%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# 6. Build a Pipeline with TfidfVectorizer and LinearSVC
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(
        stop_words='english',
        max_df=0.85,     # ignore very common words
        min_df=2,        # ignore very rare words
        ngram_range=(1, 2)  # consider unigrams and bigrams
    )),
    ('clf', LinearSVC(random_state=42))
])

# 7. Train the model
print("Training the model...")
pipeline.fit(X_train, y_train)

# 8. Evaluate the model on test set
y_pred = pipeline.predict(X_test)
# print("\nClassification Report:")
# print(classification_report(y_test, y_pred, target_names=label_encoder.classes_, zero_division=0))

# 9. Function to classify new queries
def classify_query(query):
    pred_encoded = pipeline.predict([query])[0]
    category = label_encoder.inverse_transform([pred_encoded])[0]
    return category
