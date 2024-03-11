from langchain.document_loaders import Docx2txtLoader, PyPDFLoader
import os
import io

def load_pdf_docx(file_path):
    if os.path.basename(file_path).endswith(".pdf") or os.path.basename(file_path).endswith(".PDF"):
        loader =  PyPDFLoader(file_path)
    elif os.path.basename(file_path).endswith(".docx") or os.path.basename(file_path).endswith(".DOCX"):
        loader = Docx2txtLoader(file_path)
    else :
        raise ValueError("Not the PDF or DOCX file ")
    
    documents = loader.load_and_split()

    return documents

def get_cv(filename: str):
    file_path = filename
    data = load_pdf_docx(file_path=file_path)

    _context = ""
    for x in data:
        non_empty_lines = [line.strip() for line in x.page_content.splitlines() if line.strip()]
        _context += "\n".join(non_empty_lines) + "\n"

    return _context

file = "Input file Docx/PDF"
cv_text = get_cv(file)
print(cv_text)
