import streamlit as st
from datetime import datetime, timedelta

# Title
st.title("🏋️ Muay Thai Fight Camp Nutrition Planner")

# Sidebar Inputs
st.sidebar.header("Enter your Fight Camp Details:")
age = st.sidebar.number_input("Age", min_value=10, max_value=80, value=25)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
current_weight = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=150.0, value=70.0)
target_weight = st.sidebar.number_input("Target Fight Weight (kg)", min_value=30.0, max_value=150.0, value=65.0)
fight_camp_length = st.sidebar.selectbox("Fight Camp Length (weeks)", [6, 8, 10, 12])
water_cut_percentage = st.sidebar.slider("Water Cut Percentage (Max 5%)", min_value=0.0, max_value=5.0, value=3.0)
fight_date = st.sidebar.date_input("Fight Date", min_value=datetime.today())

# Calculations
days_left = (fight_date - datetime.today().date()).days
weeks_left = fight_camp_length

if days_left > 0:
    weight_to_lose = current_weight - target_weight
    water_cut_kg = (water_cut_percentage / 100) * current_weight
    fat_loss_goal = weight_to_lose - water_cut_kg
    fat_loss_per_week = fat_loss_goal / weeks_left
    calorie_deficit_per_day = (fat_loss_goal * 7700) / (weeks_left * 7)

    # Macros (basic estimates)
    if sex == "Male":
        protein_per_kg = 2.2
    else:
        protein_per_kg = 2.0

    protein_grams = protein_per_kg * target_weight
    fat_grams = (0.3 * (calorie_deficit_per_day + 2000)) / 9  # Rough fat intake
    carbs_grams = ((calorie_deficit_per_day + 2000) - (protein_grams * 4) - (fat_grams * 9)) / 4

    # Display Results
    st.header("Fight Camp Plan:")
    st.write(f"**Days Until Fight:** {days_left} days")
    st.write(f"**Weight to Lose:** {weight_to_lose:.1f} kg")
    st.write(f"**Fat Loss Goal:** {fat_loss_goal:.1f} kg (after {water_cut_kg:.1f} kg water cut)")
    st.write(f"**Weekly Fat Loss Needed:** {fat_loss_per_week:.2f} kg/week")
    st.write(f"**Daily Calorie Deficit Needed:** {calorie_deficit_per_day:.0f} kcal/day")

    st.header("Daily Nutrition Targets:")
    st.write(f"**Calories per Day:** ~{2000 - calorie_deficit_per_day:.0f} kcal")
    st.write(f"**Protein:** {protein_grams:.0f} g/day")
    st.write(f"**Fat:** {fat_grams:.0f} g/day")
    st.write(f"**Carbs:** {carbs_grams:.0f} g/day")

    st.header("Carb & Fibre Reduction Schedule:")
    st.write("- Maintain normal carbs and fibre until 7 days before fight.")
    st.write("- 6-4 days out: reduce carbs by 50%, fibre to 15g/day.")
    st.write("- 3-1 days out: very low carbs (under 50g/day), fibre to 10g/day.")

    st.header("Water Loading Plan:")
    st.write("- 7-5 days out: Drink 6-7L/day")
    st.write("- 4-3 days out: Reduce to 3-4L/day")
    st.write("- 2 days out: 1-1.5L")
    st.write("- 1 day out: Minimal sips only")

else:
    st.error("Please select a valid future fight date!")

# Footer
st.caption("Built for fighters who are chasing greatness! 🏋️⚡")
