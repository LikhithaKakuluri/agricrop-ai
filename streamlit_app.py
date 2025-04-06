import streamlit as st
import pandas as pd
import joblib
import altair as alt
import os
from db import init_db, insert_prediction, fetch_history, fetch_market_prices
import base64

# ========== Page Setup ==========
st.set_page_config(page_title="AgriCrop AI Advisor", layout="wide")

# ========== Initialize DB ==========
init_db()

# ========== Apply Custom Theme ==========
def apply_custom_theme():
    st.markdown("""
        <style>
        body {
            background-color: #2C3E50;
        }
        .custom-box {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
        .custom-label {
            color: #ECF0F1;
            font-weight: bold;
            font-size: 18px;
        }
        input {
            color: white !important;
            font-weight: bold;
        }
        h1, h3, h4 {
            color: #ECF0F1 !important;
            font-weight: bold;
        }
        .stButton>button {
            background-color: #1ABC9C;
            color: white;
            border-radius: 12px;
            padding: 0.5rem 1rem;
            border: none;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #16A085;
        }
        </style>
    """, unsafe_allow_html=True)

apply_custom_theme()

# ========== Background Image ==========
def set_bg_image(image_file):
    with open(image_file, "rb") as file:
        img_data = file.read()
    encoded = base64.b64encode(img_data).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(44, 62, 80, 0.8), rgba(44, 62, 80, 0.8)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

set_bg_image("farm1.jpeg")

# ========== Load Models ==========
@st.cache_resource
def load_models():
    yield_model = joblib.load("ml/models/yield_model.pkl")
    sustainability_model = joblib.load("ml/models/sustainability_model.pkl")
    crop_model = joblib.load("ml/models/crop_recommender.pkl")
    label_encoder = joblib.load("ml/models/crop_label_encoder.pkl")
    return yield_model, sustainability_model, crop_model, label_encoder

yield_model, sustainability_model, crop_model, label_encoder = load_models()

# ========== Sidebar Navigation ==========
tabs = st.sidebar.radio("📍 Navigation", [
    "🏠 Home",
    "🌾 Predict Crop Advice",
    "📜 Prediction History",
    "📈 Market Insights"
])

# ========== Home ==========
if tabs == "🏠 Home":
    st.title("🌱 AgriCrop AI Advisor")
    st.markdown("""
        Welcome to the **AgriCrop AI Advisor** platform! 🌾  
        - Predict best crops based on your farm data.  
        - Estimate yield and sustainability score.  
        - Monitor market trends for better decisions.
    """)

