import streamlit as st
import json

from auth.session_manager import (
    is_logged_in,
    get_current_user,
)

from database.database import (
    save_interview,
    get_user_interview,
)

from services.report_pdf_service import generate_pdf
from services.report_service import generate_interview_report

st.set_page_config(
    page_title="Interview Results",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Interview Results")

if not is_logged_in():

    st.warning("Please login first.")

    st.switch_page("pages/login.py")

# -----------------------------------
# Open interview from History
# -----------------------------------

if "selected_interview" in st.session_state:

    user = get_current_user()

    data = get_user_interview(
        st.session_state.selected_interview,
        user["id"]
    )

    if data is None:

        st.error("Interview not found.")

        st.stop()

    interview = data["interview"]
    details = data["details"]

    st.subheader("Interview Summary")

    st.metric(
        "Overall Score",
        f"{interview['overall_score']:.1f}/10"
    )

    st.divider()

    for item in details:

        with st.expander(
            f"Question {item['question_number']}"
        ):

            st.markdown("### Topic")
            st.write(item["topic"])

            st.markdown("### Question")
            st.write(item["question"])

            st.markdown("### Answer")
            st.write(item["answer"])

            st.metric(
                "Score",
                f"{item['score']}/10"
            )

            st.markdown("### Strengths")

            for strength in json.loads(item["strengths"]):
                st.write(f"- {strength}")

            st.markdown("### Weaknesses")

            for weakness in json.loads(item["weaknesses"]):
                st.write(f"- {weakness}")

            st.markdown("### Suggestions")

            for suggestion in json.loads(item["suggestions"]):
                st.write(f"- {suggestion}")

    st.stop()
# -----------------------------------
# Current Interview
# -----------------------------------

if "agent" not in st.session_state:

    st.warning("No interview session found.")

    st.stop()

session = st.session_state.agent.session

if not session.questions:

    st.info("Complete an interview first.")

    st.stop()

# ----------------------------
# Save Interview (Only Once)
# ----------------------------

if session.is_completed and not st.session_state.get("interview_saved", False):

    user = get_current_user()

    save_interview(session, user["id"])

    st.session_state.interview_saved = True

# ----------------------------
# Summary
# ----------------------------

st.subheader("Interview Summary")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Questions Answered",
        len(session.questions)
    )

with col2:
    st.metric(
        "Overall Score",
        f"{session.overall_score:.1f}/10"
    )

st.progress(min(session.overall_score / 10, 1.0))

st.divider()

# ----------------------------
# Question Wise Feedback
# ----------------------------

for i in range(len(session.questions)):

    question = session.questions[i]
    answer = session.answers[i]
    feedback = session.feedback[i]

    with st.expander(f"Question {i + 1}"):

        st.markdown("### ❓ Question")
        st.write(question)

        st.markdown("### 💬 Your Answer")
        st.write(answer)

        st.metric(
            "Score",
            f"{feedback.get('score', 0)}/10"
        )

        st.markdown("### ✅ Strengths")
        for item in feedback.get("strengths", []):
            st.write(f"- {item}")

        st.markdown("### ⚠️ Weaknesses")
        for item in feedback.get("weaknesses", []):
            st.write(f"- {item}")

        st.markdown("### 💡 Suggestions")
        for item in feedback.get("suggestions", []):
            st.write(f"- {item}")

# ----------------------------
# Final Report
# ----------------------------

if session.is_completed:

    st.divider()

    st.subheader("📝 AI Interview Report")

    if (
        "final_report" not in st.session_state
        or not st.session_state.final_report
    ):

        with st.spinner("Generating report..."):

            st.session_state.final_report = generate_interview_report(
                session
            )

    st.markdown(st.session_state.final_report)

    pdf = generate_pdf(st.session_state.final_report)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf,
        file_name="Interview_Report.pdf",
        mime="application/pdf"
    )