import streamlit as st
from datetime import datetime, timedelta
import io
from fpdf import FPDF
import unicodedata

# --- Utility Functions ---
def clean_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def estimate_bmr(weight, age, sex):
    if sex == "Male":
        return 10 * weight + 6.25 * 170 - 5 * age + 5  # assume avg height 170cm
    else:
        return 10 * weight + 6.25 * 160 - 5 * age - 161

def calculate_training_calories(high, medium, low):
    return (high * 60 * 11) + (medium * 60 * 7.5) + (low * 60 * 4.5)

# --- Streamlit Page Config ---
st.set_page_config(page_title="My Fight Camp Nutrition", layout="centered")
st.title("My Fight Camp Nutrition")

st.markdown("""
<div style='text-align: center; margin-top: -20px;'>
    <h3>Welcome to your Fight Camp Nutrition where cutting weight is made simple</h3>
    <p>Personalised nutrition, weight cut, and water loading strategy to peak on fight day.</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar Inputs ---
st.sidebar.header("Your Fight Details")

# Theme Selector
theme = st.sidebar.radio("Choose Theme:", ("Light Mode", "Dark Mode"))
page_bg_color = "#ffffff" if theme == "Light Mode" else "#0e1117"
text_color = "#000000" if theme == "Light Mode" else "#fafafa"

st.markdown(f"""
<style>
    .stApp {{ background-color: {page_bg_color}; color: {text_color}; }}
</style>
""", unsafe_allow_html=True)

# Fighter Info
age = st.sidebar.number_input("Age", min_value=16, max_value=80, value=25)
sex = st.sidebar.selectbox("Sex", ["Male", "Female"])
current_weight = st.sidebar.number_input("Current Weight (kg)", min_value=30.0, max_value=150.0, value=70.0, step=0.1)
target_weight = st.sidebar.number_input("Target Fight Weight (kg)", min_value=30.0, max_value=150.0, value=65.0, step=0.1)
fight_date = st.sidebar.date_input("Fight Date", min_value=datetime.today())
water_cut_percentage = st.sidebar.slider("Water Cut Percentage (Max 5%)", min_value=0.0, max_value=5.0, value=3.0, step=0.1)

# Training Load Input
st.sidebar.header("Weekly Training Hours")
high_intensity = st.sidebar.number_input("High Intensity (hrs)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
medium_intensity = st.sidebar.number_input("Medium Intensity (hrs)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)
low_intensity = st.sidebar.number_input("Low Intensity (hrs)", min_value=0.0, max_value=20.0, value=5.0, step=0.5)

# --- Calculations ---
today = datetime.today().date()
days_left = (fight_date - today).days
weeks_left = days_left / 7
fight_camp_length = int(weeks_left) if weeks_left == int(weeks_left) else int(weeks_left) + 1

# Subscription Pricing
subscription_price = fight_camp_length * 5 if 4 <= fight_camp_length <= 12 else 120

# --- Display Subscription Info ---
st.sidebar.subheader("Your Subscription Plan")
st.sidebar.write(f"Fight Camp Length: **{fight_camp_length} weeks**")
st.sidebar.write(f"Total Subscription Cost: **\u00a3{subscription_price}**")

# --- Main Display ---
if days_left > 0:
    if current_weight <= target_weight:
        st.error("Current weight must be higher than target fight weight.")
    else:
        weight_to_lose = current_weight - target_weight
        water_cut_kg = (water_cut_percentage / 100) * current_weight
        fat_loss_goal = weight_to_lose - water_cut_kg
        fat_loss_per_week = fat_loss_goal / fight_camp_length
        calorie_deficit_per_day = (fat_loss_goal * 7700) / (fight_camp_length * 7)

        # Calculate Calories
        bmr = estimate_bmr(current_weight, age, sex)
        training_calories = calculate_training_calories(high_intensity, medium_intensity, low_intensity) / 7
        total_daily_energy = bmr + training_calories
        target_calories = total_daily_energy - calorie_deficit_per_day

        # Macro Calculations
        protein_per_kg = 2.2 if sex == "Male" else 2.0
        protein_grams = protein_per_kg * target_weight
        fat_grams = (0.3 * target_calories) / 9
        carbs_grams = (target_calories - (protein_grams * 4) - (fat_grams * 9)) / 4

        st.markdown("---")
        st.header("Weight Cut Overview")
        st.write(f"**Days Until Fight:** {days_left} days")

        # Progress Bar
        total_camp_days = fight_camp_length * 7
        days_completed = total_camp_days - days_left
        progress = max(0, min(1, days_completed / total_camp_days))
        st.progress(progress)

        st.write(f"**Total Weight to Lose:** {weight_to_lose:.1f} kg")
        st.write(f"**Fat Loss Goal:** {fat_loss_goal:.1f} kg (after {water_cut_kg:.1f} kg water cut)")
        st.write(f"**Weekly Fat Loss Needed:** {fat_loss_per_week:.2f} kg/week")
        st.write(f"**Daily Calorie Deficit Needed:** {calorie_deficit_per_day:.0f} kcal/day")

        st.markdown("---")
        st.header("Daily Nutrition Targets")
        st.write(f"**Calories per Day:** ~{target_calories:.0f} kcal")
        st.write(f"**Protein:** {protein_grams:.0f} g/day")
        st.write(f"**Fat:** {fat_grams:.0f} g/day")
        st.write(f"**Carbs:** {carbs_grams:.0f} g/day")

        st.markdown("---")
        st.header("Weekly Weight Goals")
        for week in range(1, fight_camp_length + 1):
            target_weight_week = current_weight - (fat_loss_per_week * week)
            st.write(f"Week {week}: Target Weight ~ {target_weight_week:.1f} kg")

        st.markdown("---")
        st.header("Carbohydrate & Fibre Reduction Plan")
        st.write("- Maintain normal carbs and fibre until 7 days before fight.")
        st.write("- 6–4 days out: reduce carbs by 50%, fibre to 15g/day.")
        st.write("- 3–1 days out: very low carbs (<50g/day), fibre to 10g/day.")

        st.markdown("---")
        st.header("Water Loading Strategy")
        st.write("- 7–5 days out: Drink 6–7L/day.")
        st.write("- 4–3 days out: Reduce to 3–4L/day.")
        st.write("- 2 days out: 1–1.5L.")
        st.write("- 1 day out: Minimal sips only.")

        st.markdown("---")
        st.header("Supplement Guidance")
        st.write("- Daily multivitamin and mineral support.")
        st.write("- Electrolyte replenishment during water loading.")
        st.write("- Protein supplements as needed to hit daily targets.")

        st.markdown("---")
        st.header("Post Weigh-In Rehydration Plan")
        st.write("- 1L of electrolyte solution immediately after weigh-in.")
        st.write("- Small carbohydrate-rich meals every 1–2 hours.")
        st.write("- Avoid high-fat and high-fibre foods initially.")

        # PDF Creation
        class PDF(FPDF):
            def header(self):
                self.set_font('Arial', 'B', 16)
                self.cell(0, 10, 'Fight Camp Nutrition Plan', 0, 1, 'C')
                self.ln(10)
            def chapter_body(self, text):
                self.set_font('Arial', '', 12)
                self.multi_cell(0, 10, text)
                self.ln()

        pdf = PDF()
        pdf.add_page()

        plan_text = f"""
Age: {age}
Sex: {sex}
Current Weight: {current_weight} kg
Target Weight: {target_weight} kg
Days Until Fight: {days_left}
Fight Camp Length: {fight_camp_length} weeks

Total Weight to Lose: {weight_to_lose:.1f} kg
Fat Loss Goal: {fat_loss_goal:.1f} kg

Daily Nutrition:
- Calories: ~{target_calories:.0f} kcal
- Protein: {protein_grams:.0f} g
- Fat: {fat_grams:.0f} g
- Carbs: {carbs_grams:.0f} g

Carbohydrate & Fibre Cut Plan
Water Loading Strategy
Supplement Plan
Post Weigh-In Rehydration Plan

Subscription Cost: £{subscription_price}
"""
        plan_text = clean_text(plan_text)
        pdf.chapter_body(plan_text)
        pdf_output = pdf.output(dest='S').encode('latin1')

        st.download_button(
            label="Download Your Fight Camp Plan as PDF",
            data=pdf_output,
            file_name="fight_camp_plan.pdf",
            mime="application/pdf"
        )
else:
    st.error("Please select a valid future fight date.")

# Footer
st.caption("Built for serious fighters preparing for peak performance.")
