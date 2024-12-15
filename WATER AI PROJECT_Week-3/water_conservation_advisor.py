import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import re
from sklearn.linear_model import LinearRegression

# Load GPT-2 Model and Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Set Streamlit app title
st.title("Water Conservation Advisor")

# User inputs
daily_shower_saving = st.number_input("Daily shower time saved (in minutes)", min_value=0, value=5)
weekly_laundry_saving = st.number_input("Weekly laundry savings (in liters)", min_value=0, value=50)
feedback = st.text_area("Your feedback about water-saving tips:")
water_rate = st.number_input("Current water cost per liter (in local currency)", min_value=0.01, value=0.1)
current_water_usage = st.number_input("Current water usage (in liters)", min_value=0, value=250)

# Calculate savings
def calculate_savings(daily_shower_saving, weekly_laundry_saving):
    daily_usage_saving = daily_shower_saving * 7 * 12  # Assuming 12 liters/minute
    total_weekly_saving = daily_usage_saving + weekly_laundry_saving
    total_monthly_saving = total_weekly_saving * 4
    return total_weekly_saving, total_monthly_saving

total_weekly_saving, total_monthly_saving = calculate_savings(daily_shower_saving, weekly_laundry_saving)

# Display savings
st.write(f"Total weekly water savings: {total_weekly_saving} liters")
st.write(f"Total monthly water savings: {total_monthly_saving} liters")
st.write(f"Estimated monthly cost savings: {total_monthly_saving * water_rate} local currency")

# Prepare data for visualization
labels = ['Shower Savings', 'Laundry Savings']
sizes = [daily_shower_saving * 7 * 12, weekly_laundry_saving]  # Assuming 12 liters/minute for shower
colors = ['gold', 'lightskyblue']
explode = (0.1, 0)

# Create pie chart
fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

# Create bar graph
fig2, ax2 = plt.subplots()
ax2.bar(labels, sizes, color=['gold', 'lightskyblue'])
ax2.set_ylabel('Water Savings (liters)')
ax2.set_title('Water Savings Breakdown')
plt.xticks(rotation=45)
st.pyplot(fig2)

# Function to generate response using GPT-2
def generate_response(feedback):
    input_ids = tokenizer.encode(feedback, return_tensors='pt')
    output = model.generate(input_ids, max_length=50, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Generate response for user feedback
if feedback:
    response = generate_response(feedback)
    st.write("AI Response to Your Feedback:")
    st.write(response)

# Predict future usage based on past data (dummy data used here)
past_usage_data = np.array([220, 240, 250, 260, 280]).reshape(-1, 1)  # Dummy past usage data
current_data = np.array([[current_water_usage]])

# Train a simple linear regression model
model_lr = LinearRegression()
model_lr.fit(np.arange(len(past_usage_data)).reshape(-1, 1), past_usage_data)
predicted_usage = model_lr.predict(current_data)

# Display predicted future usage
st.write(f"Predicted future water usage: {predicted_usage[0][0]:.2f} liters")

# Conclusion and further tips
st.write("Thank you for using the Water Conservation Advisor!")
