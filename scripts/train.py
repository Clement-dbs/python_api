from sklearn.datasets import load_iris
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import json
from datetime import datetime

data = load_iris()

X = data.data
y = data.target

print(X)
print(y)

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
) 

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

# Entrainement
rfc_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)

rfc_model.fit(X_train, y_train)
y_pred = rfc_model.predict(X_test)

# Metrics
accuracy_score_metric = accuracy_score(y_test, y_pred)
precision_score_metric = precision_score(y_test, y_pred, average="macro")
recall_score_metric = recall_score(y_test, y_pred, average="macro")
f1_score_metric = f1_score(y_test, y_pred, average="macro")

cr = classification_report(y_test, y_pred=y_pred)
cm = confusion_matrix(y_test, y_pred)

print(cr)
print(cm)

labels = data.target_names

# Visualisation
# fig, ax = plt.subplots(figsize=(8, 6))
# sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
#             xticklabels=labels,
#             yticklabels=labels,
#             ax=ax)
# plt.tight_layout()
# plt.show()

# Save
with open("./models/model.pkl", "wb") as f:
    pickle.dump(rfc_model, f)

with open("./models/training_report.json", "w") as f:
    json.dump({
        "accuracy_score" : accuracy_score_metric,
        "precision_score" : precision_score_metric,
        "recall_score" : recall_score_metric,
        "f1_score_score" : f1_score_metric,
        "date": datetime.now().isoformat()
    }, f, indent=4)