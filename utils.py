import PyPDF2

def extract_text_from_pdf(file):
    pdf = PyPDF2.PdfReader(file.file)
    text = ""
    for page in pdf.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()