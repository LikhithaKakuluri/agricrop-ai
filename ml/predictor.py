import joblib
import numpy as np
from ml.utils import normalize_columns
import pandas as pd

def load_model(path):
    return joblib.load(path)

def predict_yield(farm_input):
    model = load_model("ml/yield_predictor.pkl")
    features = np.array([[farm_input[col] for col in [
        "Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm",
        "Fertilizer_Usage_kg", "Pesticide_Usage_kg"
    ]]])
    return model.predict(features)[0]

def predict_sustainability(farm_input):
    model = load_model("ml/sustainability_predictor.pkl")
    features = np.array([[farm_input[col] for col in [
        "Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm",
        "Fertilizer_Usage_kg", "Pesticide_Usage_kg"
    ]]])
    return model.predict(features)[0]

def recommend_crop(farm_input):
    model = load_model("ml/crop_recommender.pkl")
    encoder = load_model("ml/crop_label_encoder.pkl")
    features = np.array([[farm_input[col] for col in [
        "Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm",
        "Fertilizer_Usage_kg", "Pesticide_Usage_kg"
    ]]])
    prediction = model.predict(features)[0]
    return encoder.inverse_transform([prediction])[0]
