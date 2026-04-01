from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(data, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph(f"Match Score: {data['final_score']}%", styles["Title"]))
    content.append(Paragraph(f"Resume Skills: {', '.join(data['resume_skills'])}", styles["Normal"]))
    content.append(Paragraph(f"Missing Skills: {', '.join(data['missing_skills'])}", styles["Normal"]))

    doc.build(content)

    return filename