import streamlit as st


def login(user: dict):

    st.session_state.logged_in = True
    st.session_state.user = user


def logout():

    keys = [
        "logged_in",
        "user",
        "agent",
        "feedback",
        "answer_box",
        "final_report",
        "interview_saved",
    ]

    for key in keys:
        st.session_state.pop(key, None)


def is_logged_in():

    return st.session_state.get(
        "logged_in",
        False
    )


def get_current_user():

    return st.session_state.get(
        "user",
        None
    )