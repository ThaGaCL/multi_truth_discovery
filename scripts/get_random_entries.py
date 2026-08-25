import csv
import random


filename = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/title.crew.csv'
resultFile = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/6kselected.title.crew.csv'
basics_file = '/home/thilons/Documentos/tcc/multi_truth_discovery/Datasets/title.basics.csv'

valid_tconsts = []
with open(basics_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        if row.get('titleType') == 'movie':
            valid_tconsts.append(row['tconst'])

print(f"Tconsts validos {len(valid_tconsts)}")

num_samples = min(6000, len(valid_tconsts))
chosen_tconsts = set(random.sample(valid_tconsts, num_samples))

chosen_rows = []
with open(filename, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        if row['tconst'] in chosen_tconsts:           
            chosen_rows.append([row['tconst'], row['directors'], row['writers']])

with open(resultFile, "w", encoding="utf-8", newline="") as result:
    writer = csv.writer(result)
    writer.writerow(["tconst", "directors", "writers"])
    writer.writerows(chosen_rows)
    

print("Linhas selecionadas e salvas")    
    