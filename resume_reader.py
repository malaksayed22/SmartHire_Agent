import pdfplumber
from docx import Document
import os

def extract_text(file_path: str) -> str:
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_path.endswith(".pdf"):
        return extract_from_pdf(file_path)
    
    elif file_path.endswith(".docx"):
        return extract_from_docx(file_path)
    
    else:
        raise ValueError("Unsupported format. Use PDF or DOCX only.")


def extract_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    if not text.strip():
        raise ValueError("Could not extract text from PDF. File may be scanned.")
    
    return text.strip()


def extract_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text + "\n"
    
    if not text.strip():
        raise ValueError("Could not extract text from DOCX. File may be empty.")
    
    return text.strip()

if __name__ == "__main__":
    print("Resume Reader ready")
    print("Supported formats: PDF, DOCX")