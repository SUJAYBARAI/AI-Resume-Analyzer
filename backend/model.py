import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Safe load (Render pe crash avoid karega)
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None

IMPORTANT_SKILLS = [
    "python", "machine learning", "sql", "excel",
    "data analysis", "nlp", "deep learning", "fastapi",
    "pandas", "numpy", "flask", "django", "api"
]

# 🔥 1. Better similarity (safe)
def calculate_similarity(resume, job_desc):
    try:
        tfidf = TfidfVectorizer(stop_words="english")
        vectors = tfidf.fit_transform([resume, job_desc])
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(score * 100, 2)
    except:
        return 0.0


# 🔥 2. Improved skill extraction (phrase support + fallback)
def extract_skills(text):
    text = text.lower()
    skills = set()

    # ✅ Direct keyword match (important for phrases like "machine learning")
    for skill in IMPORTANT_SKILLS:
        if skill in text:
            skills.add(skill)

    # ✅ Optional NLP enhancement
    if nlp:
        doc = nlp(text)
        for token in doc:
            if token.text.lower() in IMPORTANT_SKILLS:
                skills.add(token.text.lower())

    return list(skills)


# 🔥 3. Better scoring logic
def calculate_final_score(similarity, resume_skills, job_skills):
    try:
        if not job_skills:
            return similarity

        matched = len(set(resume_skills) & set(job_skills))
        skill_score = (matched / len(job_skills)) * 100

        final_score = (0.7 * similarity) + (0.3 * skill_score)
        return round(final_score, 2)

    except:
        return similarity