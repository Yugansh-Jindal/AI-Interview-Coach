import streamlit as st

from database.database import initialize_database
from auth.session_manager import (
    is_logged_in,
    get_current_user,
    logout,
)

# ---------------------------------------
# Initialize Database
# ---------------------------------------

initialize_database()

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
)

# ---------------------------------------
# Home Page
# ---------------------------------------

st.title("🎯 AI Interview Coach")

st.write(
    """
Welcome to the **AI Interview Coach**.

This application helps you:

- 📄 Upload your resume
- 💼 Analyze job descriptions
- 🤖 Take AI-powered interviews
- 📊 Receive detailed feedback
- 📈 Track interview history
"""
)

# ---------------------------------------
# Authentication Status
# ---------------------------------------

if is_logged_in():

    user = get_current_user()

    st.success(f"Logged in as **{user['name']}**")

    if st.button("🚪 Logout"):

        logout()
        st.rerun()

    st.info(
        """
Use the **left sidebar** to navigate to:

- Interview
- History
- Results
"""
    )

else:

    st.warning("You are not logged in.")

    st.info(
        """
Use the **left sidebar** to open:

- Login
- Register
"""
    )