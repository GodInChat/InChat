from pypdf import PdfReader

def process_pdf(file) -> str:
    reader = PdfReader(file)
    text_pages = []
    for page in reader.pages:
        text_pages.append(page.extract_text())
    text = "".join(text_pages)
    return text