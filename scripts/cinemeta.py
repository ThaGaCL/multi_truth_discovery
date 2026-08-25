import csv
import requests
import time

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/6kselected.title.crew.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/cinemeta/6kcinemeta_data.csv'

print("Iniciando coleta na API pública do Cinemeta com sistema anti-travamento...")

headers = {'User-Agent': 'TCC-Research-Script/1.0 (Academic Research)'}

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(['tconst', 'cinemeta_title', 'cinemeta_directors', 'cinemeta_writers'])
    
    for row in reader:
        tconst = row['tconst']
        url = f"https://v3-cinemeta.strem.io/meta/movie/{tconst}.json"
        
        # Sistema de retentativas
        max_tentativas = 3
        sucesso = False
        
        for tentativa in range(max_tentativas):
            try:
                # O TIMEOUT de 5 segundos é o que impede o código de congelar!
                res = requests.get(url, headers=headers, timeout=5)
                
                # Se a API nos der um Rate Limit (429), pausamos e tentamos de novo
                if res.status_code == 429:
                    print(f"[{tconst}] Rate limit atingido. Pausando por {2 ** tentativa}s...")
                    time.sleep(2 ** tentativa)  # Espera exponencial: 1s, 2s, 4s...
                    continue
                
                if res.status_code != 200:
                    writer.writerow([tconst, '\\N', '\\N', '\\N'])
                    sucesso = True
                    break
                    
                data = res.json()
                meta = data.get('meta') or {}
                
                titulo = meta.get('name') or '\\N'
                diretores = meta.get('director') or []
                roteiristas = meta.get('writer') or []
                
                dir_str = "; ".join(diretores) if diretores else '\\N'
                rot_str = "; ".join(roteiristas) if roteiristas else '\\N'
                
                writer.writerow([tconst, titulo, dir_str, rot_str])
                print(f"[{tconst}] Coletado: {titulo} (Dir: {len(diretores)} | Rot: {len(roteiristas)})")
                
                sucesso = True
                break # Sai do loop de tentativas se deu certo
                
            except requests.exceptions.Timeout:
                print(f"[{tconst}] Timeout na tentativa {tentativa + 1}. O servidor demorou demais.")
                time.sleep(1) # Pausa rápida antes de tentar de novo
            except requests.exceptions.RequestException as e:
                print(f"[{tconst}] Erro de conexão na tentativa {tentativa + 1}: {e}")
                time.sleep(1)
                
        # Se depois de 3 tentativas ele ainda falhar, escreve nulo e segue a vida
        if not sucesso:
            print(f"[{tconst}] Falhou definitivamente após {max_tentativas} tentativas. Pulando.")
            writer.writerow([tconst, '\\N', '\\N', '\\N'])
            
        # Aumentei o sleep base para 0.5s para aliviar a carga no servidor deles
        time.sleep(0.5)

print(f"\nColeta finalizada! Dados salvos em: {output_file}")