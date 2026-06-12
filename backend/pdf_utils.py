import fitz
import logging

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        logging.error(f"PDF SIZE: {len(file_bytes)} bytes")
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        logging.error(f"EXTRACTED TEXT LENGTH: {len(text)}")
        return text.strip()
    except Exception as e:
        logging.error(f"PDF ERROR: {str(e)}")
        raise