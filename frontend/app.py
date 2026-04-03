from fastapi import FastAPI, UploadFile, File, Form
from backend.utils import extract_text_from_pdf
from backend.model import calculate_similarity

app = FastAPI(title="AI Resume Analyzer")

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), job_desc: str = Form(...)):
    try:
        contents = await file.read()

        if not contents:
            return {"error": "Empty file uploaded"}

        resume_text = extract_text_from_pdf(contents)

        if not resume_text.strip():
            return {"error": "Could not extract text from PDF"}

        similarity = calculate_similarity(resume_text, job_desc)

        return {
            "similarity": similarity,
            "final_score": similarity,
            "resume_skills": [],
            "missing_skills": []
        }

    except Exception as e:
        return {"error": str(e)}