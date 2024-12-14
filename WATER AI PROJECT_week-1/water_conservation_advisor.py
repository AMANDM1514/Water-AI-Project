import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import streamlit as st
import matplotlib.pyplot as plt

# Load the improved Excel data from the specified location
data_path = r'C:\Users\ASUS\Downloads\WATER AI PROJECT\water_conservation_data_improved.xlsx'
data = pd.read_excel(data_path)

# Load the GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Initialize the Streamlit app
st.set_page_config(page_title="Water Conservation Advisor", page_icon="💧")

# Add background image
st.markdown(
    """
    <style>
    .reportview-container {
        background: url('https://www.example.com/background-image.jpg') no-repeat center center fixed; 
        background-size: cover;
    }
    .stTextInput {
        background-color: rgba(255, 255, 255, 0.8);
    }
    .stButton {
        background-color: #008CBA; 
        color: white; 
        border: none; 
        border-radius: 5px;
        padding: 10px;
        transition: background-color 0.3s;
    }
    .stButton:hover {
        background-color: #005f73;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 Water Conservation Advisor")
st.write("Welcome to the Water Conservation Advisor! Ask me for tips on saving water.")

# Input from the user
user_input = st.text_input("Enter your question or request for water-saving tips:")

if st.button("Get Tips"):
    if user_input:
        # Create a prompt for GPT-2
        prompt = f"User: {user_input}\nAI:"
        
        # Encode the prompt
        input_ids = tokenizer.encode(prompt, return_tensors='pt')

        # Generate a response from GPT-2
        output = model.generate(input_ids, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, do_sample=True, top_k=50, top_p=0.95)

        # Decode the generated response
        response = tokenizer.decode(output[0], skip_special_tokens=True)

        # Extract the AI's response
        ai_response = response.split("AI:")[-1].strip()

        # Display the response
        st.subheader("Here are some tips:")
        st.write(ai_response)

        # Generate both pie chart and bar graph based on the data
        if 'conservation_methods' in data.columns and 'counts' in data.columns:  # Check if relevant columns exist
            methods = data['conservation_methods']  # Column for water-saving methods
            counts = data['counts']  # Column for respective counts

            # Create a pie chart
            st.subheader("Water Conservation Methods (Pie Chart)")
            fig1, ax1 = plt.subplots()
            ax1.pie(counts, labels=methods, autopct='%1.1f%%', startangle=90)
            ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig1)  # Display the pie chart

            # Create a bar graph
            st.subheader("Water Conservation Methods (Bar Graph)")
            fig2, ax2 = plt.subplots()
            ax2.bar(methods, counts, color='blue')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig2)  # Display the bar graph

    else:
        st.warning("Please enter a question or request for tips.")
