import streamlit as st
from datetime import datetime
import unicodedata
import pandas as pd

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
    header {visibility: hidden; display: none;}
    .stAlert { background-color: #ffdede !important; color: black !important; }
</style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<div class='header-bar'>", unsafe_allow_html=True)
st.title("My Fight Camp Nutrition")
st.caption("A prototype nutrition plan created by fighters, for fighters!")
st.markdown("</div>", unsafe_allow_html=True)

# --- Sidebar Inputs ---
st.sidebar.header("Your Fight Details")

age = st.sidebar.number_input("Age", min_value=10, max_value=80, value=25)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
height = st.sidebar.number_input("Height (cm)", min_value=140, max_value=220, value=170)
current_weight = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1)
target_weight = st.sidebar.number_input("Target Fight Weight (kg)", min_value=30.0, max_value=150.0, value=65.0, step=0.1)
fight_date = st.sidebar.date_input("Fight Date", min_value=datetime.today())
water_cut_percentage = st.sidebar.slider("Water Cut Percentage (Max 5%)", min_value=0.0, max_value=5.0, value=0.0, step=0.1)

# Training intensity
st.sidebar.header("Training Intensity")
training_level = st.sidebar.selectbox(
    "Training Intensity",
    options=["Low (<5 hrs/week)", "Medium (5-10 hrs/week)", "High (>10 hrs/week)"]
)





if training_level == "Low (<5 hrs/week)":
    carb_multiplier = 2.5
    training_calories_factor = 1.375
elif training_level == "Medium (5-10 hrs/week)":
    carb_multiplier = 2.75
    training_calories_factor = 1.55
else:
    carb_multiplier = 3.0
    training_calories_factor = 1.75

fight_week_mode = st.sidebar.checkbox("Activate Fight Week Mode")

# --- Calculations ---
today = datetime.today().date()
days_left = (fight_date - today).days
weeks_left = days_left / 7
fight_camp_length = int(weeks_left) if weeks_left == int(weeks_left) else int(weeks_left) + 1

subscription_price = fight_camp_length * 5 if 4 <= fight_camp_length <= 12 else 120

st.sidebar.subheader("Your Subscription Plan")
st.sidebar.write(f"Fight Camp Length: **{fight_camp_length} weeks**")
st.sidebar.write(f"Total Subscription Cost: **£{subscription_price}**")

if days_left > 28:
    if current_weight <= target_weight:
        st.error("Current weight must be higher than fight weight.")
    else:
        weight_to_lose = current_weight - target_weight
        water_cut_kg = (water_cut_percentage / 100) * target_weight
        fight_week_start_weight = target_weight + (2 * water_cut_kg)
        fat_loss_goal = current_weight - fight_week_start_weight

        total_weeks = fight_camp_length - 1
        weekly_losses = [((i + 1) / sum(range(1, total_weeks + 1))) * fat_loss_goal for i in range(total_weeks)]

        weekly_data = []
        last_weight = current_weight

        for i, loss in enumerate(weekly_losses):
            this_week_weight = last_weight - loss
            bmr = 10 * this_week_weight + 6.25 * height - 5 * age + (5 if sex == "Male" else -161)
            maintenance = bmr * training_calories_factor
            deficit = (loss * 7700) / 7
            target_calories = maintenance - deficit
            protein_g = round(2.0 * this_week_weight)
            fat_g = round(1.0 * this_week_weight)
            carbs_g = round(carb_multiplier * this_week_weight)

            weekly_data.append({
                "Week": i + 1,
                "Target Weight (kg)": round(this_week_weight, 1),
                "Calories": round(target_calories),
                "Protein (g)": protein_g,
                "Fat (g)": fat_g,
                "Carbs (g)": carbs_g,
                "Fibre (g)": 30,
                "Salt (g)": "3-5"
            })

            last_weight = this_week_weight

        df_weekly = pd.DataFrame(weekly_data)

        if fight_week_mode:
            st.header("Fight Week Plan")
            st.markdown("---")
            st.subheader("Carbohydrate Management")
            st.write("- 5-7 days out: Reduce carbs by 50-80g/day.")
            with st.expander("Why reduce carbs?"):
                st.write("Depletes glycogen stores and associated water to drop weight.")

            st.subheader("Fibre Management")
            st.write("- 3 days before weigh-in: Fibre <10g/day.")
            with st.expander("Why reduce fibre?"):
                st.write("Minimizes undigested bulk in the gut.")

            st.subheader("Salt Management")
            st.write("- 3 days before weigh-in: Salt 0.5-1g/day.")
            with st.expander("Why reduce salt?"):
                st.write("Helps eliminate retained water.")

            st.subheader("Water Loading")
            st.write("- Days 4–2: 100ml/kg | Day 1: 15ml/kg | Weigh-in: minimal sips.")
            with st.expander("Why water load?"):
                st.write("Flushes excess water rapidly.")

            st.subheader("Post Weigh-In")
            st.write("- 1L electrolyte drink + carb meals every 1-2 hrs.")
        else:
            st.header("Weekly Nutrition & Weight Targets")
            with st.expander("Show Weekly Targets Table"):
                st.dataframe(df_weekly.set_index("Week"))
else:
    st.error("Fight date must be at least 4 weeks in the future.")

st.caption("Make cutting weight simple.")

# --- Disclaimer ---
st.markdown("---")
with st.expander("Disclaimer"):
    st.write("This app is for informational purposes only and should not be considered medical advice. Always consult a healthcare professional before making significant changes to your diet or exercise routine.")
