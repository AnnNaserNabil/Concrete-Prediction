import streamlit as st
import numpy as np
import pickle
import os

st.set_page_config(page_title="Concrete Property Prediction", layout="centered")

# --- Helper function to load model safely ---
def load_model(path):
    if os.path.exists(path):
        return pickle.load(open(path, "rb"))
    else:
        st.error(f"Model file not found: {path}")
        return None

# --- Load models ---
model_sts = load_model("xgb_STS.pkl")
model_cs = load_model("xgb_CS.pkl")
model_slump = load_model("CatBoost_Slump.pkl")

# --- App title ---
st.title("🧱 Concrete Property Predictor")

# --- Sidebar model selector ---
model_choice = st.sidebar.selectbox("Select prediction target:", ["STS", "CS", "Slump"])

st.subheader(f"Input features for predicting **{model_choice}**")

# --- Input fields grouped in 3 columns ---
col1, col2, col3 = st.columns(3)

with col1:
    BNHF = st.number_input("BNHF (%)", value=0.0)
    Fiber = st.number_input("Fiber (kg/m3)", value=0.0)
    Fiber_length = st.number_input("Fiber length (mm)", value=0.0)

with col2:
    wc = st.number_input("w/c", value=0.0)
    Cement = st.number_input("Cement (kg/m3)", value=0.0)
    Fine_agg = st.number_input("Fine aggregate (kg/m3)", value=0.0)

with col3:
    Coarse_agg = st.number_input("Coarse aggregate (kg/m3)", value=0.0)
    Water = st.number_input("Water (kg/m3)", value=0.0)
    if model_choice in ["STS", "CS"]:
        Curing_time = st.number_input("Curing time (days)", value=0.0)
    else:
        Curing_time = None

# --- Predict button ---
if st.button("🔍 Predict"):
    if model_choice == "STS" and model_sts:
        input_data = np.array([[BNHF, Fiber, Fiber_length, wc, Cement, Fine_agg, Coarse_agg, Water, Curing_time]])
        prediction = model_sts.predict(input_data)[0]
    elif model_choice == "CS" and model_cs:
        input_data = np.array([[BNHF, Fiber, Fiber_length, wc, Cement, Fine_agg, Coarse_agg, Water, Curing_time]])
        prediction = model_cs.predict(input_data)[0]
    elif model_choice == "Slump" and model_slump:
        input_data = np.array([[BNHF, Fiber, Fiber_length, wc, Cement, Fine_agg, Coarse_agg, Water]])
        prediction = model_slump.predict(input_data)[0]
    else:
        prediction = None

    if prediction is not None:
        st.success(f"✅ Predicted {model_choice}: **{prediction:.3f}**")
    else:
        st.error("Prediction failed. Please check the input or model.")

# --- Footer ---
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center;'>
    Developed by <strong>Md Soumike Hassan</strong><br>
    Contact: <a href='mailto:md.soumikehassan@gmail.com'>md.soumikehassan@gmail.com</a><br><br>
    <strong>Authors and Co-authors:</strong><br>
    Mehedi Hasan<sup>1</sup>, Md Soumike Hassan<sup>2</sup>, Kamrul Hasan<sup>3</sup>, Fazlul Hoque Tushar<sup>4</sup>, Majid Khan<sup>5</sup>
</p>
""", unsafe_allow_html=True)
