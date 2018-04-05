#! /bin/bash


# parse date

for file in $(ls $PWD/toParse/csv)
do
    if [[ $file != *parsed* ]]
    then
    fullPathFile=$(readlink -f $file)
    /home/heinrich/PHENOME/Ontology/DateParser.py $fullPathFile
    fi
done

# parse csv to turtle

pathToCsv='/home/heinrich/PHENOME/Ontology/toParse/csv'
pathToTurtle='/home/heinrich/PHENOME/Ontology/toParse/turtle'
pathToConfig='/home/heinrich/PHENOME/Ontology/toParse/json'
for file in $(ls $PWD/toParse/csv)
do
    if [[ $file == *parsed* ]]
    then
    fullPathFile=$pathToCsv/$file
    basename=$(basename $file .csv)
    /home/heinrich/PHENOME/Ontology/CSVparser.py -i $fullPathFile -o $pathToTurtle/$basename.ttl $pathToConfig/config_$basename.json
    echo $fullPathFile
    echo $basename
    fi
done
## DIA
../DateParser.py csv/Events_DIA2017-05-19-toImport.csv
../DateParser.py csv/Annot_DIA2017-05-19-toImport.csv
../CSVparser.py -i csv/Events_DIA2017-05-19-toImport_parsed.csv -o turtle/Events_DIA2017-05-19-toImport.ttl json/config_events_dia2017-05-19.json
../CSVparser.py -i csv/Annot_DIA2017-05-19-toImport_parsed.csv -o turtle/Annot_DIA2017-05-19-toImport.ttl json/config_annot_dia2017-05-19.json

## ARCH2017
../DateParser.py  csv/trouble_ARCH2017-03-30-toImport.csv
../DateParser.py  csv/Events_ARCH2017-03-30-toImport.csv
../DateParser.py csv/move_ARCH2017-03-30-toImport.csv
../CSVparser.py -i csv/trouble_ARCH2017-03-30-toImport_parsed.csv -o turtle/trouble_ARCH2017-03-30-toImport.ttl json/config_troubles_arch2017-03-30.json
../CSVparser.py -i csv/Events_ARCH2017-03-30-toImport_parsed.csv -o turtle/Events_ARCH2017-03-30-toImport.ttl json/config_events_arch2017-03-30.json
../CSVparser.py -i csv/move_ARCH2017-03-30-toImport_parsed.csv -o turtle/move_ARCH2017-03-30-toImport.ttl json/config_move_arch2017-03-30.json

