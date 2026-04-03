from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from backend.utils import extract_text_from_pdf
from backend.model import calculate_similarity

app = FastAPI(title="AI Resume Analyzer")

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...), job_desc: str = Form(...)):
    try:
        contents = await file.read()

        resume_text = extract_text_from_pdf(contents)

        similarity = calculate_similarity(resume_text, job_desc)

        return {
            "similarity": similarity,
            "final_score": similarity,  # simple for now
            "resume_skills": [],
            "missing_skills": []
        }

    except Exception as e:
        return {"error": str(e)}