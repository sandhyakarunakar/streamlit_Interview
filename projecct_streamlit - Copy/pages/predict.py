#pages/predict.py
import streamlit as st
from apps.utils import get

state = get()

# Check if the user is logged in
if not state['is_logged_in']:
    st.error('Please log in to view this page.')
else:
    # Logout button
    if st.button('Logout'):
        state['is_logged_in'] = False
        st.experimental_rerun()
    
    st.header("Prediction :")