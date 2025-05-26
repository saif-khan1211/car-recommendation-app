# backend/car_recommender/preprocessing.py

import pandas as pd

def preprocess_input(data):
    """
    Convert raw user input into a DataFrame with proper column names and format
    """
    df = pd.DataFrame([data])  # Convert single dict to one-row DataFrame

    # Normalize certification
    df['certified'] = df['certified'].str.lower().str.strip()
    df['certified'] = (df['certified'] == 'certified').astype(int)

    # Rename to match trained model
    df = df.rename(columns={
        "mileage": "mileages",
        "rating": "ratings",
        "price drop": "price_drop"
    })

    # Return columns in expected order
    return df[["mileages", "ratings", "price", "certified", "price_drop"]]
