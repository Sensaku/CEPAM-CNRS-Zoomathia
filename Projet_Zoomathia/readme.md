# Projet Zoomathia

https://www.cepam.cnrs.fr/sites/zoomathia/

## Equipe

Arnaud Zucker - CEPAM

Catherine Faron - I3S

Marco Corneli - CEPAM

Arnaud Barbe - CEPAM



## Objectifs



## Librairies

- RDFLib (lecture de fichier ttl)
- Regex
- unicodedata
- numpy
- pandas
- win32com.client (lecture de fichier word via l'application) only windows OS
- os

## Compte rendu réunion

https://docs.google.com/document/d/1vUZy89HA21L_kX7yifo4Y6ACTZnMEeReS7QDjQ_WIEI/edit?usp=sharing

## Schémas

- Global: https://drive.google.com/file/d/1X1MbAntXFNkopRAnX6HvInL3KrCTsGiI/view?usp=sharing
- 



## Ontologies

- Annotation Ontology (OA) : https://www.w3.org/ns/oa

## Thesaurus

Opentheso: https://opentheso.huma-num.fr/opentheso/index.xhtml

Documentation Opentheso : https://opentheso.hypotheses.org/





# TER - Machine learning for automatic semantic classification of ancient zoological texts

Title: Machine learning for automatic semantic classification of ancient zoological texts

Description:

This research project is inscribed in the framework of the international research network Zoomathia (http://www.cepam.cnrs.fr/zoomathia). Zoomathia primarily focuses on the transmission of zoological knowledge from Antiquity to the Middle Ages through textual resources, and considers compilation literature such as encyclopaedias. In more detail, parts of the encyclopaedias (or of other texts) are manually annotated by archeozoologists and linguists with the aim of extracting zoological topics that support the evaluation and interpretation of the development of a zoological knowledge through the ages. The zoological topics are collected in a devoted thesaurus THEZOO (https://opentheso.huma-num.fr/opentheso/?idt=th310} gathering all the zoology-related concepts encountered in books VIII-XI of Pliny the Elder's Naturalis Historia (1st century).

The aim of this project is to automate the semantic annotation of the paragraphs of Pliny the Elder's Naturalis Historia (English version). The problem can be formulated as a supervised classification task, where an observation (a text paragraph) must be labelled with one or more general-concepts from THEZOO. Part of the annotated portion of the encyclopaedia will act as the training dataset, the remaining part as validation/test dataset. The project will be articulated in two steps:

- Data mining and NLP. The student will first parse the .xml annotated file in order to import the text as well as the annotations/labels
  and perform some pre-processing (lowercase conversion, tokenization, punctuation and stop-words removal, etc.). 
  The tokens will then be embedded via RoBERT (Liu et al., 2019). Some fine-tuning on Naturalis Historia might be done.

 - Machine learning. The student will define the machine learning routine that will perform the automatic annotation/classification
 of the paragraph. Problems to attack: 
 1) can the problem be cast as a multiclass (soft) classification task, with as many classes as concepts? Or would it be wiser to separately train as many binary classifiers as the number of concepts, as done in (Faron et al., 2016) ? 
 2) How to combine the word-vectors in a way to obtain an input for a classifier? One possible approach is to see the word-vectors of each paragraph as the support of a probability distribution. The mass at each point would be proportional to the cosine similarity between the word-vector and a label/concept. Thus the Wasserstein distance could be employed to measure the distance between two paragraphs (Kusner et al., 2015) and every distance-based classifier (e.g. KNN or SVM) could be trained and tested on the annotated corpus.