import pandas as pd
import re

# Corese execute
import atexit
import subprocess
from time import sleep
from py4j.java_gateway import JavaGateway
from py4j.java_collections import JavaMap

# Start java gateway
java_process = subprocess.Popen(
    ['java', '-jar', '-Dfile.encoding=UTF-8', 'corese-library-python-4.4.0.jar'])
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

if __name__ == '__main__':
    g = load(["th310.ttl", "paragraph.ttl", "annotations.ttl"])
    q = """PREFIX oa:     <http://www.w3.org/ns/oa#>.
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>.
PREFIX schema:  <http://schema.org/> .

select distinct ?paragraph ?content ?concept_generique_label where {
  ?annotation a oa:Annotation;
	oa:hasBody ?concept;
	oa:hasTarget [
		oa:hasSource ?paragraph
	]
  ?paragraph rdf:value ?content.

  ?concept a skos:Concept;
	skos:prefLabel ?concept_label;
	skos:broader+ ?concept_generique.

  ?concept_generique a skos:Concept;
	skos:prefLabel ?concept_generique_label.

  FILTER NOT EXISTS { ?concept_generique skos:broader ?x }
  FILTER (lang(?concept_generique_label) = "en")
}
ORDER BY ?paragraph
"""

    response = sparqlQuery(g, q)
    candidate = list([[x.getValue("?paragraph").toString(), x.getValue("?content").toString(), x.getValue("?concept_generique_label").toString()]
                          for x in response.getMappingList()])
    obj = dict()
    to_csv = []
    for paragraph, content, concept_generique in candidate:
        if paragraph in obj.keys():
            obj[paragraph]["concepts"].append(re.sub("@.*", "", concept_generique).replace('"',""))
        else:
            obj[paragraph] = {"content" : content, "concepts" : [re.sub("@.*", "", concept_generique).replace('"',"")]}
    print(len(obj))
    for row in obj:
        to_csv.append([obj[row]["content"], obj[row]["concepts"]])
    pd.DataFrame(to_csv, columns=["paragraph", "concepts"], ).to_csv("extract_concepts_first_level.csv", index=True, sep=";", line_terminator="\n")


