#! /bin/bash


pathToCsv='/home/heinrich/PHENOME/Ontology/toParse/csv'
pathToTurtle='/home/heinrich/PHENOME/Ontology/toParse/turtle'
pathToConfig='/home/heinrich/PHENOME/Ontology/toParse/json'
# parse date

for file in $(ls $pathToCsv)
do
    if [[ $file != *parsed* ]]
    then
    fullPathFile=$pathToCsv/$file
    basename=$(basename $file .csv)
    /home/heinrich/PHENOME/Ontology/DateParser.py $fullPathFile
    fi
done

# parse csv to turtle

for file in $(ls $pathToCsv)
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
# ## DIA
# ../DateParser.py csv/Events_DIA2017-05-19-toImport.csv
# ../DateParser.py csv/Annot_DIA2017-05-19-toImport.csv
# ../CSVparser.py -i csv/Events_DIA2017-05-19-toImport_parsed.csv -o turtle/Events_DIA2017-05-19-toImport.ttl json/config_events_dia2017-05-19.json
/home/heinrich/PHENOME/Ontology/CSVparser.py -i /home/heinrich/PHENOME/Ontology/toParse/csv/Annot_DIA2017-05-19-toImport_parsed.csv -o /home/heinrich/PHENOME/Ontology/toParse/turtle/Annot_DIA2017-05-19-toImport_parsed.ttl /home/heinrich/PHENOME/Ontology/toParse/json/config_Annot_DIA2017-05-19-toImport_parsed.json

# ## ARCH2017
# ../DateParser.py  csv/trouble_ARCH2017-03-30-toImport.csv
# ../DateParser.py  csv/Events_ARCH2017-03-30-toImport.csv
# ../DateParser.py csv/move_ARCH2017-03-30-toImport.csv
# ../CSVparser.py -i csv/trouble_ARCH2017-03-30-toImport_parsed.csv -o turtle/trouble_ARCH2017-03-30-toImport.ttl json/config_troubles_arch2017-03-30.json
# ../CSVparser.py -i csv/Events_ARCH2017-03-30-toImport_parsed.csv -o turtle/Events_ARCH2017-03-30-toImport.ttl json/config_events_arch2017-03-30.json
# ../CSVparser.py -i csv/move_ARCH2017-03-30-toImport_parsed.csv -o turtle/move_ARCH2017-03-30-toImport.ttl json/config_move_arch2017-03-30.json

