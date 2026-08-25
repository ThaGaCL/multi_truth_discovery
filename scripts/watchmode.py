import csv
import requests
import time

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/selected.title.crew.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/watchmode/watchmode_data.csv'

# Cole sua chave gerada no Watchmode
API_KEY = ''

print("Iniciando coleta na API do Watchmode...")

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(['tconst', 'watchmode_title', 'watchmode_directors', 'watchmode_writers'])
    
    for row in reader:
        tconst = row['tconst']
        url = f"https://api.watchmode.com/v1/title/{tconst}/cast-crew/?apiKey={API_KEY}"
        
        try:
            res = requests.get(url)
            
            if res.status_code != 200:
                writer.writerow([tconst, '\\N', '\\N', '\\N'])
                continue
                
            crew = res.json()
            diretores = set()
            roteiristas = set()
            
            if isinstance(crew, list):
                for membro in crew:
                    cargo = membro.get('type', '').lower()
                    nome = membro.get('full_name', '')
                    
                    if cargo == 'director':
                        diretores.add(nome)
                    elif cargo == 'writer':
                        roteiristas.add(nome)
            
            dir_str = "; ".join(diretores) if diretores else '\\N'
            rot_str = "; ".join(roteiristas) if roteiristas else '\\N'
            
            # título como \N para não gastar requisições duplas da API
            writer.writerow([tconst, '\\N', dir_str, rot_str])
            print(f"[{tconst}] Coletado (Diretores: {len(diretores)} | Roteiristas: {len(roteiristas)})")
            
        except Exception as e:
            print(f"[{tconst}] Erro: {e}")
            
        time.sleep(0.5)