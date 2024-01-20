# app/login.py
import streamlit as st
from passlib.hash import pbkdf2_sha256
from apps.utils import verify_login, get

def login():
    st.header('Login')

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    if st.button('Login'):
        if verify_login(username, password):
            state = get()
            state['is_logged_in'] = True
            state['username'] = username
            st.success('Logged in successfully!')
            st.balloons()
            
            st.experimental_rerun()  # Rerun the app to navigate to the dashboard
        else:
            st.error('Invalid username or password')
