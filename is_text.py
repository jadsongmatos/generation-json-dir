import os
import magic
import chardet
import toml
import csv
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import patoolib
from email import policy
from email.parser import BytesParser
from docx2python import docx2python
import pandas as pd
import subprocess

def is_mime_text(mime_type):
    return 'text' in mime_type
    #text_based_mime_types = ['text']
    #return mime_type and any(mime_type.startswith(type) for type in text_based_mime_types):

def is_csv(file_path):
    delimiters = [',', ';', '\t']
    for delimiter in delimiters:
        try:
            # Tente abrir e analisar o arquivo como CSV
            with open(file_path, 'r') as file:
                reader = csv.reader(file, delimiter=delimiter)
                # Verifica se consegue ler pelo menos uma linha
                _ = next(reader)
            return True
        except Exception as e:
            continue
    return False

def is_csv_pd(file_path):
    try:
        df = pd.read_csv(file_path)
        return True
    except Exception as e:
        return False
    
def pptx_to_png(filename):
    # Certifique-se de que o arquivo existe
    if not os.path.isfile(filename):
        print(f"O arquivo {filename} não existe.")
        return

    # Converter o arquivo usando LibreOffice
    command = ["libreoffice", "--headless", "--convert-to", "png", filename]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()

    if process.returncode != 0 or stderr:
        print(f"Ocorreu um erro ao converter {filename} para png.")
        print(stderr)
    else:
        print(f"Conversão bem sucedida! {filename} convertido para png.")

    
def is_fwf(file_path):
    try:
        # Tente abrir e analisar o arquivo como um arquivo de largura fixa
        df = pd.read_fwf(file_path)
        return True
    except Exception as e:
        return False

def is_json(file_path):
    try:
        with open(file_path, 'r') as file:
            json.load(file)
        return True
    except (json.JSONDecodeError, IOError):
        return False
    
def is_pickle(file_path):
    try:
        # Tente abrir e analisar o arquivo como um pickle
        df = pd.read_pickle(file_path)
        return True
    except Exception as e:
        return False

def is_mime_xml(mime_type):
    return 'xml' in mime_type

def is_docx(file_path):
    try:
        with docx2python(file_path) as docx_content:
            #print(docx_content.text)
            return True
    except Exception as e:
        return False

def is_stata(file_path):
    try:
        # Tente abrir e analisar o arquivo como um arquivo Stata
        df = pd.read_stata(file_path)
        return True
    except Exception as e:
        return False
    
def is_excel(file_path):
    try:
        # Tente abrir e analisar o arquivo como um arquivo Excel
        df = pd.read_excel(file_path)
        return True
    except Exception as e:
        return False
    
def is_parquet(file_path):
    try:
        # Tente abrir e analisar o arquivo como um arquivo Parquet
        df = pd.read_parquet(file_path)
        return True
    except Exception as e:
        return False
        
def is_hdf(file_path):
    try:
        # Tente abrir e analisar o arquivo como um arquivo HDF5
        df = pd.read_hdf(file_path)
        return True
    except Exception as e:
        return False
    
def is_sas(file_path):
    try:
        # Tente abrir e analisar o arquivo como um arquivo SAS
        df = pd.read_sas(file_path)
        return True
    except Exception as e:
        return False

def is_xml(file_path):
    try:
        # Tente abrir e analisar o arquivo como XML
        with open(file_path, 'r') as file:
            ET.parse(file)
        return True
    except ET.ParseError as e:
        # O arquivo não é um XML válido
        return False
    except Exception as e:
        # Outros erros (como o arquivo não existir)
        return False

def is_latex(mime_type):
   return 'latex' in mime_type 

def is_toml(file_path):
    try:
        # Tente abrir e analisar o arquivo como TOML
        with open(file_path, 'r') as file:
            toml.load(file)
        return True
    except Exception as e:
        return False

def is_html(file_path):
    try:
        with open(file_path, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
        if soup.find():
            return True
        else:
            return False
    except IOError:
        return False

def is_chardet(file_path):
    try:
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read(1024))
            print("chardet",result)
        return result['encoding'] in ['ascii', 'utf-8', 'iso-8859-1', 'utf-16', 'utf-32']
    except IOError:
        return False

def is_eml(file_path):
    try:
        # Tente abrir e analisar o arquivo como EML
        with open(file_path, 'rb') as file:
            msg = BytesParser(policy=policy.default).parse(file)
        return True
    except Exception as e:
        return False

def is_compression(file_path):
    extensions = [
        '7z','cb7',       # 7z
        'ace','cba',
        'adf',
        'alz',            # ALZIP
        'ape',
        'a',              # AR
        'arc',
        'arj',
        'bz2',            # BZIP2
        'cab',            # CAB
        'z',              # COMPRESS
        'cpio',
        'deb',
        'dms',
        'flac',
        'gz',             # GZIP
        'iso',
        'lrz',            # LRZIP
        'lha','lzh',      # LZH
        'lz',             # LZIP
        'lzma',
        'lzo',
        'rpm',
        'rar','cbr',      # RAR
        'rz',             # RZIP
        'shn',
        'tar','cbt',      # TAR
        'xz',
        'zip','jar','cbz',# ZIP
        'zoo'
        ]
    _, file_extension = os.path.splitext(file_path)
    if file_extension in extensions:
        return True
    else:
        return False

def is_extensions(file_path):
    extensions = [
        '.log',
        '.diff','.patch',
        '.eml','.emlx','.msg','.mbx',
        'org', # Text
        'dat', # Text and Binary
        'adoc', # Text
        'san', # Text
        '.ly', '.ily'
        ]
    _, file_extension = os.path.splitext(file_path)
    if file_extension in extensions:
        return True
    else:
        return False

def is_text_file(file_path):
    try:
        m = magic.Magic()
        mime_type = m.from_file(file_path)
        print("mime_type",mime_type)
        print("is_mime_text",is_mime_text(mime_type))
        print("is_mime_xml",is_mime_xml(mime_type))
        print("is_latex",is_latex(mime_type))
        print("is_xml",is_xml(file_path))
        print("is_html",is_html(file_path))
        print("is_toml",is_toml(file_path))
        print("is_json",is_json(file_path))
        print("is_eml",is_eml(file_path))
        print("is_csv",is_csv(file_path))
        print("is_chardet",is_chardet(file_path))
        print("is_extensions",is_extensions(file_path))
    except IOError:
        return False

#Makefile
#LICENSE
#Dockerfile
#WordPerfect Documents: .wpd
#PDF

print("\n\nText .txt\n")
is_text_file("./ex/text/test.txt")

print("\n\nText sem extensão\n")
is_text_file("./ex/text/test")

print("\n\nText .diff\n")
is_text_file("./ex/text/test.diff")

print("\n\nText .json\n")
is_text_file("./ex/text/test.json")

print("\n\nText .csv\n")
is_text_file("./ex/text/test.csv")

print("\n\nText .xml\n")
is_text_file("./ex/text/test.xml")

print("\n\nText extensão desconhecido\n")
is_text_file("./ex/text/test.aa")

print("\n\nCSV\n")
is_text_file("./ex/csv/test.csv")
