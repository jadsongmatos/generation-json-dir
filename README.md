# Gerador de resumo de diretorios

O gerador lê todos os arquivos de texto em um diretório fornecido (incluindo subdiretórios) e utiliza o modelo BigBird-Pegasus do Google para gerar um resumo do conteúdo de cada arquivo.

Os resultados são então armazenados em um arquivo JSON. O arquivo JSON final terá a mesma estrutura de diretórios que o diretório fornecido, mas com cada arquivo de texto substituído por seu resumo.

## Uso

Para usar este script, substitua a variável `dir_path` pelo caminho do diretório que você deseja analisar e a variável `output_file` pelo nome do arquivo JSON de saída.

Então, execute o script. Ele irá percorrer todos os arquivos de texto no diretório fornecido (e em seus subdiretórios), gerar um resumo para cada arquivo e escrever o resultado em um arquivo JSON.

```python
dir_path = './meu_diretorio'  # substitua pelo seu diretório
output_file = 'meu_arquivo.json'  # substitua pelo nome do seu arquivo de saída

file_dict = list_files(dir_path)
to_json(file_dict, output_file)
```

## Requisitos

- Python 3.6+
- Bibliotecas Python:
  - `os`
  - `json`
  - `mimetypes`
  - `transformers` (da Hugging Face)

## Observações

- Este script assume que todos os arquivos que ele está lendo são de texto. Se um arquivo não for de texto (ou se não puder ser lido), o script irá ignorá-lo.
- O modelo BigBird-Pegasus é bastante grande e pode consumir uma quantidade significativa de memória. Se você estiver tendo problemas com falta de memória, pode tentar executar o script em um computador com mais memória.
- A qualidade do resumo gerado depende do modelo e do texto de entrada. Como tal, os resumos podem não ser perfeitos e podem não capturar todos os detalhes importantes do texto original.
- Este script foi projetado para uso com o modelo `google/bigbird-pegasus-large-arxiv`. Outros modelos podem exigir diferentes parâmetros ou métodos de pré-processamento de texto.