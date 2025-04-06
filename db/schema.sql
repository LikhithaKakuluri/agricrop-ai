-- Table: farmer_data
CREATE TABLE IF NOT EXISTS farmer_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farm_id INTEGER,
    soil_ph REAL,
    soil_moisture REAL,
    temperature_c REAL,
    rainfall_mm REAL,
    crop_type TEXT,
    fertilizer_usage_kg REAL,
    pesticide_usage_kg REAL,
    crop_yield_ton REAL,
    sustainability_score REAL,
    recorded_at TEXT
);

-- Table: market_data
CREATE TABLE IF NOT EXISTS market_data (
    market_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    market_price_per_ton REAL,
    demand_index REAL,
    supply_index REAL,
    competitor_price_per_ton REAL,
    economic_indicator REAL,
    weather_impact_score REAL,
    seasonal_factor TEXT,
    consumer_trend_index REAL
);

-- Table: advice_logs
CREATE TABLE IF NOT EXISTS advice_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT,
    timestamp TEXT,
    farm_id INTEGER,
    advice TEXT,
    FOREIGN KEY (farm_id) REFERENCES farmer_data(farm_id)
);
