import pandas as pd

base_dir = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/omdb'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/omdb/6komdb_data_full.csv'

dataframes = []

print("Iniciando a leitura dos arquivos...")

for i in range(1, 8):
    file_name = f"{base_dir}/6komdb_data_pt{i}.csv"
    try:
        df_temp = pd.read_csv(file_name)
        dataframes.append(df_temp)
        print(f"Carregado: 6komdb_data_pt{i}.csv com {len(df_temp)} linhas.")
    except FileNotFoundError:
        print(f"Aviso: O arquivo {file_name} não foi encontrado e será ignorado.")

df_full = pd.concat(dataframes, ignore_index=True)

df_full.drop_duplicates(subset=['tconst'], inplace=True)

df_full.fillna('\\N', inplace=True)

df_full.to_csv(output_file, index=False, encoding='utf-8')

print(f"\nSucesso! Dataset unificado contendo {len(df_full)} linhas salvo em: {output_file}")