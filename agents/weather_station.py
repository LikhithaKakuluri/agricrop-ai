def summarize_weather(farmer_row):
    return {
        "temperature": farmer_row["Temperature_C"],
        "rainfall": farmer_row["Rainfall_mm"],
        "summary": "Moderate climate, expect medium yield"
    }
