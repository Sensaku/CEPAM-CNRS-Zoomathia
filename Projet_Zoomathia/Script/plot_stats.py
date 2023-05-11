import matplotlib.pyplot as plt

# Corese execute
import atexit
import subprocess
from time import sleep
from py4j.java_gateway import JavaGateway
from py4j.java_collections import JavaMap
import pandas as pd


# Start java gateway
java_process = subprocess.Popen(
    ['java', '-jar', '-Dfile.encoding=UTF-8', 'corese-library-python-4.3.0.jar'])
sleep(1)
gateway = JavaGateway()

# Stop java gateway at the enf od script
def exit_handler():
    gateway.shutdown()
    print('\n' * 2)
    print('Gateway Server Stop!')

atexit.register(exit_handler)

# Import of class
Graph = gateway.jvm.fr.inria.corese.core.Graph
Load = gateway.jvm.fr.inria.corese.core.load.Load
Transformer = gateway.jvm.fr.inria.corese.core.transform.Transformer
QueryProcess = gateway.jvm.fr.inria.corese.core.query.QueryProcess
CoreseModel = gateway.jvm.fr.inria.corese.rdf4j.CoreseModel
SimpleValueFactory = gateway.jvm.org.eclipse.rdf4j.model.impl.SimpleValueFactory
RDF = gateway.jvm.org.eclipse.rdf4j.model.vocabulary.RDF


def sparqlQuery(graph, query):
    """Run a query on a graph

    :param graph: the graph on which the query is executed
    :param query: query to run
    :returns: query result
    """
    exec = QueryProcess.create(graph)
    return exec.query(query)


def load(path):
    """Load a graph from a local file or a URL

    :param path: local path or a URL
    :returns: the graph load
    """
    graph = Graph()

    ld = Load.create(graph)
    for x in path:
        ld.parse(x)

    return graph

def get_most_concepts():
    req = """
prefix oa:     <http://www.w3.org/ns/oa#>.
prefix skos: <http://www.w3.org/2004/02/skos/core#>.

select ?x ?label (count(?annotation) as ?nb) where {
  ?annotation a oa:Annotation;
	oa:hasBody ?x.
  ?x a skos:Concept;
	skos:prefLabel ?label.
  filter (lang(?label) = "en")
}
GROUP BY ?label
ORDER BY DESC (?nb)
LIMIT 10
    """

    query_result = sparqlQuery(g, req)
    label_list = [x.getValue('?label').toString() for x in query_result.getMappingList()]
    value_list = [int(x.getValue('?nb').toString()) for x in query_result.getMappingList()]
    return label_list, value_list

def get_most_general_concept():
    req = """
    prefix oa:     <http://www.w3.org/ns/oa#>.
prefix skos: <http://www.w3.org/2004/02/skos/core#>.

select distinct ?y ?ll  (count(?annotation) as ?nb) where {
  ?annotation a oa:Annotation;
	oa:hasBody ?x.

  ?x a skos:Concept;
	skos:prefLabel ?label;
	skos:broader+ ?y.

  ?y a skos:Concept;
	skos:prefLabel ?ll.
  filter not exists {?y skos:broader ?z}
  filter (lang(?label) = "en")
  filter (lang(?ll) = "en")
}
GROUP BY (?ll)
ORDER BY DESC (?nb)
LIMIT 10
    """
    query_result = sparqlQuery(g, req)
    label_list = [x.getValue('?ll').toString() for x in query_result.getMappingList()]
    value_list = [int(x.getValue('?nb').toString()) for x in query_result.getMappingList()]
    return label_list, value_list

def get_concept_not_found():
    req = """
prefix oa:     <http://www.w3.org/ns/oa#>.
prefix skos: <http://www.w3.org/2004/02/skos/core#>.

select ?label (count(?x) as ?nb) where {
  ?x a skos:Concept;
	skos:prefLabel ?label.
}
GROUP BY ?label
ORDER BY DESC (?nb)
LIMIT 10
        """
    query_result = sparqlQuery(g, req)
    label_list = [x.getValue('?label').toString() for x in query_result.getMappingList()]
    value_list = [int(x.getValue('?nb').toString()) for x in query_result.getMappingList()]
    return label_list, value_list

