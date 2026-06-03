import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

data = pd.read_csv(
    "backend/app/database/candidate_dataset.csv"
)

X = data[["resume_score", "interview_score"]]
y = data["result"]

model = DecisionTreeClassifier()

model.fit(X, y)

joblib.dump(model, "candidate_model.pkl")

print("Model Trained Successfully!")