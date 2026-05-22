## Scraping de XML feito em python

1. Recebe uma pasta com 1 ou mais arquivos que contenham a extensão .xml
2. Varre um por um capturando o número do CT-e se não for nulo através da tag <nCT>
3. Captura uma ou mais notas associadas ao número do CT-e que foi encontrado através da tag <infNFe>
4. Extrai a chave de acesso de todas as notas fiscais encontradas no XML
5. Gera um CSV com duas colunas: Numero do CT-e e Chave de acesso da NFe

### Como executar?

- Crie uma pasta para o armazenamento de XMLs
- Mude as variáveis de caminho
- Adapte o código com as demais colunas que precisar

>No terminal execute: .\interpretador .\scraping\scraping.py

````
Configurações de pasta

PASTA_XML = r"C:\O\Seu\Caminho\Relativo"
ARQUIVO_SAIDA = fr"C:\O\Seu\Caminho\Relativo\nome_do_arquivo_{yesterday}.csv"
````