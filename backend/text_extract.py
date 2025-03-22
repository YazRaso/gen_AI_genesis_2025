from PyPDF2 import PdfReader

def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

text = extract_text("biology-student-textbook-grade-9_cell_biology.pdf")
print(text)  # Send this text to Gemini