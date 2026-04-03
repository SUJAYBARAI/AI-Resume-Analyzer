from PyPDF2 import PdfReader
import io

def extract_text_from_pdf(file_bytes):
    try:
        pdf = PdfReader(io.BytesIO(file_bytes))
        text = ""

        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted

        return text.lower()

    except Exception as e:
        return ""