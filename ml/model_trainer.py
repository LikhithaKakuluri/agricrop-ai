import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.utils import normalize_columns
from ml.utils import normalize_columns

def train_yield_model():
    df = pd.read_csv("data/farmer_advisor_dataset.csv")
    df = normalize_columns(df)

    print("✅ Normalized Columns:", list(df.columns))  # Debug

    features = ["Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm",
                "Fertilizer_Usage_kg", "Pesticide_Usage_kg"]
    target = "Crop_Yield_ton"

    for col in features + [target]:
        if col not in df.columns:
            raise ValueError(f"❌ Column '{col}' is missing.")

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "ml/yield_predictor.pkl")
    print("✅ Yield model trained and saved.")

def train_sustainability_model():
    df = pd.read_csv("data/farmer_advisor_dataset.csv")
    df = normalize_columns(df)

    features = ["Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm",
                "Fertilizer_Usage_kg", "Pesticide_Usage_kg"]
    target = "Sustainability_Score"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "ml/sustainability_predictor.pkl")
    print("✅ Sustainability model trained and saved.")

def train_crop_recommender():
    df = pd.read_csv("data/farmer_advisor_dataset.csv")
    df = normalize_columns(df)

    features = ["Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm",
                "Fertilizer_Usage_kg", "Pesticide_Usage_kg"]
    target = "Crop_Type"

    le = LabelEncoder()
    df[target] = le.fit_transform(df[target])

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    joblib.dump(model, "ml/crop_recommender.pkl")
    joblib.dump(le, "ml/crop_label_encoder.pkl")
    print("✅ Crop recommender model trained and saved.")

if __name__ == "__main__":
    train_yield_model()
    train_sustainability_model()
    train_crop_recommender()
