package scripts.bayesian_mtd;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.List;

public class IterativeBayesianMTD {
    
    // iterative_multi_truth_finding(O, C, G, mappings)    
    // Algoritmo: Iterative Multi-Truth-Finding[cite: 1]
    
    // Entradas:
    //   O: Conjunto de itens de dados[cite: 1].
    //   C: Conjunto de grupos de valores {C_n | o_n in O}[cite: 1].
    //   G: Conjunto de grupos de fontes[cite: 1].
    //   mappings: Mapeamentos G_n(c) e C_n(g)[cite: 1].
      
    // Saída:
    //   Conjunto de grupos de valores verdadeiros: {c | sigma(c) >= 0.5}[cite: 1].

    class Item {String id; List<ValueGroup> valueGroups;}
    class ValueGroup {String id; List<SourceGroup> sourceGroups;}
    class SourceGroup {String id; List<Source> sources;}
    class Source {String id;}

    class Precision {double positive; double negative;}
}
