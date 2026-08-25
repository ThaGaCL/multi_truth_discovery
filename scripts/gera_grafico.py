import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# --- CONFIGURAÇÕES DE DIRETÓRIO E ARQUIVO ---
# Aponte para o arquivo CSV gerado pelo seu script de médias
input_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Resultados/4s_avg_results_1500.csv'
output_dir = 'graficos_tcc'

# Configuração de estilo para publicações científicas
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.titlesize': 14,
    'font.family': 'sans-serif',
})

print(f"Lendo dados do arquivo: {input_file}")

if not os.path.exists(input_file):
    print("Erro: O arquivo especificado não foi encontrado!")
    exit(1)

# Carrega os dados diretamente do CSV
df = pd.read_csv(input_file)
os.makedirs(output_dir, exist_ok=True)

# -------------------------------------------------------------
# FIGURA 1: Comparativo Multi-Métricas (F1, Precision, Recall)
# -------------------------------------------------------------
df_sorted_f1 = df.sort_values(by='f1', ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(df_sorted_f1))
bar_width = 0.25

rects1 = ax.barh(
    y_pos + bar_width,
    df_sorted_f1['f1'],
    bar_width,
    label='F1-Score',
    color='#1f77b4',
)
rects2 = ax.barh(
    y_pos,
    df_sorted_f1['precision'],
    bar_width,
    label='Precisão',
    color='#2ca02c',
)
rects3 = ax.barh(
    y_pos - bar_width,
    df_sorted_f1['recall'],
    bar_width,
    label='Revocação (Recall)',
    color='#ff7f0e',
)

ax.set_yticks(y_pos)
ax.set_yticklabels(df_sorted_f1['algorithm'])
ax.set_xlabel('Score')
ax.set_title('Comparativo de Desempenho entre Algoritmos de Truth Discovery')
ax.set_xlim(0, 1.05)
ax.legend(loc='lower right', frameon=True)

# Adiciona valor numérico na barra de F1-Score
for rect in rects1:
  w = rect.get_width()
  ax.annotate(
      f'{w:.3f}',
      xy=(w, rect.get_y() + rect.get_height() / 2),
      xytext=(4, 0),
      textcoords='offset points',
      ha='left',
      va='center',
      fontsize=8,
  )

plt.tight_layout()
plt.savefig(f'{output_dir}/fig1_metricas_comparativas.png', dpi=300, bbox_inches='tight')
plt.savefig(f'{output_dir}/fig1_metricas_comparativas.pdf', bbox_inches='tight')  # PDF vetorial para LaTeX
plt.close()

# -------------------------------------------------------------
# FIGURA 2: Custo Computacional (Duração em ms) vs. F1-Score
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5.5))

scatter = sns.scatterplot(
    data=df,
    x='duration_ms',
    y='f1',
    size='iterations',
    sizes=(80, 400),
    hue='f1',
    palette='viridis',
    legend=False,
    ax=ax,
)

# Adiciona rótulos textuais para cada algoritmo com leve offset
for _, row in df.iterrows():
  offset_x = 5
  offset_y = 0.015 if row['algorithm'] != 'LTM' else -0.03
  ax.annotate(
      row['algorithm'],
      (row['duration_ms'], row['f1']),
      xytext=(row['duration_ms'] + offset_x, row['f1'] + offset_y),
      fontsize=9,
      weight='bold' if row['algorithm'] in ['Voting', 'LTM', 'ThreeEstimate'] else 'normal',
  )

ax.set_xlabel('Tempo Médio de Execução (ms)')
ax.set_ylabel('F1-Score')
ax.set_title('Eficiência Computacional vs. Qualidade da Descoberta da Verdade')
ax.set_ylim(0, 0.9)
ax.axhline(0.7, color='grey', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig(f'{output_dir}/fig2_tempo_vs_f1score.png', dpi=300, bbox_inches='tight')
plt.savefig(f'{output_dir}/fig2_tempo_vs_f1score.pdf', bbox_inches='tight')
plt.close()

# -------------------------------------------------------------
# FIGURA 3: Decomposição da Matriz de Confusão (TP, FP, FN, TN)
# -------------------------------------------------------------
df_cm = df.set_index('algorithm')[['tp', 'fp', 'fn', 'tn']]
# Normalizar para percentual (100%) para facilitar comparação estrutural
df_cm_pct = df_cm.div(df_cm.sum(axis=1), axis=0) * 100
df_cm_pct = df_cm_pct.loc[df.sort_values(by='f1', ascending=False)['algorithm']]

colors = ['#2ca02c', '#d62728', '#ff7f0e', '#1f77b4']  # TP, FP, FN, TN
fig, ax = plt.subplots(figsize=(10, 5.5))

df_cm_pct.plot(
    kind='barh',
    stacked=True,
    color=colors,
    ax=ax,
    edgecolor='black',
    linewidth=0.5,
)

ax.set_xlabel('Proporção das Predições (%)')
ax.set_title('Composição da Matriz de Confusão Normalizada por Algoritmo (100%)')
ax.set_xlim(0, 100)
ax.legend(
    ['True Positives (TP)', 'False Positives (FP)', 'False Negatives (FN)', 'True Negatives (TN)'],
    loc='upper center',
    bbox_to_anchor=(0.5, -0.15),
    ncol=4,
    frameon=True,
)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig(f'{output_dir}/fig3_matriz_confusao_stacked.png', dpi=300, bbox_inches='tight')
plt.savefig(f'{output_dir}/fig3_matriz_confusao_stacked.pdf', bbox_inches='tight')
plt.close()

print(f"Gráficos gerados com sucesso na pasta: '{os.path.abspath(output_dir)}'")