import csv
import requests
import time


input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/selected.title.crew.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/omdb/omdb_data_pt2.csv'

api_key = '3ce6f63'

# --- CONFIGURAÇÃO DO INTERVALO  ---
# (OMdB só aceita 1000 reqs por dia)
# Hoje: start_row = 0, end_row = 1000
# Amanhã: start_row = 999, end_row = 1500
start_row = 999
end_row = 1500

print(f"Iniciando coleta na API do OMDb (Linhas {start_row} a {end_row - 1})...")

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
     
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    writer.writerow(['tconst', 'omdb_title', 'omdb_directors', 'omdb_writers'])
    
    for indice, row in enumerate(reader):
        if indice < start_row:
            continue
            
        # Se o índice atingir o limite, acaba o loop
        if indice >= end_row:
            print("Limite de execuções da rodada atingido.")
            break
            
        tconst = row['tconst']
    
        url = f"http://www.omdbapi.com/?i={tconst}&apikey={api_key}"
        
        try:
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()
            
            # Caso não encontre, coloca \N
            if data.get('Response') == 'False':
                print(f"[{tconst}] Não encontrado no OMDb.")
                writer.writerow([tconst, '\\N', '\\N', '\\N'])
                continue
            
            titulo_omdb = data.get('Title', '\\N')
            diretores = data.get('Director', '\\N')
            roteiristas = data.get('Writer', '\\N')
            
            # Substituir ',' por ';' 
            if diretores != '\\N':
                diretores = diretores.replace(', ', '; ')
            if roteiristas != '\\N':
                roteiristas = roteiristas.replace(', ', '; ')
                
            writer.writerow([tconst, titulo_omdb, diretores, roteiristas])
            print(f"[{indice}] {tconst} Coletado: {titulo_omdb}")
            
        except Exception as e:
             print(f"[{tconst}] Erro na requisição: {e}")
             
        # Pausa pra evitar bloqueio na requisição
        time.sleep(0.3)

print(f"Coleta finalizada! Dados salvos em {output_file}")