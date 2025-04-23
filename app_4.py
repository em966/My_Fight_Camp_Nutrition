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
    header {visibility: hidden;}
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
water_cut_percentage = st.sidebar.slider("Water Cut Percentage (Max 5%)", min_value=0.0, max_value=5.0, value=3.0, step=0.1)

# --- Simplified Training Intensity Dropdown ---
st.sidebar.header("Training Intensity")
training_level = st.sidebar.selectbox("Overall Training Intensity", options=["Low (<5 hrs/week)", "Medium (5-10 hrs/week)", "High (>10 hrs/week)"])

# Macronutrient multipliers based on training level
if training_level == "Low (<5 hrs/week)":
    carb_multiplier = 2.0
    training_calories = 200
elif training_level == "Medium (5-10 hrs/week)":
    carb_multiplier = 2.75
    training_calories = 400
else:
    carb_multiplier = 3.0
    training_calories = 600

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

if days_left > 0:
    if current_weight <= target_weight:
        st.error("Current weight must be higher than target fight weight.")
    else:
        weight_to_lose = current_weight - target_weight
        water_cut_kg = (water_cut_percentage / 100) * target_weight
        fight_week_start_weight = target_weight + (2 * water_cut_kg)
        fat_loss_goal = current_weight - fight_week_start_weight
        fat_loss_per_week = fat_loss_goal / (fight_camp_length - 1)
        calorie_deficit_per_day = (fat_loss_goal * 7700) / ((fight_camp_length - 1) * 7)

        bmr = 10 * current_weight + 6.25 * 170 - 5 * age + (5 if sex == "Male" else -161)

        total_daily_energy = bmr + training_calories
        target_calories = total_daily_energy - calorie_deficit_per_day

        protein_grams = 2.0 * current_weight
        fat_grams = 1.0 * current_weight
        carb_grams = carb_multiplier * current_weight

        if fight_week_mode:
            st.header("Fight Week Plan")
            st.markdown("---")
            st.subheader("Carbohydrate Management")
            st.write("- 5-7 days out: Reduce carbs by 50-80g/day.")
            with st.expander("Why reduce carbs?"):
                st.write("Reducing carbs helps deplete muscle glycogen stores and associated water, lowering body weight quickly before the weigh-in.")

            st.subheader("Fibre Management")
            st.write("- 3 days before weigh-in: Fibre <10g/day.")
            with st.expander("Why reduce fibre?"):
                st.write("Reducing fibre minimizes undigested material and bulk in the gut, leading to lower body mass on the scale.")

            st.subheader("Salt Management")
            st.write("- 3 days before weigh-in: Salt 0.5-1g/day.")
            with st.expander("Why reduce salt?"):
                st.write("Lowering salt intake reduces water retention, helping flush out excess body water before the weigh-in.")

            st.subheader("Water Loading Strategy")
            st.write("- 4, 3, 2 days out: 100ml/kg body weight.")
            st.write("- 1 day out: 15ml/kg body weight.")
            st.write("- Weigh-in day: minimal sips only.")
            with st.expander("Why water load?"):
                st.write("Strategically overhydrating then cutting fluids trains the body to flush water rapidly, enhancing acute weight loss before weigh-in.")

            st.subheader("Post Weigh-In Rehydration")
            st.write("- 1L electrolyte solution immediately after weigh-in.")
            st.write("- Small carb-rich meals every 1-2 hours.")
            st.write("- Avoid high-fat and high-fibre foods initially.")
            with st.expander("Why structured rehydration?"):
                st.write("Rehydration restores plasma volume, electrolyte balance, and muscle glycogen efficiently, setting up optimal fight performance.")

        else:
            with st.container():
                st.header("Daily Nutrition Targets - Week 1")
                for day in range(1, 8):
                    st.subheader(f"Day {day}")
                    st.write(f"**Calories:** ~{target_calories:.0f} kcal")
                    st.write(f"**Protein:** {protein_grams:.0f} g")
                    st.write(f"**Fat:** {fat_grams:.0f} g")
                    st.write(f"**Carbs:** {carb_grams:.0f} g")
                    st.write("**Fibre:** 30g")
                    st.write("**Salt:** 3-5g")
                    st.markdown("---")

            with st.container():
                st.header("Weekly Weight Goals")
                for week in range(1, fight_camp_length):
                    target_weight_week = current_weight - (fat_loss_per_week * week)
                    st.write(f"Week {week}: Target Weight ~ {target_weight_week:.1f} kg")
                st.write(f"Fight Week Start: ~{fight_week_start_weight:.1f} kg")

st.caption("Make cutting weight simple.")
