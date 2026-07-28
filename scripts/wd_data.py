import csv
import requests
import time

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/selected.title.crew.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/omdb/wikidata_data.csv'

# O Endpoint público do Wikidata para executar consultas SPARQL
url_sparql = 'https://query.wikidata.org/sparql'

headers = {
    'User-Agent': 'TCC-TruthDiscovery-Bot/1.0 (thales.gabriel@ufpr.br)',
    'Accept': 'application/sparql-results+json'
}

print("Iniciando coleta na base de grafos do Wikidata...")

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
     
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    writer.writerow(['tconst', 'wikidata_title', 'wikidata_directors', 'wikidata_writers'])
    
    for row in reader:
        tconst = row['tconst']
        
        # Consulta SPARQL: 
        # 1. Busca o item que tem o IMDb ID (P345) correspondente.
        # 2. Pega opcionalmente Diretores (P57) e Roteiristas (P58).
        # 3. Usa o serviço de Labels para trazer os nomes legíveis em Inglês ou Português.
        query = f"""
        SELECT ?itemLabel ?directorLabel ?writerLabel WHERE {{
          ?item wdt:P345 "{tconst}" .
          OPTIONAL {{ ?item wdt:P57 ?director . }}
          OPTIONAL {{ ?item wdt:P58 ?writer . }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en,pt". }}
        }}
        """
        
        try:
            res = requests.get(url_sparql, headers=headers, params={'query': query})
            res.raise_for_status()
            data = res.json()
            
            bindings = data.get('results', {}).get('bindings', [])
            
            if not bindings:
                print(f"[{tconst}] Não encontrado no Wikidata.")
                writer.writerow([tconst, '\\N', '\\N', '\\N'])
                continue
            
            # Como filmes podem ter múltiplos diretores/roteiristas, o Wikidata retorna uma 
            # linha para cada combinação (Produto Cartesiano). Usamos set() para agrupar sem duplicatas.
            titulo = bindings[0].get('itemLabel', {}).get('value', '\\N')
            
            diretores = set()
            roteiristas = set()
            
            for item in bindings:
                if 'directorLabel' in item:
                    # Ignora IDs crus (como Q12345) que o Wikidata retorna quando não acha a tradução do nome
                    if not item['directorLabel']['value'].startswith('http'):
                        diretores.add(item['directorLabel']['value'])
                if 'writerLabel' in item:
                    if not item['writerLabel']['value'].startswith('http'):
                        roteiristas.add(item['writerLabel']['value'])
            
            # Formata para manter o padrão que o seu modelo espera
            dir_str = "; ".join(diretores) if diretores else '\\N'
            rot_str = "; ".join(roteiristas) if roteiristas else '\\N'
            
            writer.writerow([tconst, titulo, dir_str, rot_str])
            print(f"[{tconst}] Coletado: {titulo}")
            
        except requests.exceptions.HTTPError as e:
            # Se der erro 429 (Too Many Requests), o script avisa
            print(f"[{tconst}] Erro HTTP: {e.response.status_code}. Pausando por precaução...")
            time.sleep(5)
        except Exception as e:
            print(f"[{tconst}] Erro inesperado: {e}")
             
        # O Wikidata tolera cerca de 1 a 2 requisições por segundo, mas para 
        # raspar 1500 entidades em sequência, um atraso de 1 segundo é o ideal.
        time.sleep(1)

print(f"Coleta finalizada! Dados salvos em {output_file}")