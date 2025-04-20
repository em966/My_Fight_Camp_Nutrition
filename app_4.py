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
        background-color: #ffffff;
        color: #000000;
    }
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    .stSidebar, .css-1d391kg { 
        background-color: #262730; 
        color: #ffffff; 
    }
    .css-q8sbsg, .css-1v3fvcr, .css-1lcbmhc { 
        color: #ffffff; 
    }
    h1, h2, h3, h4, h5, h6, p, label, div {
        color: #000000;
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
    .section {
        background-color: #f9f9f9;
        padding: 25px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    .stDataFrame thead tr th {
        background-color: #f2f2f2;
        color: #000000;
        font-weight: bold;
    }
    .stDataFrame tbody tr td {
        background-color: #ffffff;
        color: #000000;
    }
    .stProgress > div > div > div > div {
        background-color: #ff4b4b;
    }
</style>
""", unsafe_allow_html=True)

# --- Embedded Logo ---
logo_base64 = """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"""

st.markdown("<div class='header-bar'>", unsafe_allow_html=True)
if logo_base64.strip():
    st.markdown(
        f"""<div style="text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" style="width:200px; margin-bottom:10px;"/>
        </div>""",
        unsafe_allow_html=True
    )

st.title("My Fight Camp Nutrition")
st.caption("Welcome to a prototype of our app. It has been designed exclusively by fighters, for fighters! MY Fight Camp Nutrition is here to guide you through your weight cut by incorporating tried-and-tested weight loss principles to ensure you are in prime condition for competition!")
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
st.sidebar.write(f"Total Subscription Cost: **£{subscription_price}**")

# --- Main App Content ---
if days_left > 0:
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
    st.dataframe(df.style.set_table_styles([
        {"selector": "thead", "props": [("background-color", "#f2f2f2"), ("color", "#000000"), ("font-weight", "bold")]},
        {"selector": "tbody", "props": [("background-color", "#ffffff"), ("color", "#000000")]}
    ]), use_container_width=True)

    st.markdown("## Overall Progress")
    st.progress(1 - days_left / (fight_camp_length * 7))

    st.button("Download Your Fight Camp Plan")
else:
    st.error("Please select a valid future fight date.")
