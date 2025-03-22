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
            return reader.pages[page_number].extract_text()
    except Exception as e:
        print(f"Error reading page {page_number + 1}: {e}")
        return None

def generate_summary(text, page_number, model):
    """Generates summary using Gemini with page number reference"""
    prompt = f"Summarize the key concepts from this text from page {page_number + 1}. Present as bullet points starting with 'Page {page_number + 1}: '. Text:\n\n{text}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error summarizing page {page_number + 1}: {e}")
        return None

def process_pdf(pdf_path, output_file, model):
    """Processes all pages of a PDF and writes summaries to file"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            with open(output_file, 'w') as f:  # Overwrite mode
                for page_number in range(total_pages):
                    text = extract_text_from_pdf(pdf_path, page_number)
                    if not text:
                        continue
                    
                    summary = generate_summary(text, page_number, model)
                    if summary:
                        f.write(summary + "\n\n")
                        print(f"Processed page {page_number + 1}/{total_pages}")
                    
    except Exception as e:
        print(f"PDF processing failed: {e}")

def main():
    # Configuration
    pdf_path = "biology-student-textbook-grade-9_cell_biology.pdf"
    output_file = "summary.txt"
    
    # Set up Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY environment variable")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Process PDF
    process_pdf(pdf_path, output_file, model)
    print(f"\nSummary complete. Results in {output_file}")

if __name__ == "__main__":
    main()