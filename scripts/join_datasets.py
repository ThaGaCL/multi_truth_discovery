# Junta os datasets, baseado no tconst
import csv
import pandas as pd

tmdb_data = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/tmdb/6ktmdb_data.csv'
wd_data = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/wikidata/6kwikidata_data.csv'
cinemeta_data = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/cinemeta/6kcinemeta_data.csv'
letterbox_data = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/letterbox/6kletterboxd_data_pt2.csv'
output_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/joined/6k_dataset_full_tmdb_wd_cm_leb.csv'

df_omdb = pd.read_csv(tmdb_data)
df_wd = pd.read_csv(wd_data)
df_cm = pd.read_csv(cinemeta_data)
df_lb = pd.read_csv(letterbox_data)

df_full = pd.merge(df_omdb, df_wd, on='tconst', how='outer')
df_full = pd.merge(df_full, df_cm, on='tconst', how='outer')
df_full = pd.merge(df_full, df_lb, on='tconst', how='outer')


df_full.fillna('\\N', inplace=True)

df_full.to_csv(output_file, index=False, encoding='utf-8')
print(f"Datasets mesclados e resultado salvo em: " + output_file)