#! \bin\bash

## DIA
../CSVparser.py -i csv/Events_DIA2017-05-19-toImport.csv -o turtle/Events_DIA2017-05-19-toImport.ttl json/config_events_dia2017-05-19.json
../CSVparser.py -i csv/Annot_DIA2017-05-19-toImport.csv -o turtle/Annot_DIA2017-05-19-toImport.ttl json/config_annot_dia2017-05-19.json

## ARCH2017
../CSVparser.py -i csv/trouble_ARCH2017-03-30-toImport.csv -o turtle/trouble_ARCH2017-03-30-toImport.ttl json/config_troubles_arch2017-03-30.json
../CSVparser.py -i csv/Events_ARCH2017-03-30-toImport.csv -o turtle/Events_ARCH2017-03-30-toImport.ttl json/config_events_arch2017-03-30.json
../CSVparser.py -i csv/move_ARCH2017-03-30-toImport.csv -o turtle/move_ARCH2017-03-30-toImport.ttl json/config_move_arch2017-03-30.json
