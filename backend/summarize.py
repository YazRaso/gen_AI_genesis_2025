import PyPDF2
import os
import google.generativeai as genai

def extract_text_from_pdf(pdf_path, page_number):
    """Extracts text from a specific page in a PDF"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if page_number < 0 or page_number >= len(reader.pages):
                raise ValueError("Invalid page number")
            
            page = reader.pages[page_number]
            return page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

def generate_summary(text, page_number, model):
    """Generates summary using Gemini with page number reference"""
    prompt = f"Summarize the key concepts from the following text which comes from page {page_number + 1} of a document. Present the summary as a bulleted list where each item starts with 'Page {page_number + 1}: '. Text:\n\n{text}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None

def main():
    # Configuration
    pdf_path = "biology-student-textbook-grade-9_cell_biology.pdf"  # Replace with your PDF path
    page_number = 0  # Zero-based index (0 = first page)
    output_file = "summary.txt"
    
    # Set up Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY environment variable")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path, page_number)
    if not text:
        return
    
    # Generate summary
    summary = generate_summary(text, page_number, model)
    if not summary:
        return
    
    # Save to file and print
    with open(output_file, 'w') as f:
        f.write(summary)
    
    print(f"Summary saved to {output_file}:\n\n{summary}")

if __name__ == "__main__":
    main()