import os
import json
import yaml
import mimetypes

import magic
from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-arxiv")
# decoder attention type can't be changed & will be "original_full"
# you can change `attention_type` (encoder only) to full attention like this:
# by default encoder-attention is `block_sparse` with num_random_blocks=3, block_size=64
model = BigBirdPegasusForConditionalGeneration.from_pretrained(
    "google/bigbird-pegasus-large-arxiv", attention_type="block_sparse")

# Function to create segments
def create_segments(text):
    # text into sentences
    sentences = text.splitlines()

    segments = []
    current_segment = []
    current_token_count = 0

    for sentence in sentences:
        tokens = tokenizer(sentence, return_tensors='pt')["input_ids"]
        token_count = len(tokens)

        if current_token_count + token_count < 86683:
            current_segment.append(sentence)
            current_token_count += token_count
        else:
            segments.append(current_segment)
            current_segment = [sentence]
            current_token_count = token_count

    if current_segment:
        segments.append(current_segment)

    return segments

def is_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            yaml.safe_load(file)
        return True
    except yaml.YAMLError:
        return False

def is_binary(file_path):
    """
    Return true if the file is binary.
    """
    with open(file_path, 'rb') as file: # abra o arquivo em modo binário
        chunk = file.read(1024) # leia os primeiros 1024 bytes
    return b'\0' in chunk

def extension_file(file_path):
    TEXT_EXTENSIONS = ['json','js','ts','jsx','tsx','xml','html','csv']
    return os.path.splitext(file_path)[1][1:].lower() in TEXT_EXTENSIONS

def is_text_file(file_path):
    """Lê o conteúdo de um arquivo de texto"""
    # Obter o tipo MIME do arquivo
    mime_type, _ = mimetypes.guess_type(file_path)
    print(file_path, mime_type)
    text_based_mime_types = ['text']
    
    not_text_based_mime_types = ['video', 'image','audio','model','font']

    if mime_type and any(mime_type.startswith(type) for type in text_based_mime_types):
        return True
    else:
        if any(mime_type in type for type in not_text_based_mime_types):
            return False
        else:
            if is_yaml(file_path):
                return True
            else:
                if is_binary(file_path):
                    return False
                else:
                    return True


def read_file_content(file_path):
    """Lê o conteúdo de um arquivo de texto"""
    # Obter o tipo MIME do arquivo
    mime_type, _ = mimetypes.guess_type(file_path)
    print(file_path, mime_type)
    # Se o arquivo for de texto, JSON ou HTML, ler o conteúdo
    text_based_mime_types = ['text', 'application/json', 'application/javascript', 'application/xml',
                             'application/xhtml+xml', 'application/csv', 'application/csv', 'application/atom+xml']

    if mime_type and any(mime_type.startswith(type) for type in text_based_mime_types):
        try:
            with open(file_path, 'r') as file:
                text = file.read(text)
                segments = create_segments()
                inputs = tokenizer(file.read(), return_tensors='pt')
                prediction = model.generate(**inputs)
                return tokenizer.batch_decode(prediction)
        except UnicodeDecodeError:
            return None  # ou retornar 'Erro: não foi possível ler o arquivo'
    else:
        return None  # ou retornar 'Erro: não é um arquivo de texto'


def list_files(dir_path):
    """Retorna um dicionário de arquivos em um diretório e seus subdiretórios"""
    file_dict = {}
    for dirpath, dirnames, filenames in os.walk(dir_path):
        # remove the initial directory path
        relative_dirpath = os.path.relpath(dirpath, dir_path)
        path_parts = relative_dirpath.split(os.path.sep)
        current_dict = file_dict
        for part in path_parts:
            if part not in current_dict:
                current_dict[part] = {}
            current_dict = current_dict[part]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            current_dict[filename] = read_file_content(file_path)
            print(filename, current_dict[filename])
    return file_dict


def to_json(file_dict, output_file):
    """Escreve o dicionário de arquivos em um arquivo JSON"""
    with open(output_file, 'w') as json_file:
        json.dump(file_dict, json_file, indent=4)


dir_path = './test'  # caminho para a pasta
output_file = 'arquivos.json'  # arquivo JSON de saída

file_dict = list_files(dir_path)
to_json(file_dict, output_file)
