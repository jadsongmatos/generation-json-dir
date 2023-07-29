from docx2python import docx2python

def is_docx(file_path):
    try:
        with docx2python(file_path) as docx_content:
            #print(docx_content.text)
            return True
    except Exception as e:
        return False