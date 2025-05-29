import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load CSV
df = pd.read_csv("student_data.csv")

# Convert marks to performance labels
def label_strength(marks):
    if marks >= 80:
        return "Strong"
    elif marks >= 60:
        return "Moderate"
    else:
        return "Weak"

df["Label"] = df["Marks"].apply(label_strength)

# Train model
X = df[["Marks"]]
y = df["Label"]
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
with open("study_model.pkl", "wb") as f:
    pickle.dump(model, f)
