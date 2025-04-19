import streamlit as st
from datetime import datetime, timedelta

# --- Page Title ---
st.title("My Fight Camp Nutrition")

# Welcome text
st.markdown(
    """
    <div style='text-align: center; margin-top: -20px;'>
        <h3>Welcome to your Fight Camp Planner</h3>
        <p>Get your personalized nutrition, weight cut, and water loading strategy, ready for peak performance on fight day.</p>
    </div>
    """,
    unsafe_allow_html=True
)


# --- Sidebar Inputs ---
st.sidebar.header("Your Fight Details")

age = st.sidebar.number_input("Age", min_value=10, max_value=80, value=25)
sex = st.sidebar.selectbox("Sex", ["Male", "Female", "Dev the Twat"])
current_weight = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1)
target_weight = st.sidebar.number_input("Target Fight Weight (kg)", min_value=30.0, max_value=150.0, value=65.0, step=0.1)
fight_date = st.sidebar.date_input("Fight Date", min_value=datetime.today())

water_cut_percentage = st.sidebar.slider(
    "Water Cut Percentage (Max 5%)",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)

# --- Calculations ---
days_left = (fight_date - datetime.today().date()).days
weeks_left = days_left / 7
fight_camp_length = int(weeks_left) if weeks_left == int(weeks_left) else int(weeks_left) + 1

# Subscription price logic
price_per_week = 10  # Set your price per week here (£)
total_price = fight_camp_length * price_per_week

# --- Display Subscription Info ---
st.sidebar.subheader("Your Subscription Plan")
st.sidebar.write(f"Fight Camp Length: **{fight_camp_length} weeks**")
st.sidebar.write(f"Total Subscription Cost: **£{total_price}**")

# --- Main Section ---
st.header("Weight Cut Overview")

if days_left > 0:
    weight_to_lose = current_weight - target_weight
    water_cut_kg = (water_cut_percentage / 100) * current_weight
    fat_loss_goal = weight_to_lose - water_cut_kg
    fat_loss_per_week = fat_loss_goal / fight_camp_length
    calorie_deficit_per_day = (fat_loss_goal * 7700) / (fight_camp_length * 7)

    # Macros Calculation
    protein_per_kg = 2.2 if sex == "Male" else 2.0
    protein_grams = protein_per_kg * target_weight
    fat_grams = (0.3 * (calorie_deficit_per_day + 2000)) / 9
    carbs_grams = ((calorie_deficit_per_day + 2000) - (protein_grams * 4) - (fat_grams * 9)) / 4

    st.write(f"**Days Until Fight:** {days_left} days")
    st.write(f"**Total Weight to Lose:** {weight_to_lose:.1f} kg")
    st.write(f"**Fat Loss Goal:** {fat_loss_goal:.1f} kg (after {water_cut_kg:.1f} kg water cut)")
    st.write(f"**Weekly Fat Loss Needed:** {fat_loss_per_week:.2f} kg/week")
    st.write(f"**Daily Calorie Deficit Needed:** {calorie_deficit_per_day:.0f} kcal/day")

    st.header("Daily Nutrition Targets")
    st.write(f"**Calories per Day:** ~{2000 - calorie_deficit_per_day:.0f} kcal")
    st.write(f"**Protein:** {protein_grams:.0f} g/day")
    st.write(f"**Fat:** {fat_grams:.0f} g/day")
    st.write(f"**Carbs:** {carbs_grams:.0f} g/day")

    st.header("Carbohydrate & Fibre Reduction Plan")
    st.write("- Maintain normal carbs and fibre until 7 days before fight.")
    st.write("- 6–4 days out: reduce carbs by 50%, fibre to 15g/day.")
    st.write("- 3–1 days out: very low carbs (under 50g/day), fibre to 10g/day.")

    st.header("Water Loading Strategy")
    st.write("- 7–5 days out: Drink 6–7L/day.")
    st.write("- 4–3 days out: Reduce to 3–4L/day.")
    st.write("- 2 days out: 1–1.5L.")
    st.write("- 1 day out: Minimal sips only.")

    import io

# --- Create Plan Text ---
    plan_text = f"""
    Fight Camp Nutrition Plan

    Age: {age}
    Sex: {sex}
    Current Weight: {current_weight} kg
    Target Weight: {target_weight} kg
    Days Until Fight: {days_left} days
    Fight Camp Length: {fight_camp_length} weeks

    Total Weight to Lose: {weight_to_lose:.1f} kg
    Fat Loss Goal: {fat_loss_goal:.1f} kg (after {water_cut_kg:.1f} kg water cut)

    Daily Nutrition Targets:
    - Calories: ~{2000 - calorie_deficit_per_day:.0f} kcal
    - Protein: {protein_grams:.0f} g
    - Fat: {fat_grams:.0f} g
    - Carbs: {carbs_grams:.0f} g

    Carbohydrate & Fibre Reduction:
    - 6–4 days out: reduce carbs by 50%, fibre to 15g/day
    - 3–1 days out: very low carbs (<50g/day), fibre to 10g/day

    Water Loading:
    - 7–5 days out: 6–7L/day
    - 4–3 days out: 3–4L/day
    - 2 days out: 1–1.5L
    - 1 day out: minimal sips only

    Subscription Plan:
    - Total Price: £{total_price}
    """

    # --- Create Downloadable File ---
    plan_bytes = io.BytesIO()
    plan_bytes.write(plan_text.encode('utf-8'))
    plan_bytes.seek(0)

    # --- Download Button ---
    st.download_button(
        label="Download Your Fight Camp Plan",
        data=plan_bytes,
        file_name="fight_camp_plan.txt",
        mime="text/plain"
    )


else:
    st.error("Please select a valid future fight date.")

# --- Footer ---
st.caption("Built for serious fighters preparing for peak performance.")

