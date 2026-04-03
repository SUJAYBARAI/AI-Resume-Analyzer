from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from backend.utils import extract_text_from_pdf
from backend.model import calculate_similarity, extract_skills, calculate_final_score
from backend.report import generate_report

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

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_desc)

        missing_skills = list(set(job_skills) - set(resume_skills))

        final_score = calculate_final_score(similarity, resume_skills, job_skills)

        return {
            "similarity": similarity,
            "final_score": final_score,
            "resume_skills": resume_skills,
            "missing_skills": missing_skills
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/download-report/")
async def download_report(file: UploadFile = File(...), job_desc: str = Form(...)):
    try:
        contents = await file.read()
        resume_text = extract_text_from_pdf(contents)

        similarity = calculate_similarity(resume_text, job_desc)
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_desc)

        missing_skills = list(set(job_skills) - set(resume_skills))
        final_score = calculate_final_score(similarity, resume_skills, job_skills)

        data = {
            "final_score": final_score,
            "resume_skills": resume_skills,
            "missing_skills": missing_skills
        }

        file_path = generate_report(data)

        return FileResponse(file_path, media_type="application/pdf", filename="resume_report.pdf")

    except Exception as e:
        return {"error": str(e)}