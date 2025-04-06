def generate_advice(farmer_row, market_row):
    crop = market_row["Product"]
    advice = {
        "recommended_crop": crop,
        "price_estimate": market_row["Market_Price_per_ton"],
        "irrigation_advice": "Use drip irrigation to conserve water.",
        "fertilizer_tip": "Reduce fertilizer usage for sustainability.",
        "expected_yield": farmer_row["Crop_Yield_ton"],
        "sustainability_score": farmer_row["Sustainability_Score"]
    }
    return advice
