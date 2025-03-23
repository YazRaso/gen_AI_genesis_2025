from PyPDF2 import PdfReader
from gemini.utils import prompt_gemini
import time

def extract_text(pdf_path, md_path):
    reader = PdfReader(pdf_path)
    with open(md_path, 'a') as f:
        for i, page in enumerate(reader.pages):
            try:
                md_text = prompt_gemini(f"{page.extract_text()} Write this file in markdown with the titles as headers and verbosely written paragraphs in Spanish?")
                f.write(md_text)
                time.sleep(10)
            except Exception as e:
                print(f"Error processing page {i+1}: {str(e)}")
                continue

extract_text("chemistry-students-textbook-grade-9_chemical_bonding_intermolecular_forces.pdf", "chem_lesson_es.md")