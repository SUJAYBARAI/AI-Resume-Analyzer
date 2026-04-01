import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm")

IMPORTANT_SKILLS = [
    "python", "machine learning", "sql", "excel",
    "data analysis", "nlp", "deep learning", "fastapi",
    "pandas", "numpy"
]

def calculate_similarity(resume, job_desc):
    tfidf = TfidfVectorizer(stop_words="english")
    vectors = tfidf.fit_transform([resume, job_desc])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)

def extract_skills(text):
    doc = nlp(text)
    skills = set()

    for token in doc:
        if token.text.lower() in IMPORTANT_SKILLS:
            skills.add(token.text.lower())

    return list(skills)

def calculate_final_score(similarity, resume_skills, job_skills):
    skill_match = len(set(resume_skills) & set(job_skills)) / (len(job_skills) + 1)
    final_score = (0.7 * similarity) + (0.3 * skill_match * 100)
    return round(final_score, 2)