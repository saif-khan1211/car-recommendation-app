# backend/car_recommender/model.py

import joblib

def load_model(path: str):
    return joblib.load(path)

def predict(model, df):
    probability = model.predict_proba(df)[0][1]
    if probability >= 0.85:
        tier = "Great Buy"
    elif probability >= 0.65:
        tier = "Good Value"
    elif probability >= 0.4:
        tier = "Okay Buy"
    else:
        tier = "Bad Buy"
    return tier, round(probability * 100, 2)
