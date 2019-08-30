#! /usr/bin/python3.6

'''

rcl.py: Run Crispresso Loop(s)

    Part 3 of the BaCR pipeline. rcl.py will analyze each .fastq file in
    one or more sets of data using CRISPResso2. It accepts the BaCR .csv
    spreadsheet as a command-line argument, looping over each dataset and
    running CRISPResso2 with the specified parameters. It also accepts a 
    set of command-line arguments in the format of one row of the BaCR.csv 
    spreadsheet for standalone use on a single project.

    Designed for use by UIC's Genome Editing Core

    Written by Cody Hasty in Vim 7.4 on Centos 7 on 09/2019

    Usage: rcl.py bacr_spreadsheet.csv
        
           OR

           rcl.py projectID guideName R1/R2/PE amplicon guideSeq HDR cr2_params

    NOTE: For any unspecified parameters(e.g. no guideName, guideSeq, HDR,
          and/or cr2_params), enter nan. The length and order of argv is
          important for rcl.py to run properly

'''

import sys

###########################################################################

#
## validate argc, print help info if 'rcl.py -h' is used
#

def checkInputs():
    ##help flag
    if str(sys.argv[1]) == '-h':
        print('''
rcl.py: Run Crispresso Loop(s)

    Part 3 of the BaCR pipeline. rcl.py will analyze each .fastq file in
    one or more sets of data using CRISPResso2. It accepts the BaCR .csv
    spreadsheet as a command-line argument, looping over each dataset and
    running CRISPResso2 with the specified parameters. It also accepts a 
    set of command-line arguments in the format of one row of the BaCR.csv 
    spreadsheet for standalone use on a single project.

    Designed for use by UIC's Genome Editing Core

    Written by Cody Hasty in Vim 7.4 on Centos 7 on 09/2019

Usage:
    
    rcl.py bacr_spreadsheet.csv
        
    OR

    rcl.py projectID guideName R1/R2/PE amplicon guideSeq HDR cr2_params

NOTE: For any unspecified parameters(e.g. no guideName, guideSeq, HDR,
      and/or cr2_params), enter nan. The length and order of argv is
      important for rcl.py to run properly
        ''')
        exit()
    #check argc
    elif len(sys.argv) != 2 and len(sys.argv) != 8:
        print('ERROR: Invalid command line arguments')
        print('''
Usage: 

    rcl.py bacr_spreadsheet.csv
        
    OR

    rcl.py projectID guideName R1/R2/PE amplicon guideSeq HDR cr2_params

NOTE: For any unspecified parameters(e.g. no guideName, guideSeq, HDR,
      and/or cr2_params), enter nan. The length and order of argv is
      important for rcl.py to run properly
        ''')
        exit()

###########################################################################

###### MAIN ###############################################################

checkInputs()



