# Introdução e filosofia da implementação

Esse repositório é uma iniciativa, por parte da PDI, de criar ferramentas para pós-processamento de resultados experimentais. Tais ferramentas serão auditáveis, abertas, e com o intuito de ser colaborativa.

# Passos para gerar o build

- Criar uma pasta dentro de src, com o nome do package

## Configurar arquivo .toml

- Desenvolder todo o projeto na pasta acima
- Alterar o nome do projeto no arquivo pyproject.toml
- Modificar o número de versão
- Conferir o tipo de licença
- Configurar as urls (opicional)

## Gerar os arquivos da distribuição
Primeiro instalar:
'''
py -m pip install --upgrade build
'''
Depois:

'''
py -m build
'''

## Fazer upload dos arquivos de distribuição

'''
py -m pip install --upgrade twine
'''

'''
py -m twine upload --repository pypi dist/*
'''

Obs.: É necessário gerar o token


