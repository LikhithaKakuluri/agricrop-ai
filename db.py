import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "db/agri_data.db"
SCHEMA_PATH = "db/schema.sql"
MARKET_DATA_CSV = "data/market_researcher_dataset.csv"

# ========== Initialize Database ==========
def init_db():
    if not os.path.exists(DB_PATH):
        print("🔧 Initializing database...")
    with open(SCHEMA_PATH, "r") as f:
        schema = f.read()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    conn.close()
    print("✅ Database initialized.")

# ========== Insert Prediction into farmer_data ==========
def insert_prediction(farm_data, crop_type, yield_val, sustainability):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO farmer_data (
            soil_ph, soil_moisture, temperature_c, rainfall_mm,
            crop_type, fertilizer_usage_kg, pesticide_usage_kg,
            crop_yield_ton, sustainability_score, recorded_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        farm_data["Soil_pH"],
        farm_data["Soil_Moisture"],
        farm_data["Temperature_C"],
        farm_data["Rainfall_mm"],
        crop_type,
        farm_data["Fertilizer_Usage_kg"],
        farm_data["Pesticide_Usage_kg"],
        yield_val,
        sustainability,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()
    print("📥 Prediction inserted into database.")

# ========== Fetch Past Predictions ==========
def fetch_history():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM farmer_data ORDER BY id DESC", conn)
    conn.close()
    return df

# ========== Fetch Market Prices ==========
def fetch_market_prices():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM market_data", conn)
    conn.close()
    return df

# ========== Populate Market Data (Optional) ==========
def populate_market_data_from_csv():
    if not os.path.exists(MARKET_DATA_CSV):
        print("🚫 'market_researcher_dataset.csv' not found. Skipping market data population.")
        return

    df = pd.read_csv(MARKET_DATA_CSV)
    conn = sqlite3.connect(DB_PATH)

    df.to_sql("market_data", conn, if_exists="replace", index=False)
    conn.close()
    print("✅ Market data populated from CSV.")
