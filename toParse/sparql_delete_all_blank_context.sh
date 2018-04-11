#! /bin/bash

~/Téléchargements/eclipse-rdf4j-2.2.4/bin/console.sh -s http://147.100.175.100:8080/rdf4j-server

open phispubli

PREFIX event: <http://www.phenome-fppn.fr/vocabulary/m3p/2015/event#> 
PREFIX time: <http://www.w3.org/2006/time#> 
PREFIX oa: <http://www.w3.org/ns/oa#> 
PREFIX fn: <http://www.w3.org/2005/xpath-functions#> 
SELECT DISTINCT * FROM NAMED <http://www.phenome-fppn.fr/m3p/annotationAdded> 
FROM NAMED <http://www.phenome-fppn.fr/m3p/eventAdded> 
WHERE 
{ 
    {GRAPH <http://www.phenome-fppn.fr/m3p/eventAdded> {?s ?p ?o } } 
    UNION 
    {GRAPH <http://www.phenome-fppn.fr/m3p/annotationAdded> {?s ?p ?o } } 
}


