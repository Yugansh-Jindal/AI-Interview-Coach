import streamlit as st

from auth.session_manager import (
    is_logged_in,
    get_current_user,
)

from database.database import (
    get_interviews,
    delete_interview,
)

st.set_page_config(
    page_title="Interview History",
    page_icon="📜",
    layout="wide",
)

st.title("📜 Interview History")

# ------------------------------------
# Login Check
# ------------------------------------

if not is_logged_in():

    st.warning("Please login first.")

    st.switch_page("pages/login.py")

user = get_current_user()

# ------------------------------------
# Load Interviews
# ------------------------------------

interviews = get_interviews(user["id"])

if not interviews:

    st.info("No interview history found.")

    st.stop()

# ------------------------------------
# Display Interviews
# ------------------------------------

for index, interview in enumerate(interviews, start=1):

    with st.expander(
        f"Interview #{index} | Score: {interview['overall_score']:.1f}/10"
    ):

        st.write(f"**Date:** {interview['created_at']}")
        st.write(f"**Overall Score:** {interview['overall_score']:.1f}/10")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "View Results",
                key=f"view_{interview['id']}"
            ):

                st.session_state.selected_interview = interview["id"]

                st.switch_page("pages/results.py")

        with col2:

            if st.button(
                "Delete",
                key=f"delete_{interview['id']}"
            ):

                delete_interview(
                interview["id"],
                    user["id"]
        )

                st.success("Interview deleted.")

                st.rerun()