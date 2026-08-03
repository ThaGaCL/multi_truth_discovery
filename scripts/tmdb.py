import csv
import requests
import time

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/selected.title.crew.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/tmdb/tmdb_data.csv'

# Cole a sua chave gerada no site do TMDB aqui
api_key = '3930dd0a1ccf2aa5be8e5a6f38076b99'

print("Iniciando coleta na API do TMDB...")

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
     
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    # Cabeçalho padronizado para o Join posterior
    writer.writerow(['tconst', 'tmdb_title', 'tmdb_directors', 'tmdb_writers'])
    
    for indice, row in enumerate(reader):
        tconst = row['tconst']
        
        # A API do TMDB permite buscar diretamente pelo ID do IMDb
        url = f"https://api.themoviedb.org/3/movie/{tconst}?api_key={api_key}&append_to_response=credits"
        
        try:
            res = requests.get(url)
            
            # Se a API retornar 404, o filme não existe no banco deles
            if res.status_code == 404:
                print(f"[{indice}] {tconst} Não encontrado no TMDB.")
                writer.writerow([tconst, '\\N', '\\N', '\\N'])
                continue
                
            res.raise_for_status()
            data = res.json()
            
            # Coleta do título
            titulo_tmdb = data.get('title', '\\N')
            
            # Navegação no objeto JSON para pegar a equipe (Crew)
            crew = data.get('credits', {}).get('crew', [])
            
            # Filtro para Diretores
            diretores = [membro['name'] for membro in crew if membro.get('job') == 'Director']
            
            # Filtro para Roteiristas (Englobando as principais categorias de roteiro do TMDB)
            cargos_roteiro = ['Screenplay', 'Writer', 'Story', 'Author']
            roteiristas = [membro['name'] for membro in crew if membro.get('job') in cargos_roteiro]
            
            # Formatando com ponto e vírgula para manter a compatibilidade
            dir_str = "; ".join(diretores) if diretores else '\\N'
            rot_str = "; ".join(roteiristas) if roteiristas else '\\N'
            
            writer.writerow([tconst, titulo_tmdb, dir_str, rot_str])
            print(f"[{indice}] {tconst} Coletado: {titulo_tmdb}")
            
        except requests.exceptions.RequestException as e:
            print(f"[{indice}] {tconst} Erro de rede: {e}")
        except Exception as e:
            print(f"[{indice}] {tconst} Erro inesperado: {e}")
             
        # O TMDB permite 40 requisições a cada 10 segundos. 
        # A pausa de 0.3s mantém você numa margem 100% segura (aprox. 33 req/10s).
        time.sleep(0.3)

print(f"\nColeta finalizada! Matriz salva em: {output_file}")