from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
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

        # ✅ SAFE similarity
        try:
            similarity = calculate_similarity(resume_text, job_desc)
        except:
            similarity = 50  # fallback

        return {
            "similarity": similarity,
            "final_score": similarity,
            "resume_skills": [],
            "missing_skills": []
        }

    except Exception as e:
        return {"error": str(e)}


@app.post("/download-report/")
async def download_report(file: UploadFile = File(...), job_desc: str = Form(...)):
    try:
        contents = await file.read()

        if not contents:
            return {"error": "Empty file"}

        resume_text = extract_text_from_pdf(contents)

        if not resume_text.strip():
            return {"error": "PDF text extraction failed"}

        similarity = calculate_similarity(resume_text, job_desc)

        # simple dummy PDF (safe)
        file_path = "report.pdf"

        with open(file_path, "w") as f:
            f.write(f"Resume Score: {similarity}")

        return FileResponse(file_path, media_type="application/pdf", filename="report.pdf")

    except Exception as e:
        return {"error": str(e)}