def get_QC1():
    req = """
    prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
    prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> 
    prefix oa:     <http://www.w3.org/ns/oa#>
    prefix skos: <http://www.w3.org/2004/02/skos/core#>
    prefix schema:  <http://schema.org/>
    prefix paragraph: <http://www.zoomathia.com/>

    SELECT DISTINCT ?paragraph ?name_animal ?name_construction WHERE {
      ?annotation1 a oa:Annotation;
                  oa:hasBody ?animal;
                  oa:hasTarget ?target1.
      ?target1 oa:hasSource ?paragraph;
         oa:hasSelector ?selector.

      ?selector oa:exact ?mention_animal.

      ?animal a skos:Concept;
           skos:prefLabel ?name_animal.

      ?animal_collection a skos:Collection;
           skos:prefLabel "Ancient class"@en;
           skos:member ?animal.

      ?annotation2 oa:hasBody ?construction;
            oa:hasTarget ?target2.
      ?target2 oa:hasSource ?paragraph;
          oa:hasSelector ?selector2.
      ?selector2 oa:exact ?mention_construction.

      ?construction skos:prefLabel ?name_construction;
                        skos:broader+ ?construction_generique.
      ?construction_generique skos:prefLabel "house building"@en.

      FILTER (lang(?name_animal) = "en").
      FILTER (lang(?name_construction) = "en")
      FILTER not exists {?animal skos:narrower ?y}
    }
    ORDER BY ?paragraph
    """

    query_result = sparqlQuery(g, req)
    pd.DataFrame([
        [
            x.getValue("?paragraph").toString(),
            x.getValue("?name_animal").toString(),
            x.getValue("?name_construction").toString()
         ] for x in query_result.getMappingList()
    ], columns=["paragraph", "animal", "construction"]).to_csv("qc1.csv", index=False, encoding="utf-8", sep=";", lineterminator="\n")
    return

if __name__ == '__main__':

    label = ["generated", "to_check", "ambigue", "numeric", "incomplete", "no_concept"]
    value = [8188, 128, 109, 7, 1052, 1549]
    plt.bar(label, value)
    plt.tight_layout()
    plt.savefig('stats/stats_generation2.png')

    """files = ["annotations.ttl", "paragraph.ttl", "th310.ttl"]
    g = load(files)

    get_QC1()
    x, y = get_most_concepts()

    plt.barh(x, y)
    plt.ylabel("concept")
    plt.xlabel("occurrences")
    plt.tight_layout()
    plt.savefig('stats/occurrences.png')

    x2, y2 = get_most_general_concept()
    plt.barh(x2, y2)
    plt.xlabel("occurrence")
    plt.tight_layout()
    plt.savefig('combine.png')
    plt.close()

    x2, y2 = get_most_general_concept()
    plt.barh(x2, y2)
    plt.ylabel("concept_générique")
    plt.xlabel("occurrences")
    plt.tight_layout()
    plt.savefig('stats/generals.png')
    plt.close()

    x, y = ["Annotation", "concept distinct"], [11073, 1482]
    plt.bar(x,y)
    plt.tight_layout()
    plt.savefig("stats/global.png")
    plt.close()

    files = ["no_concept.ttl"]
    g = load(files)

    x, y = get_concept_not_found()
    plt.barh(x, y)
    plt.tight_layout()
    plt.savefig("stats/not_found.png")
    plt.close()

    files = ["overloaded.ttl"]
    g = load(files)

    x, y = get_concept_not_found()
    plt.barh(x, y)
    plt.tight_layout()
    plt.savefig("stats/overloaded.png")
    plt.close()

"""