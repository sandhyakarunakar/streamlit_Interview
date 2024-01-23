# app/registration.py
import streamlit as st
from passlib.hash import pbkdf2_sha256
from apps.utils import create_user, user_exists

def register():
    st.header('Register')

    new_username = st.text_input('New Username')
    new_password = st.text_input('New Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')

    if new_password != confirm_password:
        st.error('Passwords do not match')
        return

    if st.button('Register'):
        if user_exists(new_username):
            st.error('Username already exists. Please choose a different one.')
        else:
            create_user(new_username, new_password)
            st.success('Registration successful! You can now log in.')
