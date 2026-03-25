# 🚀 AI Resume Analyzer

An AI-powered web application that analyzes resumes and matches them with job descriptions using NLP and Machine Learning.

## 🔥 Features
- Resume parsing (PDF)
- Skill extraction using NLP (spaCy)
- Resume-job matching using TF-IDF & cosine similarity
- Final score calculation
- PDF report generation
- Interactive UI (Streamlit)

## 🧠 Tech Stack
- FastAPI
- Python
- spaCy
- Scikit-learn
- Streamlit
- ReportLab

## ▶️ How to Run

### 1. Clone repo
git clone https://github.com/SUJAYBARAI/AI-Resume-Analyzer.git

### 2. Install dependencies
pip install -r requirements.txt

### 3. Install spaCy model
python -m spacy download en_core_web_sm

### 4. Run backend
cd backend
uvicorn main:app --reload

### 5. Run frontend
cd frontend
streamlit run app.py

## 📸 Demo
(Add screenshots here)

## 💯 Author
Sujay Barai
