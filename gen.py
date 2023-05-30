import os
import json

import mimetypes

from transformers import BigBirdPegasusForConditionalGeneration, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("google/bigbird-pegasus-large-arxiv")
# decoder attention type can't be changed & will be "original_full"
# you can change `attention_type` (encoder only) to full attention like this:
# by default encoder-attention is `block_sparse` with num_random_blocks=3, block_size=64
model = BigBirdPegasusForConditionalGeneration.from_pretrained(
    "google/bigbird-pegasus-large-arxiv", attention_type="block_sparse")


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


dir_path = './ra'  # caminho para a pasta
output_file = 'arquivos.json'  # arquivo JSON de saída

file_dict = list_files(dir_path)
to_json(file_dict, output_file)
