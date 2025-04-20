import streamlit as st
from datetime import datetime, timedelta
import io
from fpdf import FPDF
import unicodedata
import base64

# --- Streamlit Page Config ---
st.set_page_config(page_title="My Fight Camp Nutrition", layout="centered")

# --- Custom Styles ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background-color: #f0f2f6;
        padding: 20px;
    }
    .section {
        background-color: #ffffff;
        padding: 30px;
        margin-bottom: 25px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }
    .header-bar {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .header-bar h1 {
        color: #ff4b4b;
        margin: 10px 0 0 0;
        font-size: 2.5em;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        margin-top: 20px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- Embedded Logo (Base64) ---
logo_base64 = """<your base64 string here>"""  # <- insert your base64 logo string between triple quotes.

# --- Header Section ---
st.markdown("<div class='header-bar'>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" style="width:250px; margin-bottom:10px;"/>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("My Fight Camp Nutrition")
st.caption("Personalised nutrition and weight cut strategy.")
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
    ("High (8+ hrs)", "Medium (5-8 hrs)", "Low (<5 hrs)")
)

# --- Determine Carb Multiplier based on Training Load ---
if training_load == "High (8+ hrs)":
    carbs_multiplier = 3.0
elif training_load == "Medium (5-8 hrs)":
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

if days_left > 0:
    bmr = estimate_bmr(current_weight, age, sex)
    total_daily_energy = bmr * 1.3  # Slight training multiplier for active fighters

    protein_grams = 2.0 * current_weight
    fat_grams = 1.0 * current_weight
    carbs_grams = carbs_multiplier * current_weight

    calories_from_protein = protein_grams * 4
    calories_from_fat = fat_grams * 9
    calories_from_carbs = carbs_grams * 4

    target_calories = calories_from_protein + calories_from_fat + calories_from_carbs

    st.markdown("### Daily Nutrition Targets")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Calories (kcal)", f"{target_calories:.0f}")
        st.metric("Protein (g)", f"{protein_grams:.0f}")
    with col2:
        st.metric("Fat (g)", f"{fat_grams:.0f}")
        st.metric("Carbs (g)", f"{carbs_grams:.0f}")

    st.markdown("### Weekly Progress")
    st.progress(1 - days_left / (fight_camp_length * 7))

    # Download Button Placeholder
    st.button("Download Fight Camp Plan PDF")

else:
    st.error("Please select a valid future fight date.")
