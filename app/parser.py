import fitz  # PyMuPDF
import requests

def parse_document(url: str) -> str:
    """Download PDF from URL and extract text."""
    try:
        # Download PDF
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return None

        with open("temp.pdf", "wb") as f:
            f.write(response.content)

        # Extract text
        doc = fitz.open("temp.pdf")
        text = "\n".join(page.get_text() for page in doc)
        return text.strip()
    except Exception:
        return None
