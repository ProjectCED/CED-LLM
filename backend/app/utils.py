import pymupdf

def extract_text_from_pdf(pdf_path: str) -> str:
    pdf_document = pymupdf.open(pdf_path)
    text = ""
    for page in pdf_document:
        text += page.get_text()
    pdf_document.close()
    return text


def extract_first_page_from_pdf(pdf_path: str) -> str:
    pdf_document = pymupdf.open(pdf_path)
    first_page = pdf_document[0]
    text = first_page.get_text()
    pdf_document.close()
    return text