import joblib
import os

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "models",
    "candidate_model.pkl"
)

model = joblib.load(MODEL_PATH)


def predict_candidate(
    resume_score,
    interview_score
):

    prediction = model.predict(
        [[resume_score, interview_score]]
    )

    return prediction[0]