import csv
import requests
import time

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/selected.title.crew.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/dbpedia/dbpedia_data.csv'

# Endpoint oficial de consultas SPARQL do DBpedia
url_sparql = 'https://dbpedia.org/sparql'

print("Iniciando coleta na base de grafos do DBpedia...")

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
     
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    writer.writerow(['tconst', 'dbpedia_title', 'dbpedia_directors', 'dbpedia_writers'])
    
    for row in reader:
        tconst = row['tconst']
        # O DBpedia às vezes armazena o ID com e sem o prefixo 'tt'
        tconst_numero = tconst.replace('tt', '')
        
        # Consulta SPARQL focada em extrair rótulos limpos em inglês
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?title ?directorName ?writerName WHERE {{
          {{ ?movie dbo:imdbId "{tconst}" }} UNION {{ ?movie dbo:imdbId "{tconst_numero}" }} .
          OPTIONAL {{ ?movie rdfs:label ?title . FILTER (lang(?title) = 'en') }}
          OPTIONAL {{
            ?movie dbo:director ?director .
            ?director rdfs:label ?directorName .
            FILTER (lang(?directorName) = 'en')
          }}
          OPTIONAL {{
            ?movie dbo:writer ?writer .
            ?writer rdfs:label ?writerName .
            FILTER (lang(?writerName) = 'en')
          }}
        }}
        """
        
        try:
            # O DBpedia prefere receber as queries via GET com formatação JSON
            res = requests.get(url_sparql, params={'query': query, 'format': 'json'})
            res.raise_for_status()
            data = res.json()
            
            bindings = data.get('results', {}).get('bindings', [])
            
            if not bindings:
                print(f"[{tconst}] Não encontrado no DBpedia.")
                writer.writerow([tconst, '\\N', '\\N', '\\N'])
                continue
            
            titulo = bindings[0].get('title', {}).get('value', '\\N')
            
            diretores = set()
            roteiristas = set()
            
            # Agrupa os resultados do Produto Cartesiano gerado pelo SPARQL
            for item in bindings:
                if 'directorName' in item:
                    diretores.add(item['directorName']['value'])
                if 'writerName' in item:
                    roteiristas.add(item['writerName']['value'])
            
            dir_str = "; ".join(diretores) if diretores else '\\N'
            rot_str = "; ".join(roteiristas) if roteiristas else '\\N'
            
            writer.writerow([tconst, titulo, dir_str, rot_str])
            print(f"[{tconst}] Coletado: {titulo}")
            
        except requests.exceptions.HTTPError as e:
            print(f"[{tconst}] Erro HTTP: {e.response.status_code}")
        except Exception as e:
            print(f"[{tconst}] Erro inesperado: {e}")
             
        # Pausa leve para respeitar os limites do servidor acadêmico
        time.sleep(1)

print(f"Coleta finalizada! Dados salvos em {output_file}")