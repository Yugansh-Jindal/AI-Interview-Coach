import streamlit as st

from services.document_service import documents_exist
from agents.interview_agent import InterviewAgent
from auth.session_manager import (
    is_logged_in,
    get_current_user,
)
from database.database import save_interview

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 AI Interview Coach")

if not is_logged_in():

    st.warning("Please login first.")

    st.switch_page("pages/login.py")

user = get_current_user()

# ------------------------
# Session State
# ------------------------

if "agent" not in st.session_state:
    st.session_state.agent = InterviewAgent()

if "feedback" not in st.session_state:
    st.session_state.feedback = None

if "answer_box" not in st.session_state:
    st.session_state.answer_box = ""

agent = st.session_state.agent
session = agent.session

# ------------------------
# Start Interview
# ------------------------

if not session.is_started:

    button_text = (
        "🚀 Start Interview"
        if not session.is_completed
        else "🔄 Start New Interview"
    )

    if st.button(button_text):

        if not documents_exist(user["id"]):
            st.error("Please upload your Resume and Job Description first.")
            st.stop()

        st.session_state.feedback = None

        st.session_state.pop("answer_box", None)

        # Reset saved interview/report for the new interview
        st.session_state.pop("interview_saved", None)
        st.session_state.pop("final_report", None)

        agent.start_interview(user["id"])

        st.rerun()

# ------------------------
# Interview
# ------------------------

if session.is_started:

    st.subheader(
        f"Question {session.current_question_number}/{session.total_questions}"
    )

    st.progress(
        session.current_question_number /
        session.total_questions
    )

    st.info(session.current_question)

    answer = st.text_area(
        "Your Answer",
        key="answer_box",
        height=200
    )

    if st.button("Submit Answer"):

        if answer.strip():

            st.session_state.feedback = agent.submit_answer(answer)

            st.rerun()

        else:

            st.warning("Please enter your answer.")

    if st.session_state.feedback:

        feedback = st.session_state.feedback

        st.divider()

        st.subheader("Evaluation")

        st.metric(
            "Score",
            f"{feedback.get('score', 0)}/10"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### ✅ Strengths")

            for item in feedback.get("strengths", []):
                st.write(f"- {item}")

        with col2:

            st.markdown("### ⚠️ Weaknesses")

            for item in feedback.get("weaknesses", []):
                st.write(f"- {item}")

        st.markdown("### 💡 Suggestions")

        for item in feedback.get("suggestions", []):
            st.write(f"- {item}")

        if session.is_completed:

            st.success("🎉 Interview Completed!")

            st.balloons()

            if "interview_saved" not in st.session_state:

                st.session_state.interview_saved = save_interview(
                 session,
                 user["id"]
        )

        else:

            if st.button("Next Question ➜"):

                st.session_state.feedback = None

                agent.move_to_next_question()

                # Clear textbox safely
                st.session_state.pop("answer_box", None)

                st.rerun()