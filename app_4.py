import streamlit as st
from datetime import datetime
import unicodedata

# --- Streamlit Page Config ---
st.set_page_config(page_title="My Fight Camp Nutrition", layout="centered")

# --- Custom Styles ---
st.markdown("""
<style>
    .stApp {
        background-color: #f0f2f6;
        color: #000000;
        padding: 20px;
    }
    .section {
        background-color: #ffffff;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<div class='header-bar'>", unsafe_allow_html=True)
st.title("My Fight Camp Nutrition")
st.caption("A prototype nutrition planner built for fighters!")
st.markdown("</div>", unsafe_allow_html=True)

# --- Sidebar Inputs ---
st.sidebar.header("Your Fight Details")

age = st.sidebar.number_input("Age", min_value=10, max_value=80, value=25)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
current_weight = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1)
target_weight = st.sidebar.number_input("Target Fight Weight (kg)", min_value=30.0, max_value=150.0, value=65.0, step=0.1)
fight_date = st.sidebar.date_input("Fight Date", min_value=datetime.today())

intensity = st.sidebar.selectbox("Exercise Intensity", ["High", "Medium", "Low"])

# --- Calculations ---
today = datetime.today().date()
days_left = (fight_date - today).days
weeks_left = days_left / 7
fight_camp_length = int(weeks_left) if weeks_left == int(weeks_left) else int(weeks_left) + 1

subscription_price = fight_camp_length * 5 if 4 <= fight_camp_length <= 12 else 120

st.sidebar.subheader("Your Subscription Plan")
st.sidebar.write(f"Fight Camp Length: **{fight_camp_length} weeks**")
st.sidebar.write(f"Total Subscription Cost: **£{subscription_price}**")

if days_left > 0:
    if current_weight <= target_weight:
        st.error("Current weight must be higher than target fight weight.")
    else:
        weight_to_lose = current_weight - target_weight
        fat_loss_goal = weight_to_lose
        fat_loss_per_week = fat_loss_goal / (fight_camp_length - 1)
        calorie_deficit_per_day = (fat_loss_goal * 7700) / ((fight_camp_length - 1) * 7)

        bmr = 10 * current_weight + 6.25 * 170 - 5 * age + (5 if sex == "Male" else -161)

        # Macro calculation using training intensity factors
        protein_grams = 2.0 * current_weight
        fat_grams = 1.0 * current_weight
        intensity_factor = {"High": 3.0, "Medium": 2.75, "Low": 2.5}[intensity]
        carbs_grams = intensity_factor * current_weight

        # Calories from macros
        calories_from_protein = protein_grams * 4
        calories_from_fat = fat_grams * 9
        calories_from_carbs = carbs_grams * 4
        total_calories = calories_from_protein + calories_from_fat + calories_from_carbs

        # Adjust for calorie deficit
        adjusted_calories = total_calories - calorie_deficit_per_day

        with st.container():
            st.header("Daily Nutrition Targets")
            st.write(f"**Calories per Day:** ~{adjusted_calories:.0f} kcal")
            st.write(f"**Protein:** {protein_grams:.0f} g/day")
            st.write(f"**Fat:** {fat_grams:.0f} g/day")
            st.write(f"**Carbs:** {carbs_grams:.0f} g/day")
            st.write("**Fibre:** 30g/day")
            st.write("**Salt:** 3-5g/day")

        with st.container():
            st.header("Weekly Weight Goals")
            for week in range(1, fight_camp_length):
                target_weight_week = current_weight - (fat_loss_per_week * week)
                st.write(f"Week {week}: Target Weight ~ {target_weight_week:.1f} kg")
else:
    st.error("Please select a valid future fight date.")

st.caption("Make cutting weight simple.")
