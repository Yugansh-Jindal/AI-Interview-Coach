import streamlit as st

from auth.auth_service import auth_service

st.set_page_config(
    page_title="Register",
    page_icon="📝"
)

st.title("📝 Create an Account")

name = st.text_input("Full Name")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password"
)

if st.button("Register", use_container_width=True):

    if not name.strip():

        st.error("Please enter your name.")

    elif not email.strip():

        st.error("Please enter your email.")

    elif not password:

        st.error("Please enter a password.")

    elif password != confirm_password:

        st.error("Passwords do not match.")

    else:

        success = auth_service.register_user(
            name=name,
            email=email,
            password=password,
        )

        if success:

            st.success("✅ Account created successfully!")

            st.info("Go to the Login page to sign in.")

        else:

            st.error("An account with this email already exists.")