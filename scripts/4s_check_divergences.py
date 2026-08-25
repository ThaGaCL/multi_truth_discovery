import csv
from itertools import combinations

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/normalized/4s_normalized_dataset_full.csv'

# Dicionário para armazenar as estatísticas
stats = {
    'titles': {'exatos': 0, 'conflitos': 0, 'apenas_um': 0, 'vazios': 0},
    'directors': {'exatos': 0, 'parciais': 0, 'conflitos_totais': 0, 'apenas_um': 0, 'vazios': 0},
    'writers': {'exatos': 0, 'parciais': 0, 'conflitos_totais': 0, 'apenas_um': 0, 'vazios': 0}
}

# Lista das fontes presentes no seu CSV
fontes_ativas = ['tmdb', 'wikidata', 'cinemeta', 'letterboxd']

def parse_lista(valor):
    """Converte a string separada por ';' em um set matemático para facilitar a comparação"""
    if valor == '\\N' or not valor.strip():
        return set()
    return set([item.strip() for item in valor.split(';')])

print("Analisando matriz de dados (TMDB vs Wikidata vs Cinemeta vs Letterboxd)...")

total_filmes = 0

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_filmes += 1
        
        # --- ANÁLISE DE TÍTULOS (Single-Truth) ---
        titulos_presentes = []
        for fonte in fontes_ativas:
            t = row[f'{fonte}_title'].strip()
            if t != '\\N' and t != '':
                titulos_presentes.append(t)
        
        if len(titulos_presentes) == 0:
            stats['titles']['vazios'] += 1
        elif len(titulos_presentes) == 1:
            stats['titles']['apenas_um'] += 1
        else:
            # Se o set(lista) tem tamanho 1, significa que todos os itens da lista são idênticos
            if len(set(titulos_presentes)) == 1:
                stats['titles']['exatos'] += 1
            else:
                stats['titles']['conflitos'] += 1
                
        # --- ANÁLISE DE DIRETORES E ROTEIRISTAS (Multi-Truth) --- 
        for role in ['directors', 'writers']:
            sets_presentes = []
            for fonte in fontes_ativas:
                s = parse_lista(row[f'{fonte}_{role}'])
                if s: # Só adiciona à análise as fontes que informaram algum nome
                    sets_presentes.append(s)
            
            if len(sets_presentes) == 0:
                stats[role]['vazios'] += 1
            elif len(sets_presentes) == 1:
                stats[role]['apenas_um'] += 1
            else:
                # Compara se TODOS os sets presentes são exatamente iguais ao primeiro
                if all(s == sets_presentes[0] for s in sets_presentes):
                    stats[role]['exatos'] += 1
                else:
                    # Verifica se existe intersecção entre QUALQUER PAR de fontes
                    # Ex: Se TMDB e Wiki discordam, mas TMDB e Cinemeta tem 1 nome em comum, é parcial.
                    tem_interseccao = False
                    for s1, s2 in combinations(sets_presentes, 2):
                        if s1.intersection(s2):
                            tem_interseccao = True
                            break
                    
                    if tem_interseccao:
                        stats[role]['parciais'] += 1
                    else:
                        stats[role]['conflitos_totais'] += 1

# --- IMPRESSÃO DOS RESULTADOS ---
print(f"\nTotal de Filmes Analisados: {total_filmes}")
print("="*60)

print("\nTÍTULOS (Atributo de Verdade Única)")
print(f"Concordância Exata: {stats['titles']['exatos']}")
print(f"Divergência / Conflito: {stats['titles']['conflitos']}")
print(f"Informação em apenas 1 fonte: {stats['titles']['apenas_um']}")
print(f"Nenhuma fonte informou: {stats['titles']['vazios']}")

# Calculo de divergência para Títulos
opinaram_titulos = stats['titles']['exatos'] + stats['titles']['conflitos']
if opinaram_titulos > 0:
    taxa_div_titulos = (stats['titles']['conflitos'] / opinaram_titulos) * 100
    print(f"-> Quando múltiplas fontes opinam, divergem em {taxa_div_titulos:.1f}% das vezes.")

for role in ['directors', 'writers']:
    s = stats[role]
    nome_exibicao = "DIRETORES" if role == 'directors' else "ROTEIRISTAS"
    print(f"\n--- {nome_exibicao} (Atributo de Múltiplas Verdades) ---")
    print(f"Concordância Exata (Listas 100% idênticas): {s['exatos']}")
    print(f"Divergência Parcial (Concordam em alguns nomes): {s['parciais']}")
    print(f"Divergência Total (Nomes completamente diferentes): {s['conflitos_totais']}")
    print(f"Informação em apenas 1 fonte: {s['apenas_um']}")
    print(f"Nenhuma fonte informou: {s['vazios']}")
    
    # Cálculo para a tese: A taxa de divergência quando MÚLTIPLAS fontes opinam
    opinaram_multi = s['exatos'] + s['parciais'] + s['conflitos_totais']
    if opinaram_multi > 0:
        taxa_divergencia = ((s['parciais'] + s['conflitos_totais']) / opinaram_multi) * 100
        print(f"-> Quando múltiplas fontes opinam, divergem em {taxa_divergencia:.1f}% das vezes.")

print("\n" + "="*60)