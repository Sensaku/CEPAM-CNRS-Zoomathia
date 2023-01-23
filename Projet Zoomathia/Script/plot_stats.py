import matplotlib.pyplot as plt

# Corese execute
import atexit
import subprocess
from time import sleep
from py4j.java_gateway import JavaGateway
from py4j.java_collections import JavaMap


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


if __name__ == '__main__':

    files = ["annotations.ttl", "th310.ttl"]
    g = load(files)
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

    x, y = ["Annotation", "concept distinct"], [24442, 3083]
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

