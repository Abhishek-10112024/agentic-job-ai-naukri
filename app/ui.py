import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import json

st.set_page_config(page_title="Agentic Job AI", layout="wide")

st.title("🤖 Agentic AI Job Application System")

st.markdown("Find, rank, and optimize job applications using AI")

st.warning("⚠️ Demo Mode: This app shows pre-processed results. Full system runs locally with live scraping + LLM.")

# Load sample data
DATA_PATH = "data/sample_output.json"

if st.button("🚀 Run Job Pipeline (Demo)"):

    with st.spinner("Loading results..."):
        with open(DATA_PATH, "r") as f:
            result = json.load(f)

    jobs = result["jobs"]

    st.success("✅ Results loaded!")

    for i, job in enumerate(jobs):

        with st.container():
            st.subheader(f"{i+1}. {job['title']} @ {job['company']}")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Score", job["score"])
                st.write("📍 Location:", job["location"])

            with col2:
                st.write("🧠 Reason:")
                st.write(job["reason"])

            # Optional: Show description
            with st.expander("📄 Job Description"):
                st.write(job.get("description", ""))

            # Optional: Resume output (if exists)
            if "resume_content" in job:
                with st.expander("✨ Resume & Cover Message"):
                    st.text(job["resume_content"])

            st.markdown("---")