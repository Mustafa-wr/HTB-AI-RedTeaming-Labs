import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import re

# --- Load JSON files ---
with open("skills_assessment_data/train.json", "r", encoding="utf-8") as f:
    train_data = json.load(f)

with open("skills_assessment_data/test.json", "r", encoding="utf-8") as f:
    test_data = json.load(f)

# --- Convert to DataFrame ---
train_df = pd.DataFrame(train_data)
test_df = pd.DataFrame(test_data)

# --- Clean text function ---
def clean_text(text):
    text = re.sub(r"<.*?>", " ", text)  # remove HTML tags
    text = re.sub(r"\s+", " ", text)    # remove extra spaces
    return text.strip()

train_df['text'] = train_df['text'].apply(clean_text)
test_df['text'] = test_df['text'].apply(clean_text)

# --- Vectorize ---
vectorizer = TfidfVectorizer(max_features=5000)
X_train = vectorizer.fit_transform(train_df['text'])
X_test = vectorizer.transform(test_df['text'])

y_train = train_df['label']
y_test = test_df['label']

# --- Train model ---
clf = RandomForestClassifier(n_estimators=200, random_state=42)
clf.fit(X_train, y_train)

# --- Evaluate ---
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict=True)

# Misclassified samples
misclassified = test_df[y_test != y_pred]

# --- Results ---
results = {
    "accuracy": accuracy,
    "metrics": report,
    "misclassified": misclassified.to_dict(orient="records")
}

print(results)