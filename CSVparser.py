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
    def __init__(self, prefix=None, postfix = None, assocRules=None, uuidPerRow=0, grouping=[]):
        self.assoc_rules = assocRules
        self.prefix = prefix
        self.postfix = postfix
        self.uuid_per_row = uuidPerRow
        self.grouping = grouping
    def __computeGrouping(self, csvFile):
        groups_uuid = {}
        with open(csvFile) as csvfile:
            reader = csv.DictReader(csvfile)
            for col in self.grouping:
                groups_uuid[col] = {}
                for row in reader:
                    groups_uuid[col][row[col]] = str(uuid.uuid4())
        return groups_uuid
    def parse_csv(self, csvFile, turtleFile):
        """This function read a csv file and parse its content as a turtle rdf file"""
        groups_uuid = self.__computeGrouping(csvFile)
        with open(csvFile) as csvfile:
            with open(turtleFile, 'w') as turtlefile:
                reader = csv.DictReader(csvfile)
                turtlefile.write(self.prefix)
                turtlefile.write('\n')
                cpt = 0
                for row in reader:
                    # Handle multiline string as litteral
                    for key in row.keys():
                        if isinstance(row[key], basestring):
                            row[key] = ' '.join(row[key].split())
                    # Handle grouping (uuid per column)
                    for col in self.grouping:
                        row[col] = groups_uuid[col][row[col]]
                    # Handle uuid per row 
                    for i in range(0, self.uuid_per_row):
                        row['uuid_' + str(i)] = str(uuid.uuid4())
                    row['row'] = cpt
                    # Fullfil the rules
                    for rule in self.assoc_rules:
                        line = rule.format(**row) + "\n"
                        turtlefile.write(line)
                    turtlefile.write('\n')
                    cpt += 1
                turtlefile.write(self.postfix)

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
        converter = CSVtoTurtleConverter(\
        ' \n'.join(config['prefix']),\
        ' \n'.join(config['postfix']) if 'postfix' in config else None,\
        config['associativeRules'],\
        config['uuidPerRow'] if 'uuidPerRow' in config else None,\
        config['grouping'] if 'uuidPgroupingerRow' in config else [])
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
#                     " lol<{Experiment}>",
#                    ]
            



# myConv = CSVtoTurtleConverter(prefix, None, associativeRules, 1, ['Experiment'])
# myConv.parse_csv('Events ARCH2017-03-30.csv', 'Events ARCH2017-03-30.ttl')
