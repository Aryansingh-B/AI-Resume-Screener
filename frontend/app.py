import streamlit as st
import requests
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Resume Screener", page_icon="🤖", layout="centered")

st.title("🤖 AI Resume Screener")
st.caption("Powered by Google Gemini · Built with FastAPI + Streamlit")

st.divider()

job_desc = st.text_area(
    "📋 Paste Job Description",
    height=200,
    placeholder="e.g. We are looking for a Data Scientist with experience in Python, ML pipelines, SQL..."
)

resume_file = st.file_uploader("📄 Upload Resume (PDF only)", type=["pdf"])

if st.button("🔍 Screen Resume", use_container_width=True):
    if not job_desc.strip():
        st.warning("Please enter a job description.")
    elif resume_file is None:
        st.warning("Please upload a resume PDF.")
    else:
        with st.spinner("Analysing with Gemini AI..."):
            try:
                response = requests.post(
                    f"{API_URL}/screen-resume",
                    data={"job_description": job_desc},
                    files={"resume": (resume_file.name, resume_file, "application/pdf")},
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()

                st.divider()

                # Score gauge
                score = result["score"]
                color = "green" if score >= 70 else "orange" if score >= 50 else "red"
                st.markdown(f"### Match Score: :{color}[**{score}/100**]")
                st.progress(score / 100)

                st.divider()

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### ✅ Strengths")
                    for s in result["strengths"]:
                        st.success(s)
                with col2:
                    st.markdown("#### ❌ Gaps")
                    for g in result["gaps"]:
                        st.error(g)

                st.divider()
                st.markdown("#### 📝 Summary")
                st.info(result["summary"])

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach the API. Make sure the backend is running on port 8000.")
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Gemini took too long — please try again.")
            except requests.exceptions.HTTPError as e:
                st.error(f"🚨 API Error {e.response.status_code}: {e.response.text}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")