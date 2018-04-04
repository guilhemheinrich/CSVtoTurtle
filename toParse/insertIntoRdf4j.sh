#! /bin/bash

~/Téléchargements/eclipse-rdf4j-2.2.4/bin/console.sh -s http://147.100.175.100:8080/rdf4j-server

open phispubli
# load [things]

# Fix /
sparql
PREFIX vocabulary: <http://www.phenome-fppn.fr/vocabulary/m3p/2015#>
PREFIX event: <http://www.phenome-fppn.fr/vocabulary/m3p/2015/event#>
WITH <http://www.phenome-fppn.fr/m3p/event>
DELETE {?event event:to ?oldURI }
INSERT {?event event:to ?newURI }
WHERE {
  ?event event:to ?oldURI .
  BIND (URI(REPLACE(STR(?oldURI), "http://www.phenome-fppn.fr/m3p/phenoarch/", "http://www.phenome-fppn.fr/m3p/phenoarch")) AS ?newURI)
}
.

sparql
PREFIX vocabulary: <http://www.phenome-fppn.fr/vocabulary/m3p/2015#>
PREFIX event: <http://www.phenome-fppn.fr/vocabulary/m3p/2015/event#>
WITH <http://www.phenome-fppn.fr/m3p/event>
DELETE {?event event:from ?oldURI }
INSERT {?event event:from ?newURI }
WHERE {
  ?event event:from ?oldURI .
  BIND (URI(REPLACE(STR(?oldURI), "http://www.phenome-fppn.fr/m3p/phenoarch/", "http://www.phenome-fppn.fr/m3p/phenoarch")) AS ?newURI)
}
.