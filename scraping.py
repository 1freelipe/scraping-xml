import os
import csv
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

yesterday = (datetime.now() - timedelta(days=21)).strftime("%Y-%m-%d")

# Configuração de pastas
PASTA_XML = r"C:\XMLCTE"
ARQUIVO_SAIDA = fr"C:\Users\felipe.rodrigues\python-portable\extract_keys\keys_extracts_{yesterday}.csv"
PATH_NAME = os.path.basename(ARQUIVO_SAIDA).lstrip('keys_extracts_')

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

    # Verificar se o arquivo já existe
    if os.path.exists(ARQUIVO_SAIDA):
        print("\nATENÇÃO!")
        print(f"O arquivo já existe:")
        print(PATH_NAME)

        response = input("Deseja sobrescrever o arquivo? (S/N)").strip().upper()

        if response != "S":
            print("\nOperação cancelada.")
            print("O arquivo existente foi preservado.")
            print("Os arquivos XML também NÃO foram apagados")
            return False

    # Gerando CSV para os arquivos extraídos
    with open(ARQUIVO_SAIDA, mode='w', newline='', encoding='utf-8') as csv_file:
        columns = ['Numero_CTE', 'Chave_NFE']
        writer = csv.DictWriter(csv_file, fieldnames=columns, delimiter=';')

        writer.writeheader()
        for line in data:
            writer.writerow(line)

    print(f"Sucesso! Extração concluída. Total de notas encontradas: {len(data)}")
    print(f"Arquivo salvo como em: {PATH_NAME}")

    return True

# Apagar todos os arquivos da pasta pós extração
def clear_xml_folder():
    for ctes in os.listdir(PASTA_XML):
        file_path = os.path.join(PASTA_XML, ctes)

        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Erro ao excluir {ctes}: {e}')
    
    print('Arquivos XML removidos com sucesso.')

# Execute script
if __name__ == "__main__":
    sucess = extract_data()

    if sucess:
        clear_xml_folder()

