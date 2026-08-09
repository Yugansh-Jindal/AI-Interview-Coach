import fitz
import pdfplumber


def extract_text(pdf_path):
    text = ""

    # Try PyMuPDF first
    try:
        doc = fitz.open(pdf_path)

        for page in doc:
            text += page.get_text()

        doc.close()

        if text.strip():
            return text

    except Exception as e:
        pass

    # Fallback to pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        pass

    return text