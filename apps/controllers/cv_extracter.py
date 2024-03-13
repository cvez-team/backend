import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader


def load_pdf_docx(file_path):
    '''
    Load the PDF or DOCX file and split the content into the list of documents.
    '''
    if os.path.basename(file_path).endswith(".pdf") or os.path.basename(file_path).endswith(".PDF"):
        loader = PyPDFLoader(file_path)

    elif os.path.basename(file_path).endswith(".docx") or os.path.basename(file_path).endswith(".DOCX"):
        loader = Docx2txtLoader(file_path)

    else:
        raise ValueError("File must be the PDF or DOCX file.")

    # Load and split the content
    return loader.load_and_split()


def get_cv_content(filename: str):
    '''
    Get the content of the CV file. Weathers it is a PDF or DOCX file.
    '''
    data = load_pdf_docx(file_path=filename)

    _content = ""
    for x in data:
        non_empty_lines = [line.strip()
                           for line in x.page_content.splitlines() if line.strip()]
        _content += "\n".join(non_empty_lines) + "\n"

    return _content
