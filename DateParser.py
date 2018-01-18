#!/usr/bin/python

import re
import time
import argparse
import os


""" This module aims at converting all occurence of a date to
    a valid xsd:dateTimeStamp.
"""

class DateFormatter:
    token = 'MATCH'
    date_format_regex = [\
'(?P<year>\d{4})(?P<sepD>.)(?P<mounth>\d{2})(?P=sepD)(?P<day>\d{2})',\
'(?P<day>\d{2})(?P<sepD>.)(?P<mounth>\d{2})(?P=sepD)(?P<year>\d{4})',\
'(?P<year>\d{4})(?P<sepD>.)(?P<mounth>\d{2})(?P=sepD)(?P<day>\d{2}).{0,2}\
(?P<hour>\d{2})(?P<sepT>)(?P<minute>\d{2})(?P=sepT)(?P<second>\d{2})',\
'(?P<day>\d{2})(?P<sepD>.)(?P<mounth>\d{2})(?P=sepD)(?P<year>\d{4}).{0,2}\
(?P<hour>\d{2})(?P<sepT>)(?P<minute>\d{2})(?P=sepT)(?P<second>\d{2})'\
]
    def __init__(self,\
    year = '2000',\
    mounth = '01',\
    day = '01',\
    hour = '12',\
    minute = '00',\
    second = '00',\
    timezoneShift = None,\
    **kwargs):
        self.year = year
        self.mounth = mounth
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.timezone_shift = time.localtime().tm_isdst
        if timezoneShift:
            self.timezone_shift = timezoneShift
    def asXsdDateTimeStamp(self):
        # pattern_XsdDateTimeStamp = '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z|((+|-)\d{2}:\d{2})'
        output = "{year}-{mounth}-{day}T{hour}:{minute}:{second}".format(**self.__dict__)
        if self.timezone_shift == 0:
            output +='Z'
        elif isinstance(self.timezone_shift, int):
            ## If it's an integer, it's between -14 and 14
            assert self.timezone_shift < 15 and self.timezone_shift > -15
            if self.timezone_shift > 0:
                output += '+'
                if self.timezone_shift < 9:
                    output += '0' + str(self.timezone_shift) +':00'
                else:
                    output += str(self.timezone_shift) +':00'
            else:
                if self.timezone_shift > -10:
                    output += '0' + str(abs(self.timezone_shift)) +':00'
                else:
                    output += str(abs(self.timezone_shift)) +':00'
        ## Otherwise it's already a string
        else:
            assert isinstance(self.timezone_shift, basestring)
            output += self.timezone_shift
        return output
    @staticmethod
    def compute(stringOrMatch, token = ''):
        if stringOrMatch.__class__.__name__== 'SRE_Match':
            dateFormatter = DateFormatter(**stringOrMatch.groupdict())
            return token + dateFormatter.asXsdDateTimeStamp()
        else:
            return stringOrMatch
    @staticmethod
    def fromFile(infile, outfile = None):
        if outfile:
            output = outfile
        else:
            filename, file_extension = os.path.splitext(infile)
            output = filename + '_parsed' + file_extension
        with open(infile) as inputFile:
            with open(output, 'w') as outputFile:
                for line in inputFile:
                    new_line = DateFormatter.fromString(line)
                    outputFile.write(new_line)
    @staticmethod
    def fromString(stringToParse):
        old_line = stringToParse
        for pattern in DateFormatter.date_format_regex:
            patternAndToken = '(?<!' + DateFormatter.token + ')' + pattern
            new_line = re.sub(patternAndToken, lambda line: DateFormatter.compute(line, DateFormatter.token), old_line)
            if old_line != new_line:
                old_line = new_line
        new_line = re.sub(DateFormatter.token, '', new_line)
        return new_line
 



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = """ This module aims at converting all date to 
    the xsd:DateTimeStamp format (As described in http://www.datypic.com/sc/xsd11/t-xsd_dateTimeStamp.html).
""")
    parser.add_argument('-i', dest = 'input', help="""Path to the input file""")
    parser.add_argument('-o', dest = 'output',nargs = '?', help="""Path to the output file""")
    args = parser.parse_args()
    print(args.__dict__)
    DateFormatter.fromFile( infile = args.input, outfile = args.output)

# datestring = '20-02-2018 blasdjwbc 20-04-2018'
# DateFormatter.fromString(datestring)


