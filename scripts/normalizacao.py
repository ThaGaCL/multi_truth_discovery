import csv
import unicodedata
import re

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/joined/dataset_full_tmdb_wd.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/normalized/normalized_dataset_full.csv'

def normalizar_texto(texto, is_nome=False):
    """Remove acentos, pontuações indesejadas, espaços extras e padroniza em minúsculas."""
    if texto == '\\N' or not str(texto).strip():
        return '\\N'
    
    # 1. Transliteração (Remove acentos: Émile -> emile)
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    
    # 2. Converte para minúsculas
    texto = texto.lower()
    
    # 3. Limpeza específica
    if is_nome:
        # Filtra IDs crus do Wikidata (ex: q38047964) que não foram traduzidos
        if re.match(r'^q\d+$', texto):
            return '\\N'
        # Remove pontuações dos nomes (ex: J. Searle Dawley -> j searle dawley)
        texto = re.sub(r'[^\w\s]', '', texto)
    
    # 4. Remove espaços duplos e espaços nas pontas
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    return texto if texto else '\\N'

def processar_lista(texto_bruto, is_nome=True):
    """Separa a lista, normaliza cada item, remove duplicatas internas e reagrupa."""
    if texto_bruto == '\\N':
        return '\\N'
        
    itens_limpos = set()
    for item in texto_bruto.split(';'):
        item_norm = normalizar_texto(item.strip(), is_nome)
        if item_norm != '\\N':
            itens_limpos.add(item_norm)
            
    # Se a limpeza removeu tudo (ex: eram só Q-codes), retorna nulo
    if not itens_limpos:
        return '\\N'
        
    # Ordena a lista para manter consistência nas execuções e junta novamente
    return '; '.join(sorted(list(itens_limpos)))

print("Iniciando normalização mantendo a estrutura original do CSV...")

with open(input_file, 'r', encoding='utf-8') as infile, \
     open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    
    reader = csv.DictReader(infile)
    cabecalho = reader.fieldnames
    
    writer = csv.DictWriter(outfile, fieldnames=cabecalho)
    writer.writeheader()
    
    for row in reader:
        nova_linha = {}
        nova_linha['tconst'] = row['tconst']
        
        # --- Normaliza dados do TMDB ---
        nova_linha['tmdb_title'] = normalizar_texto(row['tmdb_title'], is_nome=False)
        nova_linha['tmdb_directors'] = processar_lista(row['tmdb_directors'], is_nome=True)
        nova_linha['tmdb_writers'] = processar_lista(row['tmdb_writers'], is_nome=True)
        
        # --- Normaliza dados do Wikidata ---
        titulo_wd = normalizar_texto(row['wikidata_title'], is_nome=False)
        # Uma verificação extra caso o Wikidata tenha devolvido um Q-code no lugar do título do filme
        if re.match(r'^q\d+$', titulo_wd):
            titulo_wd = '\\N'
        nova_linha['wikidata_title'] = titulo_wd
        
        nova_linha['wikidata_directors'] = processar_lista(row['wikidata_directors'], is_nome=True)
        nova_linha['wikidata_writers'] = processar_lista(row['wikidata_writers'], is_nome=True)
        
        writer.writerow(nova_linha)

print(f"Sucesso! Dataset normalizado salvo em: {output_file}")