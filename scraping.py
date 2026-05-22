import os
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Extraindo a data para usar como parâmetro no nome do arquivo
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# Configuração de pastas
PASTA_XML = r"C:\XMLCTE"
ARQUIVO_SAIDA = fr"C:\Users\felipe.rodrigues\python-portable\extract_keys\keys_extracts_{yesterday}.csv"

# Namespace padrão da SEFAZ para CT-e
NAMESPACE = {'ns': 'http://www.portalfiscal.inf.br/cte'}

def extract_data():
    data = []

    # Percorrer todos os arquivos dentro da pasta
    for ctes in os.listdir(PASTA_XML):
        if ctes.lower().endswith('.xml'):
            folder_path = os.path.join(PASTA_XML, ctes)

            try:
                # Ler toda a árvore do XML
                tree = ET.parse(folder_path)
                root = tree.getroot()

                # Buscar o número do CT-e (Tag <nCT>)
                tag_nct = root.find('.//ns:nCT', NAMESPACE)
                numero_cte = tag_nct.text if tag_nct is not None else "Sem número"

                # Buscar todas as chaves de NF-e vinculadas ao CT-e (<infNfe>)
                tags_chave_nfe = root.findall('.//ns:infNFe/ns:chave', NAMESPACE)

                # Extrair e gravar todas as chaves encontradas associadas ao número do CT-e
                for tag in tags_chave_nfe:
                    data.append({
                        'Numero_CTE': numero_cte,
                        'Chave_NFE': tag.text
                    })
            # Lançando exceções caso não consiga ler o XML do CT-e
            except ET.ParseError:
                print(f"Erro ao ler o arquivo (XML Corrompido): {ctes}")
            except Exception as e:
                print(f"Erro inesperado no arquivo {ctes}: {e}")

    # Gerando CSV para os arquivos extraídos
    with open(ARQUIVO_SAIDA, mode='w', newline='', encoding='utf-8') as csv_file:
        columns = ['Numero_CTE', 'Chave_NFE']
        writer = csv.DictWriter(csv_file, fieldnames=columns, delimiter=';')

        writer.writeheader()
        for line in data:
            writer.writerow(line)

    print(f"Sucesso! Extração concluída. Total de notas encontradas: {len(data)}")
    print(f"Arquivo salvo em: {ARQUIVO_SAIDA}")

# Execute script
if __name__ == "__main__":
    extract_data()

