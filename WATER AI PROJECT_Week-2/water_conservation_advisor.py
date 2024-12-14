import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import streamlit as st
import matplotlib.pyplot as plt

# Load the Excel data
data_path = r'C:\Users\ASUS\Downloads\WATER AI PROJECT\water_conservation_data_improved.xlsx'
data = pd.read_excel(data_path)

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Initialize the Streamlit app
st.set_page_config(page_title="Water Conservation Advisor", page_icon="💧")
st.title("🌍 Water Conservation Advisor")
st.write("Welcome to the Water Conservation Advisor! Explore tips, calculators, and interactive charts.")

# User Input Section for GPT-2 Advice
st.subheader("Get Water-Saving Tips")
user_input = st.text_input("Enter your question or request for water-saving tips:")

if st.button("Get Tips"):
    if user_input:
        # Create a prompt for GPT-2
        prompt = f"User: {user_input}\nAI:"
        
        # Encode the prompt
        input_ids = tokenizer.encode(prompt, return_tensors='pt')
        output = model.generate(input_ids, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, do_sample=True, top_k=50, top_p=0.95)

        # Decode and display GPT-2 response
        ai_response = tokenizer.decode(output[0], skip_special_tokens=True).split("AI:")[-1].strip()
        st.subheader("Here are some tips:")
        st.write(ai_response)
    else:
        st.warning("Please enter a question or request for tips.")

# Dynamic Chart Section
st.subheader("Water Conservation Charts")
if "category" in data.columns:
    category = st.selectbox("Select a Category for Chart Analysis", data["category"].unique())

    if category:
        filtered_data = data[data["category"] == category]
        if not filtered_data.empty:
            methods = filtered_data["conservation_method"]
            counts = filtered_data["count"]

            # Pie Chart
            fig1, ax1 = plt.subplots()
            ax1.pie(counts, labels=methods, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            # Bar Graph
            fig2, ax2 = plt.subplots()
            ax2.bar(methods, counts, color='skyblue')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig2)
        else:
            st.write("No data available for the selected category.")

# Initialize savings variables
daily_shower_saving = 0
weekly_laundry_saving = 0

# Water Usage Calculator
st.subheader("💧 Water Usage Calculator")
shower_usage = st.number_input("Average daily shower time in minutes", min_value=1, max_value=60, value=8)
shower_saving = st.number_input("Water saved per minute with efficient shower head (liters)", min_value=1, max_value=10, value=3)
laundry_loads = st.number_input("Number of laundry loads per week", min_value=1, max_value=20, value=5)
laundry_saving = st.number_input("Water saved per load with efficient machine (liters)", min_value=1, max_value=50, value=20)

if st.button("Calculate Water Usage Savings"):
    daily_shower_saving = shower_usage * shower_saving
    weekly_laundry_saving = laundry_loads * laundry_saving
    st.write(f"**Estimated Daily Shower Water Savings**: {daily_shower_saving} liters")
    st.write(f"**Estimated Weekly Laundry Water Savings**: {weekly_laundry_saving} liters")

# Water Bill Savings Calculator
st.subheader("💸 Water Bill Savings Calculator")
water_rate = st.number_input("Current water cost per liter (in local currency)", min_value=0.001, value=0.0025)
daily_usage_saving = daily_shower_saving * 7 + weekly_laundry_saving

if st.button("Calculate Water Bill Savings"):
    weekly_cost_saving = daily_usage_saving * water_rate
    monthly_cost_saving = weekly_cost_saving * 4
    yearly_cost_saving = weekly_cost_saving * 52
    st.write(f"**Weekly Savings**: {weekly_cost_saving:.2f}")
    st.write(f"**Monthly Savings**: {monthly_cost_saving:.2f}")
    st.write(f"**Yearly Savings**: {yearly_cost_saving:.2f}")

# Rainwater Harvesting Calculator
st.subheader("🌧️ Rainwater Harvesting Calculator")
roof_area = st.number_input("Roof area for rainwater collection (square meters)", min_value=1.0, value=50.0)
rainfall = st.number_input("Average rainfall per month (mm)", min_value=1.0, value=100.0)
collection_efficiency = st.slider("Collection Efficiency (%)", min_value=50, max_value=100, value=85)

if st.button("Calculate Rainwater Collection"):
    monthly_rainwater = roof_area * rainfall * (collection_efficiency / 100) * 0.001  # in cubic meters
    st.write(f"**Estimated Monthly Rainwater Collection**: {monthly_rainwater:.2f} cubic meters")
    st.write(f"Equivalent to approximately {monthly_rainwater * 1000:.2f} liters")
