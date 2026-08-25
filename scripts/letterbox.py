import csv
import requests
from bs4 import BeautifulSoup
import time

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/6kselected.title.crew.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/letterbox/6kletterboxd_data_pt2.csv'

# Máscara para o Letterboxd não bloquear nosso acesso achando que somos um robô malicioso
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("Iniciando Scraping no Letterboxd...")

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(['tconst', 'letterboxd_title', 'letterboxd_directors', 'letterboxd_writers'])
    
    for row in reader:
        tconst = row['tconst']
        url = f"https://letterboxd.com/imdb/{tconst}/"
        
        try:
            # O requests segue o redirecionamento automaticamente
            res = requests.get(url, headers=headers)
            
            if res.status_code != 200:
                writer.writerow([tconst, '\\N', '\\N', '\\N'])
                continue
                
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # Pega o Título
            titulo = '\\N'
            
            titulo_tag = soup.select_one('.headline-1 .name') or soup.find('h1', class_='headline-1')
            if titulo_tag:
                titulo = titulo_tag.text.strip()
            else:
                # Busca a meta tag oculta padrão de redes sociais
                meta_tag = soup.find('meta', property='og:title')
                if meta_tag and meta_tag.get('content'):
                    titulo = meta_tag['content'].split(' (')[0].strip()
            
            # Pega Diretores e Roteiristas buscando pelos links internos do site
            diretores = set()
            roteiristas = set()
            
            for a in soup.find_all('a', href=True):
                if a['href'].startswith('/director/'):
                    diretores.add(a.text.strip())
                elif a['href'].startswith('/writer/') or a['href'].startswith('/screenplay/'):
                    roteiristas.add(a.text.strip())
                    
            dir_str = "; ".join(diretores) if diretores else '\\N'
            rot_str = "; ".join(roteiristas) if roteiristas else '\\N'
            
            writer.writerow([tconst, titulo, dir_str, rot_str])
            print(f"[{tconst}] Coletado: {titulo}")
            
        except Exception as e:
            print(f"[{tconst}] Erro: {e}")
            
        # Pausa de 1 segundo é estritamente necessária para não sofrer bloqueio de IP
        time.sleep(1)