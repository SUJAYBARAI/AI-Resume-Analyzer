import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# 🎯 Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}
h1 {
    text-align: center;
    color: #00ADB5;
}
.card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# 🧠 Title
st.title("🚀 AI Resume Analyzer Pro")

# 📂 Upload + JD
col1, col2 = st.columns(2)

with col1:
    file = st.file_uploader("📄 Upload Resume (PDF)")

with col2:
    job_desc = st.text_area("📝 Paste Job Description")

# 🚀 Analyze Button
if st.button("Analyze Resume"):
    if file and job_desc:
        with st.spinner("Analyzing... ⏳"):
            res = requests.post(
                "http://127.0.0.1:8000/analyze/",
                files={"file": file},
                data={"job_desc": job_desc}
            ).json()

        # 🎯 Score Display
        st.subheader("🎯 Match Score")
        st.progress(int(res["final_score"]))
        st.success(f"{res['final_score']} % Match")

        # 📊 Layout
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ✅ Resume Skills")
            for skill in res["resume_skills"]:
                st.markdown(f"- {skill}")

        with col2:
            st.markdown("### ❌ Missing Skills")
            if res["missing_skills"]:
                for skill in res["missing_skills"]:
                    st.markdown(f"- {skill}")
            else:
                st.success("No missing skills 🎉")

# 📥 Download Report
st.markdown("---")

if st.button("📥 Generate Report"):
    if file and job_desc:
        with st.spinner("Generating report... ⏳"):
            res = requests.post(
                "http://127.0.0.1:8000/download-report/",
                files={"file": file},
                data={"job_desc": job_desc}
            )

        if res.status_code == 200:
            st.success("Report Ready ✅")

            st.download_button(
                label="⬇️ Download PDF",
                data=res.content,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Failed to generate report ❌")