import streamlit as st
import requests

API_URL = "https://ai-resume-analyzer-0h1a.onrender.com"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🚀", layout="wide")

# 🌈 Modern CSS
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #00ADB5;
}
.sub-text {
    text-align: center;
    color: #AAAAAA;
    margin-bottom: 30px;
}
.card {
    background: linear-gradient(145deg, #1E1E1E, #2A2A2A);
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 10px rgba(0,173,181,0.2);
}
.stButton>button {
    width: 100%;
    background-color: #00ADB5;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# 🧠 Title Section
st.markdown('<div class="main-title">🚀 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Analyze your resume using AI & get instant feedback</div>', unsafe_allow_html=True)

# 📂 Input Section
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Upload Resume")
    file = st.file_uploader("", type=["pdf"])

with col2:
    st.markdown("### 📝 Job Description")
    job_desc = st.text_area("", height=200)

# 🚀 Analyze Button
if st.button("🚀 Analyze Resume"):
    if file and job_desc:
        with st.spinner("Analyzing your resume... ⏳"):
            response = requests.post(
                f"{API_URL}/analyze/",
                files={"file": file},
                data={"job_desc": job_desc}
            )

        if response.status_code == 200:
            res = response.json()

            if "final_score" in res:
                score = int(res["final_score"])

                # 🎯 Score Card
                st.markdown("## 🎯 Match Score")
                st.progress(score)

                if score > 75:
                    st.success(f"🔥 Excellent Match: {score}%")
                elif score > 50:
                    st.warning(f"⚡ Moderate Match: {score}%")
                else:
                    st.error(f"❌ Low Match: {score}%")

                # 📊 Skills Section
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### ✅ Your Skills")
                    for skill in res.get("resume_skills", []):
                        st.success(skill)

                with col2:
                    st.markdown("### ❌ Missing Skills")
                    if res.get("missing_skills"):
                        for skill in res["missing_skills"]:
                            st.error(skill)
                    else:
                        st.success("No missing skills 🎉")

            else:
                st.error("Invalid API response ❌")
                st.write(res)
        else:
            st.error("API request failed ❌")

# 📥 Download Section
st.markdown("---")

if st.button("📥 Generate Report"):
    if file and job_desc:
        with st.spinner("Generating report... ⏳"):
            response = requests.post(
                f"{API_URL}/download-report/",
                files={"file": file},
                data={"job_desc": job_desc}
            )

        if response.status_code == 200:
            st.success("Report Ready ✅")

            st.download_button(
                label="⬇️ Download PDF",
                data=response.content,
                file_name="resume_report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Failed to generate report ❌")