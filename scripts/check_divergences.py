import csv

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/normalized/4s_6k_normalized_dataset_full.csv'

# Dicionário para armazenar as estatísticas
stats = {
    'titles': {'exatos': 0, 'conflitos': 0, 'apenas_um': 0, 'vazios': 0},
    'directors': {'exatos': 0, 'parciais': 0, 'conflitos_totais': 0, 'apenas_um': 0, 'vazios': 0},
    'writers': {'exatos': 0, 'parciais': 0, 'conflitos_totais': 0, 'apenas_um': 0, 'vazios': 0}
}

def parse_lista(valor):
    """Converte a string separada por ';' em um set matemático para facilitar a comparação"""
    if valor == '\\N' or not valor.strip():
        return set()
    return set([item.strip() for item in valor.split(';')])

print("Analisando matriz de dados TMDB vs Wikidata...")

total_filmes = 0

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_filmes += 1
        
        # ANÁLISE DE TÍTULOS (Single-Truth)
        t_tmdb = row['tmdb_title'].strip()
        t_wd = row['wikidata_title'].strip()
        
        if t_tmdb == '\\N' and t_wd == '\\N':
            stats['titles']['vazios'] += 1
        elif t_tmdb == '\\N' or t_wd == '\\N':
            stats['titles']['apenas_um'] += 1
        elif t_tmdb == t_wd:
            stats['titles']['exatos'] += 1
        else:
            stats['titles']['conflitos'] += 1
            
        # ANÁLISE DE DIRETORES E ROTEIRISTAS (Multi-Truth) 
        for role in ['directors', 'writers']:
            # Pega as colunas montando o nome dinamicamente
            set_tmdb = parse_lista(row[f'tmdb_{role}'])
            set_wd = parse_lista(row[f'wikidata_{role}'])
            
            if not set_tmdb and not set_wd:
                stats[role]['vazios'] += 1
            elif not set_tmdb or not set_wd:
                stats[role]['apenas_um'] += 1
            elif set_tmdb == set_wd:
                stats[role]['exatos'] += 1
            elif set_tmdb.intersection(set_wd):
                # Há intersecção, mas os sets não são 100% iguais (Concordância Parcial)
                stats[role]['parciais'] += 1
            else:
                # Intersecção vazia (Conflito Total: fontes dizem nomes completamente diferentes)
                stats[role]['conflitos_totais'] += 1

# IMPRESSÃO DOS RESULTADOS
print(f"\nTotal de Filmes Analisados: {total_filmes}")
print("="*50)

print("\nTÍTULOS (Atributo de Verdade Única)")
print(f"Concordância Exata: {stats['titles']['exatos']}")
print(f"Divergência / Conflito: {stats['titles']['conflitos']}")
print(f"Informação em apenas 1 fonte: {stats['titles']['apenas_um']}")
print(f"Nenhuma fonte informou: {stats['titles']['vazios']}")

for role in ['directors', 'writers']:
    s = stats[role]
    nome_exibicao = "DIRETORES" if role == 'directors' else "ROTEIRISTAS"
    print(f"\n--- {nome_exibicao} (Atributo de Múltiplas Verdades) ---")
    print(f"Concordância Exata (Sets 100% iguais): {s['exatos']}")
    print(f"Divergência Parcial (Concordam em alguns, discordam em outros): {s['parciais']}")
    print(f"Divergência Total (Nomes completamente diferentes): {s['conflitos_totais']}")
    print(f"Informação em apenas 1 fonte: {s['apenas_um']}")
    print(f"Nenhuma fonte informou: {s['vazios']}")
    
    # Cálculo para a tese: A taxa de divergência quando AMBAS as fontes opinam
    ambas_opinaram = s['exatos'] + s['parciais'] + s['conflitos_totais']
    if ambas_opinaram > 0:
        taxa_divergencia = ((s['parciais'] + s['conflitos_totais']) / ambas_opinaram) * 100
        print(f"-> Quando ambas as fontes opinam, divergem em {taxa_divergencia:.1f}% das vezes.")

print("\n" + "="*50)