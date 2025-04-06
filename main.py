import joblib
import pandas as pd
from ml.utils import normalize_columns

def main():
    # Sample input (you can replace with dynamic input)
    farm_input = {
        "Soil_pH": 7.0,
        "Soil_Moisture": 45.0,
        "Temperature_C": 26.0,
        "Rainfall_mm": 220.0,
        "Fertilizer_Usage_kg": 130.0,
        "Pesticide_Usage_kg": 3.0
    }

    input_df = pd.DataFrame([farm_input])
    input_df = normalize_columns(input_df)

    features = ["Soil_pH", "Soil_Moisture", "Temperature_C", "Rainfall_mm",
                "Fertilizer_Usage_kg", "Pesticide_Usage_kg"]

    # Load models
    yield_model = joblib.load("ml/models/yield_model.pkl")
    sustainability_model = joblib.load("ml/models/sustainability_model.pkl")
    crop_model = joblib.load("ml/models/crop_recommender.pkl")
    label_encoder = joblib.load("ml/models/crop_label_encoder.pkl")

    # Predictions
    X = input_df[features]
    predicted_crop_encoded = crop_model.predict(X)[0]
    predicted_crop = label_encoder.inverse_transform([predicted_crop_encoded])[0]

    predicted_yield = yield_model.predict(X)[0]
    predicted_sustainability = sustainability_model.predict(X)[0]

    # Advice logic (simple example)
    irrigation = "Use drip irrigation to conserve water."
    fertilizer_tip = "Reduce fertilizer usage for sustainability."

    print("\n🌿 FINAL ADVICE")
    print(f"recommended_crop: {predicted_crop}")
    print(f"price_estimate: {round(predicted_yield * 163.5, 2)}")  # Just a dummy estimate
    print(f"irrigation_advice: {irrigation}")
    print(f"fertilizer_tip: {fertilizer_tip}")
    print(f"expected_yield: {predicted_yield}")
    print(f"sustainability_score: {predicted_sustainability}")

if __name__ == "__main__":
    main()
