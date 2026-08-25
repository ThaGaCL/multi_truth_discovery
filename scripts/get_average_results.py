import pandas as pd
import os

input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Truth_Discovery_Comparative_Analysis/DAFNAData/experiments/voterLog/movies_all_algorithms.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Resultados/4s_6k_avg_results_6000.csv'

print(f"Lendo e limpando o arquivo consolidado...\n{input_file}")

# Lista exata dos algoritmos esperados
algoritmos_validos = {
    'Voting', 'TruthFinder', 'TwoEstimates', 'ThreeEstimate', 
    'SimpleLCA', 'GuessLCA', 'AccuCopy_TT', 'AccuCopy_TF', 
    'AccuCopy_FT', 'AccuCopy_FF', 'LTM'
}

dados_limpos = []

# Leitura segura linha por linha para contornar o ParserError
with open(input_file, 'r', encoding='utf-8') as f:
    for linha in f:
        partes = linha.strip().split(',')
        # Se a primeira palavra for um algoritmo válido e a linha tiver as 12 colunas, nós guardamos
        if partes[0] in algoritmos_validos and len(partes) == 12:
            dados_limpos.append(partes)

if not dados_limpos:
    print("Erro: Nenhum dado válido encontrado no arquivo. Verifique o caminho.")
    exit()

# Monta o DataFrame limpo
colunas = ['algorithm', 'tp', 'fp', 'fn', 'tn', 'precision', 'recall', 'accuracy', 'specificity', 'f1', 'iterations', 'duration_ms']
df = pd.DataFrame(dados_limpos, columns=colunas)

# Converte todas as colunas de métricas de string para números float/int
for col in colunas[1:]:
    df[col] = pd.to_numeric(df[col])

print(f"Foram encontradas {len(df)} execuções válidas.")

# Agrupa por algoritmo e tira a média geral
df_medias = df.groupby('algorithm').mean().reset_index()

# Formatação visual científica (Arredonda contagens inteiras e limita as taxas a 4 casas decimais)
df_medias = df_medias.round({
    'tp': 0, 'fp': 0, 'fn': 0, 'tn': 0,
    'precision': 4, 'recall': 4, 'accuracy': 4, 'specificity': 4, 'f1': 4,
    'iterations': 0, 'duration_ms': 0
})

# Salva o resultado
df_medias.to_csv(output_file, index=False)

print(f"\nSucesso! As médias dos 30 runs foram salvas em:\n{output_file}\n")
print("--- RANKING DE F1-SCORE (MÉDIA) ---")
# Mostra no terminal um resumo ordenado do melhor para o pior F1
print(df_medias[['algorithm', 'f1', 'accuracy', 'duration_ms']].sort_values(by='f1', ascending=False).to_string(index=False))