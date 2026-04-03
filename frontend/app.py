import streamlit as st
import requests

API_URL = "https://ai-resume-analyzer-0h1a.onrender.com"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="🚀", layout="wide")

# 🎨 Advanced CSS
st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #00ADB5;
}
.card {
    background: linear-gradient(145deg, #1e1e1e, #2a2a2a);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 0px 10px rgba(0,173,181,0.2);
}
.metric-box {
    background-color: #111;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 🎯 Sidebar
st.sidebar.title("⚙️ Settings")
st.sidebar.markdown("### 🧠 AI Resume Analyzer")
st.sidebar.info("Upload your resume and get smart feedback instantly.")

# 🧠 Header
st.markdown('<div class="main-title">🚀 AI Resume Analyzer Dashboard</div>', unsafe_allow_html=True)
st.markdown("Analyze your resume using AI & improve your chances 🚀")

# 📂 Inputs
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📄 Upload Resume")
    file = st.file_uploader("", type=["pdf"])

with col2:
    st.markdown("### 📝 Job Description")
    job_desc = st.text_area("", height=200)

# 🚀 Analyze Button
if st.button("🚀 Analyze Resume"):
    if file and job_desc:
        try:
            with st.spinner("🔍 AI is analyzing your resume..."):
                response = requests.post(
                    f"{API_URL}/analyze/",
                    files={"file": file},
                    data={"job_desc": job_desc},
                    timeout=60
                )

            if response.status_code == 200:
                res = response.json()

                if "error" in res:
                    st.error(res["error"])
                else:
                    score = int(res.get("final_score", 0))

                    # 🎯 Metrics Row
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("📊 Match Score", f"{score}%")

                    with col2:
                        st.metric("✅ Skills Found", len(res.get("resume_skills", [])))

                    with col3:
                        st.metric("❌ Missing Skills", len(res.get("missing_skills", [])))

                    st.markdown("---")

                    # 🎯 Progress Bar
                    st.subheader("🎯 Resume Match Strength")
                    st.progress(score)

                    # 📊 Skills Section
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 🟢 Your Skills")
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        for skill in res.get("resume_skills", []):
                            st.success(skill)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col2:
                        st.markdown("### 🔴 Missing Skills")
                        st.markdown('<div class="card">', unsafe_allow_html=True)
                        if res.get("missing_skills"):
                            for skill in res["missing_skills"]:
                                st.error(skill)
                        else:
                            st.success("No missing skills 🎉")
                        st.markdown('</div>', unsafe_allow_html=True)

            else:
                st.error("API request failed ❌")

        except:
            st.error("⚠️ Server waking up... try again in 30 sec")

# 📥 Download Section
st.markdown("---")

if st.button("📥 Generate PDF Report"):
    if file and job_desc:
        try:
            with st.spinner("📄 Generating report..."):
                response = requests.post(
                    f"{API_URL}/download-report/",
                    files={"file": file},
                    data={"job_desc": job_desc},
                    timeout=60
                )

            if response.status_code == 200:
                st.success("✅ Report Ready")

                st.download_button(
                    label="⬇️ Download Report",
                    data=response.content,
                    file_name="resume_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Failed to generate report ❌")

        except:
            st.error("Server error ❌")