import csv

# Dataset do imdb reduzido e convertido para csv
filename = '/home/thilons/Documentos/tcc/Datasets/selected.title.crew.csv'

# Output
resultFile = '/home/thilons/Documentos/tcc/Datasets/translated.title.crew.csv'

# Arquivos de tradução
title_basics_file = '/home/thilons/Documentos/tcc/Datasets/title.basics.csv'
name_basic_file = '/home/thilons/Documentos/tcc/Datasets/name.basics.csv'

# IDs
tconsts_alvos = set()
nconsts_alvos = set()

with open(filename, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        tconsts_alvos.add(row['tconst'])
        
        if row['directors'] != '\\N':
            nconsts_alvos.update(row['directors'].split(';'))
        if row['writers'] != '\\N':
            nconsts_alvos.update(row['writers'].split(';'))
            
print(f"Filmes: {len(tconsts_alvos)} Membros: {len(nconsts_alvos)}")    

# Mapeamento do arquivo de tradução
mapa_titulos = {}
mapa_nomes = {}

with open(title_basics_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        if row['tconst'] in tconsts_alvos:
            mapa_titulos[row['tconst']] = row['primaryTitle']

with open(name_basic_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        if row['nconst'] in nconsts_alvos:
            mapa_nomes[row['nconst']] = row['primaryName']
            
        
# Tradução 
with open(filename, 'r', encoding='utf-8') as infile, open(resultFile, 'w', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    
    writer.writerow(['movie_title', 'directors_names', 'writers_names'])
    
    for row in reader:
        titulo = mapa_titulos.get(row['tconst'], 'Desconhecido')
        
        diretores = []
        if row['directors'] != "\\N":
            for nconst in row['directors'].split(';'):
                nome = mapa_nomes.get(nconst, nconst)
                diretores.append(nome)

        roteiristas = []
        if row['writers'] != "\\N":
            for nconst in row['writers'].split(';'):
                nome = mapa_nomes.get(nconst, nconst)
                roteiristas.append(nome)
                
        writer.writerow([
            titulo,
            "; ".join(diretores) if diretores else "\\N",
            ", ".join(roteiristas) if roteiristas else "\\N"
        ])
        
print(f"Resultado salvo em: {resultFile}")