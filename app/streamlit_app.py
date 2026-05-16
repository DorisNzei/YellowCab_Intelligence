import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(
    page_title="NYC Yellow Taxi Duration Predictor",
    page_icon="🚕",
    layout="centered"
)

st.markdown("""
<style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1534430480872-3498386e7856?w=1600");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.75);
        z-index: 0;
    }
    .block-container { position: relative; z-index: 1; }
    .main-title {
        font-size: 2.5em; font-weight: 900;
        color: #FFD700; text-align: center;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        padding: 20px 0;
    }
    .subtitle {
        font-size: 1.1em; color: #cccccc;
        text-align: center; margin-bottom: 30px;
    }
    .taxi-banner {
        background: linear-gradient(90deg, #FFD700, #FFA500);
        padding: 15px; border-radius: 10px;
        text-align: center; font-size: 1.3em;
        font-weight: bold; color: #000000;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(255,215,0,0.4);
    }
    .result-box {
        background: linear-gradient(135deg, #1e3a5f, #0d2137);
        border: 2px solid #FFD700; border-radius: 15px;
        padding: 25px; text-align: center; margin: 20px 0;
        box-shadow: 0 0 20px rgba(255,215,0,0.3);
    }
    .stButton > button {
        background: linear-gradient(90deg, #FFD700, #FFA500) !important;
        color: black !important; font-weight: bold !important;
        font-size: 1.2em !important; border-radius: 10px !important;
        border: none !important; padding: 15px !important;
    }
    .footer {
        text-align: center; color: #888888;
        font-size: 0.85em; margin-top: 30px;
        padding: 10px; border-top: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("models/lightgbm_model.pkl")

@st.cache_data
def load_zones():
    return pd.read_csv("data/taxi_zone_lookup.csv")

model = load_model()
zones = load_zones()

st.markdown('<div class="main-title">🚕 NYC Yellow Taxi</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Trip Duration Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Powered by LightGBM • Trained on 46 Million NYC Trips</div>', unsafe_allow_html=True)
st.markdown('<div class="taxi-banner">🌆 New York City • 2025 • Live Prediction Engine</div>', unsafe_allow_html=True)

st.divider()

zone_options = zones[["LocationID", "Zone"]].copy()
zone_options["display"] = zone_options["Zone"] + " (ID: " + zone_options["LocationID"].astype(str) + ")"

col1, col2 = st.columns(2)

with col1:
    pickup_zone = st.selectbox("📍 Pickup Zone", zone_options["display"].tolist())
    hour = st.slider("🕐 Hour of Day", 0, 23, 8)
    is_rush = st.checkbox("🚦 Rush Hour? (7-9am or 5-7pm)")

with col2:
    dropoff_zone = st.selectbox("🏁 Dropoff Zone", zone_options["display"].tolist())
    day = st.selectbox("📅 Day of Week",
                       ["Monday","Tuesday","Wednesday",
                        "Thursday","Friday","Saturday","Sunday"])
    is_weekend = 1 if day in ["Saturday","Sunday"] else 0

pu_id = zone_options[zone_options["display"] == pickup_zone]["LocationID"].values[0]
do_id = zone_options[zone_options["display"] == dropoff_zone]["LocationID"].values[0]
day_num = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"].index(day)

st.divider()

if st.button("🔮 Predict My Trip Duration", use_container_width=True):
    features = pd.DataFrame([{
        "trip_distance": 2.5,
        "pickup_hour": hour,
        "day_of_week": day_num,
        "month": 6,
        "is_weekend": is_weekend,
        "is_rush_hour": 1 if is_rush else 0,
        "route_avg_duration": 15.0,
        "congestion_fee_flag": 1 if pu_id in range(4, 100) else 0,
        "PULocationID": pu_id,
        "DOLocationID": do_id
    }])

    prediction = model.predict(features)[0]

    st.markdown(f"""
    <div class="result-box">
        <div style="font-size:1.2em; color:#FFD700; margin-bottom:10px">🚕 Estimated Trip Duration</div>
        <div style="font-size:3.5em; font-weight:900; color:#ffffff">{prediction:.0f}</div>
        <div style="font-size:1.5em; color:#FFD700">minutes</div>
    </div>
    """, unsafe_allow_html=True)

    if prediction < 10:
        st.info("⚡ Short trip — quick ride across town!")
    elif prediction < 25:
        st.success("🙂 Average NYC trip length — typical journey!")
    else:
        st.warning("⏳ Long trip — sit back and enjoy the city view!")

st.markdown('<div class="footer">Built with LightGBM | NYC TLC 2025 Data | 46M trips analyzed</div>', unsafe_allow_html=True)
