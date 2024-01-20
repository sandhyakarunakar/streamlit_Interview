# app/profile_page.py
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
        st.experimental_rerun()  # Rerun the app to go back to the login/register page

    st.header('Profile Page')
    st.subheader(f'Welcome, {state["username"]}! 😊')
    
    # Add the content specific to the profile page here
    st.write('This is the content of the profile page.')
