import streamlit as st


st.title('Weather App')

name = st.text_input('Enter your name', '')
if name:
    st.write(f'Hello {name}, welcome to the weather app!')

# To run this app, use the command line to navigate to the app's directory and type:
# streamlit run app.py