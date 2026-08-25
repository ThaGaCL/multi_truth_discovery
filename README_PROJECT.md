# Multi-Truth Discovery - Projeto de Pesquisa

Este projeto é uma estrutura de pesquisa sobre descoberta de verdade em cenários de múltiplas fontes de dados.

## 📁 Estrutura do Projeto

O projeto contém três repositórios principais (git submodules/forks):

### 1. 🎬 **Datasets**
Coleção de datasets utilizados na pesquisa:
- `Datasets/` - Dados brutos e processados
  - `imdb/` - Dados do Internet Movie Database
  - `omdb/` - Dados do Open Movie Database
  - `wikidata/` - Dados do Wikidata
  - `joined/` - Dataset final consolidado (`dataset_full.csv`)

### **Truth Discovery Comparative Analysis**
Repositório: https://github.com/LaureBerti/Truth_Discovery_Comparative_Analysis (fork, branch: update)
- Implementação Java dos algoritmos de descoberta de verdade
- Localização: `./Truth_Discovery_Comparative_Analysis/`
- Suporta múltiplos datasets: Weather, Population, Flight, Biography, **Movies** (novo!)

**Como usar:**
```bash
cd Truth_Discovery_Comparative_Analysis

# Compilar projeto
mkdir -p build/classes
javac --release 25 -d build/classes @sources-runtime.txt

# Executar dataset de filmes (novo!)
java -cp build/classes main.MainClass movies

# Ou executar comparação de métricas em todos os datasets
./compare_metrics.sh
```

### 4. 📚 **Scripts**
Utilitários e scripts de processamento:
- `scripts/join_datasets.py` - Consolida dados de múltiplas fontes
- `scripts/omdb_data.py` - Coleta dados OMDB
- `scripts/wd_data.py` - Coleta dados Wikidata

## 🎯 O Dataset de Filmes (NOVO!)

### Objetivo
Testar algoritmos de descoberta de verdade em um cenário realista com:
- Múltiplas fontes (OMDB + Wikidata)
- Dados conflitantes e incompletos
- Múltiplas verdades possíveis

### Características
- **~1000 filmes** com metadados
- **4.599 claims** no total
  - OMDB: 3.456 claims (mais completo)
  - Wikidata: 1.143 claims (cobertura ~33%)
- **Atributos**: título, diretores, roteiristas
- **Ground truth**: 3.456 valores de referência

### Como Usar o Dataset de Filmes
```bash
cd Truth_Discovery_Comparative_Analysis

# Opção 1: Processar o dataset
java -cp build/classes main.MainClass movies

# Opção 2: Adicionar ao compare_metrics.sh e executar todos os datasets
./compare_metrics.sh
```

Ver documentação completa em: [MOVIES_DATASET_README.md](./Truth_Discovery_Comparative_Analysis/MOVIES_DATASET_README.md)

## 📊 Algoritmos Suportados

O Truth Discovery Comparative Analysis implementa os seguintes algoritmos:

- ✅ Voting
- ✅ TruthFinder
- ✅ Cosine Similarity
- ✅ 2-Estimates
- ✅ 3-Estimates
- ✅ Simple LCA
- ✅ Guess LCA
- ✅ AccuCopy (variações T/F)
- ✅ LTM (Latent Truth Model)
- ✅ MLE (Maximum Likelihood Estimation)

## 🚀 Próximos Passos

1. ✅ Dataset de filmes integrado
2. ⏳ Executar algoritmos no novo dataset
3. ⏳ Comparar performance com cenários de verdade única
4. ⏳ Analisar impacto de múltiplas fontes
5. ⏳ Documentar insights e resultados

## 📝 Estrutura de Repositórios Git

```
multi_truth_discovery (origem principal)
├── .git
├── BLIND/
│   └── .git (fork independente)
├── Truth_Discovery_Comparative_Analysis/
│   └── .git (fork independente, branch: update)
├── Datasets/
├── scripts/
└── README_PROJECT.md (este arquivo)
```

## 🔄 Sincronizando com Repositórios Remotos

### Truth Discovery
```bash
cd Truth_Discovery_Comparative_Analysis
git pull origin update
git push origin update
```

### BLIND
```bash
cd BLIND
git pull origin master
git push origin master
```

### Principal (multi_truth_discovery)
```bash
git pull origin main
git push origin main
```

## 📚 Referências

- Truth Discovery Paper: [Arxiv CoRR abs/1409.6428](https://arxiv.org/abs/1409.6428)
- Laure Berti-Équille Research: [Veracity of Data](http://www.morganclaypool.com/doi/abs/10.2200/S00676ED1V01Y201509DTM042)
- OMDB API: http://www.omdbapi.com/
- Wikidata: https://www.wikidata.org/

## 👤 Autor

Integração do dataset de filmes e documentação: 28 de Julho de 2026

---

**Status**: ✅ Pronto para testes e análise
