## Préfix

```SPARQL
prefix oa:     <http://www.w3.org/ns/oa#>.
prefix skos: <http://www.w3.org/2004/02/skos/core#>.
prefix schema:  <http://schema.org/> .
```



## Quels sont les animaux qui construisent un habitat (textes où l’on parle de cette construction)



```SPARQL
SELECT DISTINCT ?paragraph ?name_animal ?mention_animal ?name_construction ?mention_construction WHERE {
  ?annotation1 a oa:Annotation;
              oa:hasBody ?animal;
              oa:hasTarget ?target1.
  ?target1 oa:hasSource ?paragraph;
     	   oa:hasSelector ?selector.
    
  ?selector oa:exact ?mention_animal.

  ?animal a skos:Concept;
       skos:prefLabel ?name_animal;
       skos:broader+ ?animal_generique.
    
  ?animal_generique skos:prefLabel ?name_animal_generique.

  ?annotation2 oa:hasBody ?construction;
        oa:hasTarget ?target2.
  ?target2 oa:hasSource ?p;
      oa:hasSelector ?selector2.
  ?selector2 oa:exact ?mentio_construction.

  ?construction skos:prefLabel ?name_construction;
     skos:broader+ ?construction_generique.
  ?construction_generique skos:prefLabel ?name_construction_generique.

  FILTER (str(?name_animal_generique) = "TERRESTRE").
  FILTER (str(?name_construction_generique) = "house building").
  FILTER (lang(?name_animal) = "en").
  FILTER (lang(?name_construction) = "en")
}
ORDER BY ?paragraph
```



## Quelles anecdotes mettant en relation un homme et un animal (pas toutes les relations hommes/animaux, comme la chasse, etc., mais seulement les situations individuelles, qui seront probablement marquées par un nom propre, ou un nom de lieu, etc.)



## Quels sont les oiseaux qui sont consommés (gastronomie)



## Quels sont les remèdes (thérapeutiques) qui incluent une langue animale (ou un morceau de langue)?



## Quels sont les animaux qui communiquent entre eux (textes où il est question de mode de communication, de langage, etc.)?



## Sur le rythme alimentaire des animaux : quels sont les animaux capables de jeûner, quelles sont les informations sur les rythmes de repas (fréquence)?



## Quelles sont les données transmises sur le temps de gestation des animaux?



## Quelles sont les expérimentations faites sur les animaux (contexte, description…)?



## Quels sont les animaux typiques de l’Afrique (qui ne sont pas considérés comme des variantes d’animaux connus en Europe, telles les moutons (ici d’Afrique), les lions (ici d’Afrique, mais il y en a aussi en Europe et en Asie)



## Quels sont les caractéristiques comportementaux des rongeurs, ou des souris ?



## quelles sont les paires d’animaux (régulièrement associés) qui sont dans un rapport spécial d’affection (sympathie) ou de haine (antipathie)?



## Quels sont les objets techniques réalisés avec des parties animales (peau, os, cornes…)?

