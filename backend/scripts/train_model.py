import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import mlflow
import mlflow.sklearn
from sklearn.metrics import precision_score, recall_score, f1_score


# ✅ Step 1: Load the dataset directly from local KaggleHub cache
dataset_path = os.path.expanduser(
    "~/.cache/kagglehub/datasets/ayazlakho/carsdataset/versions/1/new-used-cars-dataset.csv"
)
df = pd.read_csv(dataset_path)

# ✅ Step 2: Normalize column names (lowercase, underscores)
df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

# ✅ Step 3: Convert numeric-looking columns from strings to numbers
df["mileages"] = pd.to_numeric(df["mileages"].str.replace(",", "").str.extract(r"(\d+)")[0], errors="coerce")
df["ratings"] = pd.to_numeric(df["ratings"], errors="coerce")
df["price"] = pd.to_numeric(df["price"].str.replace(",", "").str.extract(r"(\d+)")[0], errors="coerce")
df["price_drop"] = pd.to_numeric(df["price_drop"].str.replace(",", "").str.extract(r"(\d+)")[0], errors="coerce")

# ✅ Step 4: Drop rows with missing required fields
df = df.dropna(subset=["mileages", "ratings", "price", "used/certified", "price_drop"])

# ✅ Step 5: Normalize certification column
df["used/certified"] = df["used/certified"].str.lower().str.strip()

# ✅ Step 6: Define 'recommend' label using simple business logic
df["recommend"] = (
    (df["ratings"] >= 4.0).astype(int) +
    (df["mileages"] <= 80000).astype(int) +
    (df["price"] < df["price"].median()).astype(int) +
    (df["price_drop"] > 500).astype(int) +
    (df["used/certified"].str.contains("certified")).astype(int)
) >= 3

df["recommend"] = df["recommend"].astype(int)

# ✅ Step 7: Create binary 'certified' feature for model input
df["certified"] = (df["used/certified"] == "certified").astype(int)

# ✅ Step 8: Define model inputs and outputs
X = df[["mileages", "ratings", "price", "certified", "price_drop"]]
y = df["recommend"]

# ✅ Step 9: Split data into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ✅ Step 10: Train the RandomForest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# ✅ Step 11: Save model and cleaned data
df.to_csv("backend/model/cleaned_cars.csv", index=False)
joblib.dump(model, "backend/model/car_model.pkl")