# ========== Crop Advisor ==========
elif tabs == "🌾 Predict Crop Advice":
    st.header("🌿 Enter Farm Data for Predictions")
    with st.form("farm_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            soil_ph = st.number_input("Soil pH", 0.0, 14.0, 6.5)
            temperature = st.number_input("Temperature (°C)", -10.0, 50.0, 25.0)
        with col2:
            soil_moisture = st.number_input("Soil Moisture (%)", 0, 100, 50)
            rainfall = st.number_input("Rainfall (mm)", 0.0, 1000.0, 120.0)
        with col3:
            fertilizer = st.number_input("Fertilizer Usage (kg)", 0.0, 500.0, 50.0)
            pesticide = st.number_input("Pesticide Usage (kg)", 0.0, 100.0, 10.0)

        submit = st.form_submit_button("🚀 Predict")

    if submit:
        input_data = {
            "Soil_pH": soil_ph,
            "Soil_Moisture": soil_moisture,
            "Temperature_C": temperature,
            "Rainfall_mm": rainfall,
            "Fertilizer_Usage_kg": fertilizer,
            "Pesticide_Usage_kg": pesticide,
        }

        X = pd.DataFrame([input_data])
        yield_pred = yield_model.predict(X)[0]
        sustainability_pred = sustainability_model.predict(X)[0]
        crop_pred_encoded = crop_model.predict(X)[0]
        crop_pred = label_encoder.inverse_transform([crop_pred_encoded])[0]
        price_estimate = round(yield_pred * 163.5, 2)

        irrigation_advice = "Use drip irrigation to conserve water." if soil_moisture < 40 else "Flood irrigation may be used."
        fertilizer_tip = "Reduce fertilizer usage for sustainability." if fertilizer > 150 else "Fertilizer usage is optimal."

        st.success("✅ Recommendation complete!")
        st.markdown(f"**🌾 Recommended Crop:** `{crop_pred}`")
        st.markdown(f"**📦 Expected Yield:** `{yield_pred:.2f} tons`")
        st.markdown(f"**💰 Estimated Price:** `₹{price_estimate}`")
        st.markdown(f"**♻️ Sustainability Score:** `{sustainability_pred:.2f}`")
        st.write(f"**💧 Irrigation Advice:** {irrigation_advice}")
        st.write(f"**🧪 Fertilizer Tip:** {fertilizer_tip}")

        insert_prediction(input_data, crop_pred, yield_pred, sustainability_pred)

        # ========== Charts ==========
        st.subheader("📊 Prediction Breakdown")
        chart_df = pd.DataFrame({
            'Metric': ['Yield (tons)', 'Sustainability Score', 'Soil Moisture', 'Fertilizer Usage', 'Pesticide Usage'],
            'Value': [yield_pred, sustainability_pred, soil_moisture, fertilizer, pesticide]
        })

        bar_chart = alt.Chart(chart_df).mark_bar().encode(
            x=alt.X('Metric', sort='-y'),
            y='Value',
            color='Metric'
        ).properties(height=400)

        st.altair_chart(bar_chart, use_container_width=True)

        # ========== Price Comparison ==========
        st.subheader("🏷️ Price Comparison")
        market_df = pd.read_csv("data/market_researcher_dataset.csv")
        product_row = market_df[market_df["Product"] == crop_pred]

        if not product_row.empty:
            market_price = float(product_row["Market_Price_per_ton"].values[0])
            competitor_price = float(product_row["Competitor_Price_per_ton"].values[0])
        else:
            market_price = price_estimate * 1.1
            competitor_price = price_estimate * 0.95

        price_df = pd.DataFrame({
            'Price Type': ['Estimated Price', 'Market Price', 'Competitor Price'],
            'Value (₹/ton)': [price_estimate, market_price, competitor_price]
        })

        price_chart = alt.Chart(price_df).mark_bar().encode(
            x='Price Type',
            y='Value (₹/ton)',
            color='Price Type'
        ).properties(height=350)

        st.altair_chart(price_chart, use_container_width=True)

        # ========== Profit Estimator ==========
        st.subheader("📈 Profit Estimator (Total Revenue)")

        profit_df = pd.DataFrame({
            'Scenario': ['Estimated Price', 'Market Price', 'Competitor Price'],
            'Revenue (₹)': [
                yield_pred * price_estimate,
                yield_pred * market_price,
                yield_pred * competitor_price
            ]
        })

        profit_chart = alt.Chart(profit_df).mark_bar().encode(
            x='Scenario',
            y='Revenue (₹)',
            color='Scenario'
        ).properties(height=350)

        st.altair_chart(profit_chart, use_container_width=True)

# ========== Prediction History ==========
elif tabs == "📜 Prediction History":
    st.header("🕓 Previous Predictions")
    df = fetch_history()
    if df.empty:
        st.warning("No past predictions yet.")
    else:
        st.dataframe(df)
        st.download_button(
            label="⬇️ Download Prediction History CSV",
            data=df.to_csv(index=False),
            file_name="prediction_history.csv",
            mime="text/csv"
        )
        if "recorded_at" in df.columns:
            df["recorded_at"] = pd.to_datetime(df["recorded_at"], errors="coerce")
            yield_chart = alt.Chart(df).mark_line(point=True).encode(
                x="recorded_at:T",
                y="crop_yield_ton:Q",
                color="crop_type:N"
            ).properties(title="🌿 Yield Over Time", height=350)
            st.altair_chart(yield_chart, use_container_width=True)

# ========== Market Insights ==========
elif tabs == "📈 Market Insights":
    st.header("📈 Market Trends & Prices")
    file_path = "data/market_researcher_dataset.csv"

    if not os.path.exists(file_path):
        st.error("🚫 'market_researcher_dataset.csv' not found.")
    else:
        df = pd.read_csv(file_path)
        st.success("✅ Market data loaded.")
        st.dataframe(df)

        st.subheader("💰 Market Price by Product")
        price_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X("Product", sort='-y'),
            y="Market_Price_per_ton",
            color="Product"
        ).properties(height=400)
        st.altair_chart(price_chart, use_container_width=True)

        st.subheader("⚖️ Demand vs Supply Comparison")
        demand_supply = df[["Product", "Demand_Index", "Supply_Index"]].melt("Product", var_name="Type", value_name="Index")
        demand_supply_chart = alt.Chart(demand_supply).mark_bar().encode(
            x="Product",
            y="Index",
            color="Type"
        ).properties(height=400)
        st.altair_chart(demand_supply_chart, use_container_width=True)

        st.subheader("👥 Consumer Trend Index")
        consumer_chart = alt.Chart(df).mark_line(point=True).encode(
            x="Product",
            y="Consumer_Trend_Index",
            color="Product"
        ).properties(height=300)
        st.altair_chart(consumer_chart, use_container_width=True)

        st.subheader("🏷️ Market vs Competitor Pricing")
        comp_price = df[["Product", "Market_Price_per_ton", "Competitor_Price_per_ton"]].melt("Product", var_name="Price_Type", value_name="Price")
        comp_chart = alt.Chart(comp_price).mark_bar().encode(
            x="Product",
            y="Price",
            color="Price_Type"
        ).properties(height=400)
        st.altair_chart(comp_chart, use_container_width=True)

        st.download_button("⬇️ Download Market Data CSV", df.to_csv(index=False), file_name="market_data.csv")
