#!/usr/bin/python

""" This module aims at converting a csv file into a RDF graph in turtle syntax.
    More specificly it will read the columns :
    and parse them using the given associative array
"""

import argparse
import datetime
import csv
import json
import uuid
import re
from string import Formatter


class CSVtoTurtleConverter(object):
    """ A class to convert a csv to a rdf turtle file"""
    def __init__(self, prefix="", postfix = "", assocRules=None, grouping={}):
        self.assoc_rules = assocRules
        self.prefix = prefix
        self.postfix = postfix
        self.grouping = grouping
        AllUuidPerRow = []
        for rule in self.assoc_rules:
            AllUuidPerRow += re.findall(r'\{(uuid_\d+)\}', rule)
        self.uuid_per_row = set(AllUuidPerRow)
    def __computeGrouping(self, csvFile):
        groups_uuid = {}
        group_prefix = []
        with open(csvFile) as csvfile:
            reader = csv.DictReader(csvfile)
            for col in self.grouping.keys():
                group = self.grouping[col]
                groups_uuid[col] = {}
                ## dateNow need to be consistent across all rows of a grouping
                dateNow = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                last_grouping_column_value = None 
                for row in reader:
                    ## Handle multiline string as litteral, clear unsued space
                    for key in row.keys():
                        if isinstance(row[key], basestring):
                            row[key] = ' '.join(row[key].split())
                    if last_grouping_column_value == None:
                        group_uuid = str(uuid.uuid4())
                        last_grouping_column_value = row[col]
                    elif last_grouping_column_value != row[col]:
                        group_uuid = str(uuid.uuid4())
                    ## Added for further reference of the grouping inside the grouping rules
                    row['dateNow'] = dateNow
                    row['group_uuid'] = group_uuid
                    groups_uuid[col][row[col]] = group_uuid
                    line = ''
                    for rule in group:
                        line += rule.format(**row) + "\n"
                    line = line.encode('ascii', 'ignore')
                    group_prefix.append(line)
                    last_grouping_column_value = row[col]
            group_prefix = set(group_prefix)
        return groups_uuid, "\n".join(group_prefix)
    def __processRow(self, row, turtlefile, cpt, groups_uuid):
        # Handle multiline string as litteral
        for key in row.keys():
            if isinstance(row[key], basestring):
                row[key] = ' '.join(row[key].split())
        row['dateNow'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
        # Handle grouping (uuid per column)
        for col in self.grouping:
            row[col] = groups_uuid[col][row[col]]
        # Handle uuid per row 
        for key in self.uuid_per_row:
            row[key] = str(uuid.uuid4())
        # Add an identifier for the row index
        row['row'] = cpt
        # Fullfil the rules
        for rule in self.assoc_rules:
            skip = False
            for value in Formatter().parse(rule):
                if value[1] is not None:  
                    if row[value[1]] is '':
                        skip = True
                        break
            if skip:
                continue
            line = rule.format(**row) + "\n"
            line = line.encode('ascii', 'ignore')
            turtlefile.write(line)
        turtlefile.write('\n')
    def parse_csv(self, csvFile, turtleFile):
        """This function read a csv file and parse its content as a turtle rdf file"""
        groups_uuid, group_prefix = self.__computeGrouping(csvFile)
        with open(csvFile) as csvfile:
            with open(turtleFile, 'w') as turtlefile:
                reader = csv.DictReader(csvfile)
                turtlefile.write(self.prefix)
                turtlefile.write('\n')
                turtlefile.write(group_prefix)
                turtlefile.write('\n')
                cpt = 0
                for row in reader:
                    self.__processRow(row, turtlefile, cpt, groups_uuid)
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
        ' \n'.join(config['postfix']) if 'postfix' in config else "\n",\
        config['associativeRules'],\
        config['groupingRules'] if 'groupingRules' in config else {})
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

# mystring = "{a} puis {b} et enfin {c}{d}"
# mydict = {'a' : 'a', 'b' : 'bhee', 'c' : 'cheh', 'd' : 'dai'}
# # .format(**mydict)
# formatter = string.Formatter()
# ite = formatter.parse(mystring)
# for t in ite:
#     print(t[1])
