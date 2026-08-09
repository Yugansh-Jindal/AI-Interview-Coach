import streamlit as st

from auth.auth_service import auth_service
from auth.session_manager import login

st.set_page_config(
    page_title="Login",
    page_icon="🔐"
)

st.title("🔐 Login")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login", use_container_width=True):

    if not email.strip():

        st.error("Please enter your email.")

    elif not password:

        st.error("Please enter your password.")

    else:

        user = auth_service.login_user(
            email=email,
            password=password,
        )

        if user is None:

            st.error("Invalid email or password.")

        else:

            login(user)

            st.success(f"Welcome, {user['name']}!")

            st.switch_page("pages/interview.py")