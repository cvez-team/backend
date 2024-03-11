from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
import os


def load_pdf_docx(file_path):
    if os.path.basename(file_path).endswith(".pdf") or os.path.basename(file_path).endswith(".PDF"):
        loader =  PyPDFLoader(file_path)
    elif os.path.basename(file_path).endswith(".docx") or os.path.basename(file_path).endswith(".DOCX"):
        loader = Docx2txtLoader(file_path)
    
    documents = loader.load_and_split()

    return documents

def get_cv(file_name):
    file_path = file_name

    data = load_pdf_docx(file_path=file_path)
    _context = ""
    for x in data:
        lines = x.page_content.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        _context += '\n'.join(non_empty_lines) + "\n"

    return _context.strip()
