import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import base64
import unicodedata

# --- Streamlit Page Config ---
st.set_page_config(page_title="My Fight Camp Nutrition", layout="centered")

# --- Custom Styles ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f0f2f6;
        color: #000000;
    }
    .stApp {
        background-color: #f0f2f6;
        color: #000000;
        padding: 20px;
    }
    .section {
        background-color: #ffffff;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .header-bar {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-bar h1 {
        color: #ff4b4b;
        margin: 10px 0 0 0;
        font-size: 2em;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: bold;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Embedded Logo (Base64) ---
logo_base64 = """<base64 image here>"""  # Use your actual base64 image string here

# --- Header ---
st.markdown("<div class='header-bar'>", unsafe_allow_html=True)
if logo_base64.strip():
    st.markdown(
        f"""<div style="text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" style="width:200px; margin-bottom:10px;"/>
        </div>""",
        unsafe_allow_html=True
    )
st.markdown("""
<h1>My Fight Camp Nutrition</h1>
<p>Welcome to a prototype of our app. It has been designed exclusively by fighters, for fighters!<br>
MY Fight Camp Nutrition is here to guide you through your weight cut by incorporating tried-and-tested weight loss principles to ensure you are in prime condition for competition!</p>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- Utility Functions ---
def clean_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def estimate_bmr(weight, age, sex):
    if sex == "Male":
        return 10 * weight + 6.25 * 170 - 5 * age + 5
    else:
        return 10 * weight + 6.25 * 160 - 5 * age - 161

# --- Sidebar Inputs ---
st.sidebar.header("Fight Details")
age = st.sidebar.number_input("Age", min_value=16, max_value=80, value=25)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
current_weight = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1)
target_weight = st.sidebar.number_input("Target Fight Weight (kg)", min_value=30.0, max_value=150.0, value=65.0, step=0.1)
fight_date = st.sidebar.date_input("Fight Date", min_value=datetime.today())

st.sidebar.header("Training Load")
training_load = st.sidebar.selectbox(
    "Weekly Training Load:",
    ("High (10+ hrs)", "Medium (5-10 hrs)", "Low (<5 hrs)")
)

# --- Determine Carb Multiplier ---
if training_load == "High (10+ hrs)":
    carbs_multiplier = 3.0
elif training_load == "Medium (5-10 hrs)":
    carbs_multiplier = 2.75
else:
    carbs_multiplier = 2.5

# --- Calculations ---
today = datetime.today().date()
days_left = (fight_date - today).days
weeks_left = days_left / 7
fight_camp_length = int(weeks_left) if weeks_left == int(weeks_left) else int(weeks_left) + 1

subscription_price = fight_camp_length * 5 if 4 <= fight_camp_length <= 12 else 120

st.sidebar.subheader("Subscription")
st.sidebar.write(f"Fight Camp Length: **{fight_camp_length} weeks**")
st.sidebar.write(f"Total Subscription Cost: **\u00a3{subscription_price}**")

# --- Main App Content ---
if days_left > 0:
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("## Weekly Nutrition & Weight Targets")

    weekly_data = []
    weight_loss_total = current_weight - target_weight
    weekly_fat_loss = weight_loss_total / fight_camp_length

    for week in range(1, fight_camp_length + 1):
        projected_weight = current_weight - weekly_fat_loss * week
        bmr = estimate_bmr(projected_weight, age, sex)
        tdee = bmr * 1.3

        protein = 2.0 * projected_weight
        fat = 1.0 * projected_weight
        carbs = carbs_multiplier * projected_weight

        calories = (protein * 4) + (fat * 9) + (carbs * 4)

        weekly_data.append({
            "Target Weight (kg)": f"{projected_weight:.2f}",
            "Calories (kcal)": round(calories),
            "Protein (g)": round(protein),
            "Fat (g)": round(fat),
            "Carbs (g)": round(carbs)
        })

    df = pd.DataFrame(weekly_data)
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("## Overall Progress")
    st.progress(1 - days_left / (fight_camp_length * 7))
    st.button("Download Your Fight Camp Plan")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("Please select a valid future fight date.")
