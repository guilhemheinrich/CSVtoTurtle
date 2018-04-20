#! /bin/bash

pathToDateFormater='/home/heinrich/PHENOME/Ontology/DateParser.py'
pathToCSVparser='/home/heinrich/PHENOME/Ontology/CSVparser.py'
pathToCsv='/home/heinrich/PHENOME/Ontology/toParse/csv'
pathToCsvParsed='/home/heinrich/PHENOME/Ontology/toParse/csv/parsed'
pathToTurtle='/home/heinrich/PHENOME/Ontology/toParse/turtle'
pathToConfig='/home/heinrich/PHENOME/Ontology/toParse/json'


# parse date

for file in $(ls $pathToCsv)
do
    if [[ $file != *parsed* ]]
    then
    fullPathFile=$pathToCsv/$file
    basename=$(basename $file .csv)
    $pathToDateFormater $fullPathFile
    fi
done


# parse csv to turtle

for file in $(ls $pathToCsvParsed)
do
    if [[ $file == *parsed* ]]
    then
    fullPathFile=$pathToCsvParsed/$file
    basename=$(basename $file .csv)
    echo "COMPUTING $pathToCSVparser -i $fullPathFile -o $pathToTurtle/$basename.ttl $pathToConfig/config_$basename.json"
    $pathToCSVparser -i $fullPathFile -o $pathToTurtle/$basename.ttl $pathToConfig/config_$basename.json
    fi
done
