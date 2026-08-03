# Junta os datasets, baseado no tconst
import csv
import pandas as pd

tmdb_data = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/tmdb/tmdb_data.csv'
wd_data = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/wikidata/wikidata_data.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/joined/dataset_full_tmdb_wd.csv'

df_omdb = pd.read_csv(tmdb_data)
df_wd = pd.read_csv(wd_data)

df_full = pd.merge(df_omdb, df_wd, on='tconst', how='outer')
df_full.fillna('\\N', inplace=True)

df_full.to_csv(output_file, index=False, encoding='utf-8')
print(f"Datasets mesclados e resultado salvo em: " + output_file)