import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from PDF.
    """

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from DOCX.
    """

    document = Document(file_path)

    text = []

    for paragraph in document.paragraphs:
        text.append(paragraph.text)

    return "\n".join(text)