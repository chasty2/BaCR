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

import multiprocessing
import pandas
from pathlib import Path
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

#
##
#

#def createTSVTitle()
###########################################################################

#
## helper function for createBatchFile. creates and populates .tsv file
## with sample names and file paths for R1 and R2
#

def _createBatchFilePE(fastqPath, projectID, guideName, readSet):
    #create title string
    if guideName == 'nan':
        title = f'{projectID}_PE_batchfile.tsv'
    else:
        title = f'{projectID}_{guideName}_PE_batchfile.tsv'
    print(title)
    #create title

###########################################################################

#
##
#

#def _createBatchFileSingleRead()

###########################################################################

#
## creates the .tsv batchfile for CRISPResso2 for a given dataset (row in
## .csv, given as a tuple) and moves it to it's respective subdirectory
#

def createBatchFile(projectID, guideName, readSet):
    #declare path to .fastq files based on directory structure
    fastqPath = Path(projectID)
    print(str(fastqPath))
    if guideName == 'nan':
        _createBatchFilePE(fastqPath, projectID, guideName)
    else:
        fastqPath = fastqPath / guideName
        _createBatchFilePE(fastqPath, projectID, guideName)

###########################################################################

#
## master function of rcb.py:
##      1. declares variables from input dataTuple in human-readable form
##      2. creates batchfile(s) for dataset based on R1/R2/PE column
#

def runCRISPRessoLoop(dataTuple):
    # declare variables. split reads and cr2Params inputs into tuples for 
    # separate analyses for R1,R2,PE +- additional parameters
    coresToUse = str(int(multiprocessing.cpu_count()-2))
    projectID = str(dataTuple[0])
    guideName = str(dataTuple[1])
    reads =tuple(str(dataTuple[2]).split(","))
    amplicon = str(dataTuple[3])
    guideSeq = str(dataTuple[4])
    hdr = str(dataTuple[5])
    cr2Params =tuple(str(dataTuple[6]).split(","))

    # create analysis subdirectory(s) and batchfile(s)
    for readSet in reads:
        createBatchFile(projectID, guideName, readSet)


###### MAIN ###############################################################

checkInputs()

## argc = 2
if len(sys.argv) == 2:
    csvFile = pandas.read_csv(sys.argv[1])
    ## run CRISPRessoBatch on each dataset, given as a row in csvFile
    for row in csvFile.itertuples():
        runCRISPRessoLoop(tuple(row[1:]))

