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
import string


class CSVtoTurtleConverter(object):
    """ A class to convert a csv to a rdf turtle file"""
    def __init__(self, prefix=None, postfix = None, assocRules=None, uuidPerRow=0, grouping={}, dateColumns = []):
        self.assoc_rules = assocRules
        self.prefix = prefix
        self.postfix = postfix
        self.uuid_per_row = uuidPerRow
        self.grouping = grouping
        self.date_columns = dateColumns
    def __computeGrouping(self, csvFile):
        groups_uuid = {}
        group_prefix = []
        with open(csvFile) as csvfile:
            reader = csv.DictReader(csvfile)
            for col in self.grouping.keys():
                group = self.grouping[col]
                # col = group.key()
                groups_uuid[col] = {}
                ## dateNow need to be consistent across all rows of a grouping
                dateNow = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                last_grouping_column_value = None 
                for row in reader:
                    ## Handle multiline string as litteral, clear unsued space
                    for key in row.keys():
                        if isinstance(row[key], basestring):
                            row[key] = ' '.join(row[key].split())
                    # Handle date format
                    for col in self.date_columns:
                        row[col] = datetime.datetime(row[col]).strftime('%Y-%m-%dT%H:%M:%S.%f')
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
            # print(group_prefix)
        return groups_uuid, "\n".join(group_prefix)
    def parse_csv(self, csvFile, turtleFile):
        """This function read a csv file and parse its content as a turtle rdf file"""
        groups_uuid, group_prefix = self.__computeGrouping(csvFile)
        print(groups_uuid)
        with open(csvFile) as csvfile:
            with open(turtleFile, 'w') as turtlefile:
                reader = csv.DictReader(csvfile)
                turtlefile.write(self.prefix)
                turtlefile.write('\n')
                turtlefile.write(group_prefix)
                turtlefile.write('\n')
                cpt = 0
                for row in reader:
                    # Handle multiline string as litteral
                    for key in row.keys():
                        if isinstance(row[key], basestring):
                            row[key] = ' '.join(row[key].split())
                    row['dateNow'] = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
                    # Handle grouping (uuid per column)
                    for col in self.grouping:
                        row[col] = groups_uuid[col][row[col]]
                    # Handle date format
                    for col in self.date_columns:
                        row[col] = datetime.datetime(row[col]).strftime('%Y-%m-%dT%H:%M:%S.%f')
                    # Handle uuid per row 
                    for i in range(0, self.uuid_per_row):
                        row['uuid_' + str(i)] = str(uuid.uuid4())
                    row['row'] = cpt
                    # Fullfil the rules
                    for rule in self.assoc_rules:
                        line = rule.format(**row) + "\n"
                        line = line.encode('ascii', 'ignore')
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
        config['groupingRules'] if 'groupingRules' in config else {},\
        config['dateColumns'] if 'dateColumns' in config else [])
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
dt = datetime.datetime.strptime('2017-03-03', '%Y-%m-%dT%H:%M:%S.%f')