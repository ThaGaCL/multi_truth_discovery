import re

tsvFile = '/home/thilons/Documentos/tcc/Datasets/title.basics.tsv'
csvFile = '/home/thilons/Documentos/tcc/Datasets/title.basics.csv'

with open(tsvFile, "r") as tsv:
    with open(csvFile, "w") as csv:
        for line in tsv:
            fileContent = re.sub(",", ';', line)
            fileContent = re.sub("\t", ",", fileContent)
            csv.write(fileContent)

print("Conversão finalizada")