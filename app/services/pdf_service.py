import io

from pypdf import PdfReader

# Guard against extremely large PDFs blowing up the model's context window.
MAX_CHARS = 120_000


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file's raw bytes, page by page."""
    reader = PdfReader(io.BytesIO(pdf_bytes))

    pages = []
    for index, page in enumerate(reader.pages):
        text = (page.extract_text() or "").strip()
        if text:
            pages.append(f"--- Page {index + 1} ---\n{text}")

    full_text = "\n\n".join(pages)

    return full_text[:MAX_CHARS]