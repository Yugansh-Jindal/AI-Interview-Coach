import os

import streamlit as st

from services.pdf_service import extract_text
from rag.chunker import chunk_text
from rag.vector_store import (
    store_chunks,
    clear_vector_store
)

from auth.session_manager import (
    get_current_user,
    is_logged_in,
)

from services.document_service import (
    save_resume,
    save_job_description,
)

st.set_page_config(
    page_title="Upload Documents",
    page_icon="📄"
)

st.title("📄 Upload Resume & Job Description")

if not is_logged_in():
    st.switch_page("pages/login.py")

user = get_current_user()

st.write(
    "Upload your resume and job description to prepare your interview."
)


resume = st.file_uploader(
    "Upload Resume",
    type=["pdf"],
    key="resume"
)

job_description = st.file_uploader(
    "Upload Job Description",
    type=["pdf"],
    key="job_description"
)

if st.button("Process Documents"):

    if resume is None or job_description is None:

        st.warning("Please upload both documents.")

    else:

        clear_vector_store(user["id"])

        resume_path = save_resume(
            user["id"],
            resume
)

        job_path = save_job_description(
             user["id"],
            job_description
)
        with st.spinner("Processing Resume..."):

            resume_text = extract_text(resume_path)

            resume_chunks = chunk_text(resume_text)

        store_chunks(
            resume_chunks,
            "resume",
            user["id"]
    )

        with st.spinner("Processing Job Description..."):

            job_text = extract_text(job_path)

            job_chunks = chunk_text(job_text)

            store_chunks(
                job_chunks,
                    "job_description",
                    user["id"]
        )

        st.success("Documents processed successfully.")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Resume Chunks",
                len(resume_chunks)
            )

        with col2:

            st.metric(
                "Job Description Chunks",
                len(job_chunks)
            )

        with st.expander("Resume Preview"):

            st.text_area(
                "Resume",
                resume_text,
                height=300,
                disabled=True
            )

        with st.expander("Job Description Preview"):

            st.text_area(
                "Job Description",
                job_text,
                height=300,
                disabled=True
            )

        st.success("Ready to start the interview.")

        if st.button("🚀 Start Interview"):
            st.switch_page("pages/interview.py")