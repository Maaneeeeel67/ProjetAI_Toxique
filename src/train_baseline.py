import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline

# charger dataset
df = pd.read_csv("data/train.csv")

X = df["comment_text"]
y = df["toxic"]

# division train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# pipeline modèle
model = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", max_features=50000)),
    ("clf", LogisticRegression(max_iter=1000))
])

print("Training model...")

model.fit(X_train, y_train)

print("Prediction...")

pred = model.predict(X_test)

print("\nModel evaluation:\n")
print(classification_report(y_test, pred))