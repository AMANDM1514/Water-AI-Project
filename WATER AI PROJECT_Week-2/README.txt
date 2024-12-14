
Here's a breakdown of the code and the functionality of each section:

1. Imports and Data Loading
python
Copy code
import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import streamlit as st
import matplotlib.pyplot as plt

data_path = r'C:\Users\ASUS\Downloads\WATER AI PROJECT\water_conservation_data_improved.xlsx'
data = pd.read_excel(data_path)
Imports: Brings in necessary libraries for data handling (pandas), model processing (transformers), app interface (streamlit), and plotting (matplotlib).
Data Loading: Loads the Excel data containing water conservation details.
2. Loading GPT-2 Model and Initializing Streamlit App
python
Copy code
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

st.set_page_config(page_title="Water Conservation Advisor", page_icon="💧")
st.title("🌍 Water Conservation Advisor")
st.write("Welcome to the Water Conservation Advisor! Explore tips, calculators, and interactive charts.")
GPT-2 Model: Loads a tokenizer and model for generating natural language responses to user input.
Streamlit Configuration: Sets up the app’s title and icon and displays a welcoming title and description on the main page.
3. GPT-2 Water-Saving Tips Section
python
Copy code
st.subheader("Get Water-Saving Tips")
user_input = st.text_input("Enter your question or request for water-saving tips:")

if st.button("Get Tips"):
    if user_input:
        prompt = f"User: {user_input}\nAI:"
        input_ids = tokenizer.encode(prompt, return_tensors='pt')
        output = model.generate(input_ids, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, do_sample=True, top_k=50, top_p=0.95)
        ai_response = tokenizer.decode(output[0], skip_special_tokens=True).split("AI:")[-1].strip()
        st.subheader("Here are some tips:")
        st.write(ai_response)
    else:
        st.warning("Please enter a question or request for tips.")
Text Input: Accepts a user’s water conservation-related question.
GPT-2 Response: GPT-2 generates a response using the user's input as a prompt.
Display: Shows the generated tips or warnings if no input is provided.
4. Dynamic Water Conservation Charts Section
python
Copy code
st.subheader("Water Conservation Charts")
if "category" in data.columns:
    category = st.selectbox("Select a Category for Chart Analysis", data["category"].unique())

    if category:
        filtered_data = data[data["category"] == category]
        if not filtered_data.empty:
            methods = filtered_data["conservation_method"]
            counts = filtered_data["count"]

            fig1, ax1 = plt.subplots()
            ax1.pie(counts, labels=methods, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')
            st.pyplot(fig1)

            fig2, ax2 = plt.subplots()
            ax2.bar(methods, counts, color='skyblue')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig2)
        else:
            st.write("No data available for the selected category.")
Category Selection: Provides a dropdown of unique categories from the dataset for user selection.
Chart Generation: Displays both pie and bar charts based on the selected category data.
5. Water Usage Calculator
python
Copy code
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
User Input for Savings Calculation: Takes daily and weekly usage values for showers and laundry.
Calculations and Display: Computes and displays water savings in liters based on user input.
6. Water Bill Savings Calculator
python
Copy code
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
Water Rate Input: Takes the water cost per liter from the user.
Bill Savings Calculation: Estimates weekly, monthly, and yearly savings based on daily and weekly water savings.
Display: Shows estimated monetary savings.
7. Rainwater Harvesting Calculator
python
Copy code
st.subheader("🌧️ Rainwater Harvesting Calculator")
roof_area = st.number_input("Roof area for rainwater collection (square meters)", min_value=1.0, value=50.0)
rainfall = st.number_input("Average rainfall per month (mm)", min_value=1.0, value=100.0)
collection_efficiency = st.slider("Collection Efficiency (%)", min_value=50, max_value=100, value=85)

if st.button("Calculate Rainwater Collection"):
    monthly_rainwater = roof_area * rainfall * (collection_efficiency / 100) * 0.001  # in cubic meters
    st.write(f"**Estimated Monthly Rainwater Collection**: {monthly_rainwater:.2f} cubic meters")
    st.write(f"Equivalent to approximately {monthly_rainwater * 1000:.2f} liters")
Input for Roof Area, Rainfall, and Efficiency: Allows user to provide parameters to estimate rainwater harvesting potential.
Rainwater Collection Calculation: Computes monthly rainwater collected based on user input.
Display: Shows results in cubic meters and equivalent liters for easier interpretation.
Summary
The app offers an interactive interface to:

Provide water conservation tips using GPT-2.
Display visualizations (pie and bar charts) for selected conservation data.
Calculate potential water savings from reduced usage.
Estimate financial savings based on the reduced usage.
Calculate potential rainwater harvesting collection based on input parameters.
This setup gives users insights and tools to explore water conservation comprehensively. Let me know if you have further questions about any section!






