#!/usr/bin/python

""" This module aims at converting a csv file into a RDF graph in turtle syntax.
    More specificly it will read the columns : 
    and parse them using the given associative array
"""

import argparse
import csv
import json
import uuid


class CSVtoTurtleConverter(object):
    """ A class to convert a csv to a rdf turtle file"""
    def __init__(self, prefix = None, assocRules = None, uuidPerRow = None):
        self.assoc_rules = assocRules
        self.prefix = prefix
        self.uuid_per_row = uuidPerRow
    def parse_csv(self, csvFile, turtleFile):
        """This function read a csv file and parse its content as a turtle rdf file"""
        with open(csvFile) as csvfile:
            with open(turtleFile, 'w') as turtlefile:
                reader = csv.DictReader(csvfile)
                turtlefile.write(self.prefix)
                turtlefile.write('\n')
                cpt = 0
                for row in reader:
                    for i in range(0, self.uuid_per_row):
                        row['uuid_' + str(i)] = str(uuid.uuid4())
                    row['row'] = cpt
                    for rule in self.assoc_rules:
                        line = rule.format(**row) + "\n"
                        turtlefile.write(line)
                        # print (line)
                    turtlefile.write('\n')
                    cpt += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = """ This module aims at converting a csv file into a RDF graph in turtle syntax.
    More specificly it will read the columns : 
    and parse them using the given associative array
""")
    parser.add_argument('configJSON', help="""Path to the configuration file to parse the csv, in json format.""")
    parser.add_argument('-i', dest = 'input', help="""Path to the input CSV file""")
    parser.add_argument('-o', dest = 'output', help="""Path to the output turtle file""")
    args = parser.parse_args()
    with open(args.configJSON, 'r') as jsonconfigfile:
        config = json.load(jsonconfigfile)
        converter = CSVtoTurtleConverter(' \n'.join(config['prefix']), config['associativeRules'], config['uuidPerRow'])
        converter.parse_csv(args.input, args.output)
        

    
# prefix = """
# @prefix : <http://www.phenome-fppn.fr/vocabulary/m3p/2015/event#> .
# @prefix owl: <http://www.w3.org/2002/07/owl#> .
# @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
# @prefix xml: <http://www.w3.org/XML/1998/namespace> .
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
# @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
# @base <http://www.phenome-fppn.fr/vocabulary/m3p/2015/event> .
# """


# associativeRules = ["<event{uuid_0}> rdf:type :{Category} ;",
#                     "   :concern <{uri}> ;",
#                     "   :inDateTime \"{Date event}\" .",
#                    ]



# myConv = CSVtoTurtleConverter(prefix, associativeRules, 1)
# myConv.parse_csv('Events ARCH2017-03-30.csv', 'Events ARCH2017-03-30.ttl')