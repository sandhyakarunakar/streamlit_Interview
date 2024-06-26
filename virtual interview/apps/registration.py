import streamlit as st
from PIL import Image
from passlib.hash import pbkdf2_sha256
from apps.utils import create_user, user_exists

def register():

    #background color
    st.markdown(
        """
        <style>
        .stApp {
            background-color: rgba(137, 207, 240, 0.5); /* Adjust the RGBA values and opacity as needed */
        }
        .stTextInput>div>div>input {
            color: #2d3436 !important;
            background-color: #dfe6e9 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    with st.form(key='register_form'):
        image = Image.open("images/login.png")
        st.image(image)
        
        st.markdown("<style>div[data-testid='stForm'] {border: 2px solid darkblue; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);}</style>", unsafe_allow_html=True)
        # st.subheader(":blue[Register]")
        st.markdown("<h3 style='color: darkblue;'>Register</h2>", unsafe_allow_html=True)
        new_username = st.text_input('New Username')
        new_password = st.text_input('New Password', type='password')
        confirm_password = st.text_input('Confirm Password', type='password')

        submit_button_style = """
            <style>
                .stButton>button {
                    background-color: darkblue !important;
                    color: white !important;
                }
            </style>
        """
        st.markdown(submit_button_style, unsafe_allow_html=True)
        
        submit_button = st.form_submit_button(label='Register')

        if new_password != confirm_password:
            st.error('Passwords do not match')
            return

        if submit_button:
            if user_exists(new_username):
                st.error('Username already exists. Please choose a different one.')
            else:
                create_user(new_username, new_password)
                st.success('Registration successful! You can now log in.')


