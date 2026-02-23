import streamlit as st
import numpy as np
import joblib
import os

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="Machine Failure Prediction",
    page_icon="⚙️",
    layout="centered"
)

st.title("⚙️ Machine Failure Prediction System")
st.markdown("Enter sensor values to predict machine failure.")

# ---------------------------------
# Load Model & Scaler
# ---------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "xgb_machine_failure_model.pkl")
scaler_path = os.path.join(BASE_DIR, "sensor_scaler.pkl")

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except:
    st.error("❌ Model or Scaler file not found.")
    st.stop()

st.divider()

# ---------------------------------
# Input Fields (EDIT THESE NAMES BASED ON YOUR DATASET)
# ---------------------------------

footfall = st.number_input("Footfall", value=0.0)
temp_mode = st.number_input("Temperature Mode", value=0.0)
aq = st.number_input("Air Quality", value=0.0)
uss = st.number_input("Ultrasonic Sensor Data", value=0.0)
cs = st.number_input("Current Sensor Reading", value=0.0)
voc = st.number_input("VOC Level", value=0.0)
rpm = st.number_input("RPM", value=0.0)
ip = st.number_input("Input Pressure", value=0.0)
temperature = st.number_input("Temperature", value=0.0)

st.divider()

# ---------------------------------
# Prediction
# ---------------------------------
if st.button("🔍 Predict Machine Status"):

    try:
        features = np.array([[footfall, temp_mode, aq, uss, cs, voc, rpm, ip, temperature]])
        features_scaled = scaler.transform(features)

        prediction = model.predict(features_scaled)[0]
        probability = model.predict_proba(features_scaled)[0][1]

        st.subheader("Prediction Result")

        if prediction == 1:
            st.error(f"⚠️ Machine Failure Detected!\n\nFailure Risk: {probability:.2%}")
        else:
            st.success(f"✅ Machine Operating Normally\n\nFailure Risk: {probability:.2%}")

    except Exception as e:
        st.error("Feature mismatch. Ensure input order matches training data.")
        st.text(str(e))

st.caption("⚠️ For industrial monitoring purposes only.")