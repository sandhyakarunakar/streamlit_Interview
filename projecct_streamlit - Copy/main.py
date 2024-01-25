# main.py
import streamlit as st
from apps import dashboard, registration
from apps import login
from apps.utils import create_user_table, get

def main():
    st.title('Virtual Interview')

    create_user_table()  # Explicitly create the "users" table

    if 'state' not in st.session_state:
        st.session_state.state = {'username': '', 'password': '', 'is_logged_in': False}

    if not st.session_state.state['is_logged_in']:
        page = st.sidebar.selectbox("Select Page", ["Login", "Register"])
        if page == "Login":
            login.login()
        elif page == "Register":
            registration.register()

    else:
        dashboard.show_dashboard()

if __name__ == '__main__':
    main()
