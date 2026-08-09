import streamlit as st
import pandas as pd

from auth.session_manager import (
    is_logged_in,
    get_current_user,
)

from database.database import (
    get_average_score,
    get_best_score,
    get_total_interviews,
    get_total_questions,
    get_score_history,
    get_topic_performance,
)

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Interview Analytics")

# -------------------------------------
# Login Check
# -------------------------------------

if not is_logged_in():

    st.warning("Please login first.")

    st.switch_page("pages/login.py")

user = get_current_user()

# -------------------------------------
# Load Analytics
# -------------------------------------

total_interviews = get_total_interviews(user["id"])
average_score = get_average_score(user["id"])
best_score = get_best_score(user["id"])
total_questions = get_total_questions(user["id"])

# -------------------------------------
# Summary Cards
# -------------------------------------

col1, col2, col3, col4 = st.columns([1.3, 1, 1, 1.3])

with col1:
    st.metric(
        "Total Interviews",
        total_interviews
    )

with col2:
    st.metric(
        "Average Score",
        f"{average_score}/10"
    )

with col3:
    st.metric(
        "Best Score",
        f"{best_score}/10"
    )

with col4:
    st.metric(
        "Questions Answered",
        total_questions
    )

# -------------------------------------
# Score History
# -------------------------------------

score_history = get_score_history(user["id"])

if score_history:

    st.divider()

    st.subheader("📈 Score History")

    chart_data = pd.DataFrame(score_history)

    chart_data["Interview"] = (
    "Interview " + chart_data["id"].astype(str)
    )

    chart_data = chart_data.set_index("Interview")

    st.line_chart(chart_data["overall_score"])

else:

    st.info("Complete an interview to view your score history.")

# -------------------------------------
# Topic Performance
# -------------------------------------

topic_data = get_topic_performance(user["id"])

if topic_data:

    st.divider()

    st.subheader("📊 Topic Performance")

    topic_df = pd.DataFrame(topic_data)

    topic_df = topic_df.sort_values(
    by="average_score",
    ascending=False
)

    topic_df = topic_df.set_index("topic")

    st.bar_chart(topic_df["average_score"])

else:

    st.info("Topic performance will appear after completing interviews.")   