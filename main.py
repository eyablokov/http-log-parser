#!/usr/bin/env python3
''' This script is for logs parsing. You could be placing
    log file (Apache, Nginx, etc), edit pattern appropriately
    and get result parsed from it as a file created with
    "parsed_MyInputFile" name. Thank you. '''

__author__ = "Evgeniy Yablokov"
__email__ = "eyablokov@me.com"
__license__ = "None"

import re

def find(pattern, text):
    ''' Low level function
        It just primitively putting the pattern defined
        in "get_requests" function on to input file's
        lines '''
    match = re.findall(pattern, text)
    if match:
        return match
    return False

def get_requests(f):
    ''' The function which does main job
          - reads incoming data from the input file
          - defines regexp pattern to apply
          - triggers "find" function argumenting it with
            the pattern and input file line by line
        Attention: GET method and 200 status are defined
        here. Edit it appropriately for your needs '''
    log_line = f.read()
    pattern = (r''
                '(\d+.\d+.\d+.\d+)\s-\s-\s' # ip address
                '\[(.+)\]\s'                # datetime
                '"GET\s(.*)\s\w+/.+"\s'     # requested file
                '200\s'                     # http status
                '(\d+)\s'                   # bytes size
                '"(.+)"\s'                  # referer
                '"(.+)"'                    # user agent
    )
    requests = find(pattern, log_line)
    return requests

def process_log(log):
    ''' the function just triggers "get_requests" function
        argumenting it with input file's content '''
    requests = get_requests(log)
    return requests

''' The main working entrypoint of the script
      - going to get the input and output files
      - open the input file, to work with incoming data
      - get the resulting facts
      - open the output file and write the facts into it '''
if __name__ == '__main__':
    input_file = 'log00.log'
    output_file = 'parsed_'+input_file
    log_file = open(input_file, 'r')
    get_the_facts = process_log(log_file)
    saved_file = open(output_file, 'w')
    saved_file.write('\n'.join(map(str, get_the_facts)))
