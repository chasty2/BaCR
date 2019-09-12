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

import csv
import multiprocessing
import pandas
from pathlib import Path
import subprocess
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
## helper function for createBatchFile. creates a string for a crispresso2 
## .tsv batchfile and returns it to the createBatchFile function
#

def _createTSVTitle(projectID, guideName, readSet):
    if guideName == 'nan':
        title = f'{projectID}_{readSet}.tsv'
    else:
        title = f'{projectID}_{guideName}_{readSet}.tsv'

    return str(title)
###########################################################################

#
## helper function for createBatchFile. Populates .tsv file with sample
## names and file paths for both R1 and R2
#

def _populateBatchFilePairedEnd(projectID, guideName,writer):
    # write title
    writer.writerow(['name', 'fastq_r1', 'fastq_r2'])
    # declare path to R1 and R2 reads
    if guideName == 'nan':
        r1Path = Path(f'{projectID}/R1')
        r2Path = Path(f'{projectID}/R2')
    else:
        r1Path = Path(f'{projectID}/{guideName}/R1')
        r2Path = Path(f'{projectID}/{guideName}/R2')
    # loop through R1 files and slice filename to get sampleName and R2
    for r1 in r1Path.glob('*.fastq.gz'):
        sampleName = r1.name[:-12]
        r2 = r2Path / f'{sampleName}_R2.fastq.gz'
        #populate row
        writer.writerow([sampleName, r1, r2])

    return
    
###########################################################################

#
## helper function for createBatchFile. Populates .tsv file with sample
## names and file paths for the specified readSet
#

def _populateBatchFileSingleRead(projectID, guideName, readSet, writer):
    #write title
    writer.writerow(['name', 'fastq_r1'])
    #declare path to reads specified by readSet
    if guideName == 'nan':
        readPath = Path(f'{projectID}/{readSet}')
    else:
        readPath = Path(f'{projectID}/{guideName}/{readSet}')
    #loop through .fastq files and slice filename to get sampleName
    for fastq in readPath.glob('*.fastq.gz'):
        sampleName = fastq.name[:-12]
        #populate row
        writer.writerow([sampleName, fastq])

    return

###########################################################################

#
## creates the .tsv batchfile for CRISPResso2 for a given dataset (row in
## .csv, given as a tuple) and populates it with the names and paths of
## the .fastq files in that dataset. Returns .tsv
#

def createBatchFile(projectID, guideName, readSet):
    ##create .tsv file with title corresponding to dataset
    title = _createTSVTitle(projectID, guideName, readSet)
    with open(title, 'w') as tsvFile:
        writer = csv.writer(tsvFile, delimiter = '\t', lineterminator = '\n')
        if readSet == 'PE':
            _populateBatchFilePairedEnd(projectID, guideName, writer)
        else:
            _populateBatchFileSingleRead(projectID, guideName, readSet, writer)

    return tsvFile

    
###########################################################################

#
## concatenates strings from dataset inputs to create command input for
## CRISPRessoBatch
#

def createCRISPRessoInput(batchFile, coresToUse, projectID, guideName,
                          readSet, amplicon, guideSeq, hdr, cr2Params):
    # declare CRISPResso2 command and concatenate mandatory parameters
    CRISPRessoInput = f'CRISPRessoBatch --batch_settings {batchFile}'
    CRISPRessoInput = f'{CRISPRessoInput} -p {coresToUse} --skip_failed'
    # specify output folder
    if guideName == 'nan':
        outputPath = Path(f'{projectID}/CRISPRessoBatch_Analysis_{readSet}')
        CRISPRessoInput = f'{CRISPRessoInput} -bo {outputPath}'
    else:
        outputPath = Path(f'{projectID}/{guideName}/CRISPRessoBatch_Analysis_{readSet}')
        CRISPRessoInput = f'{CRISPRessoInput} -bo {outputPath}'
    #slice amplicon for R1/R2 analysis if amplicon size > 165
    if readSet == 'R1' and len(amplicon) > 165:
        CRISPRessoInput = f'{CRISPRessoInput} -a {amplicon[:149]}'
    elif readSet == 'R2' and len(amplicon) > 165:
        CRISPRessoInput = f'{CRISPRessoInput} -a {amplicon[149:]}'
    else:
        CRISPRessoInput = f'{CRISPRessoInput} -a {amplicon}'
    # concatenate additional parameters if they exist
    if guideSeq != 'nan':
        CRISPRessoInput = f'{CRISPRessoInput} -g {guideSeq}'
    if hdr != 'nan':
        CRISPRessoInput = f'{CRISPRessoInput} -e {hdr}'
    if cr2Params != 'nan':
        CRISPRessoInput = f'{CRISPRessoInput} {cr2Params}'
    
    return CRISPRessoInput

###########################################################################


#
## master function of rcb.py:
##      1. declares variables from input dataTuple in human-readable form
##      2. creates batchfile(s) for dataset based on R1/R2/PE column
##      3. build CRISPRessoBatch input
##      4. Run CRISPRessoBatch
#

def runCRISPRessoLoop(dataTuple):
    # declare variables. split reads inputs into tuples for 
    # separate analyses for R1,R2,PE
    coresToUse = str(int(multiprocessing.cpu_count()-2))
    projectID = str(dataTuple[0])
    guideName = str(dataTuple[1])
    reads =tuple(str(dataTuple[2]).split(","))
    amplicon = str(dataTuple[3])
    guideSeq = str(dataTuple[4])
    hdr = str(dataTuple[5])
    cr2Params =str(dataTuple[6])

    # create batchfile(s), CRISPResso2 input(s), and call cr2 for each
    for readSet in reads:
        batchFile = createBatchFile(projectID, guideName, readSet)
        CRISPRessoInput = createCRISPRessoInput(batchFile.name, coresToUse,
                                                projectID,guideName,
                                                readSet,amplicon,
                                                guideSeq, hdr, cr2Params)
        subprocess.run(str(CRISPRessoInput), shell=True, cwd = str(Path.cwd()))

    return

###### MAIN ###############################################################

checkInputs()

## argc = 2
if len(sys.argv) == 2:
    csvFile = pandas.read_csv(sys.argv[1])
    ## run CRISPRessoBatch on each dataset, given as a row in csvFile
    for row in csvFile.itertuples():
        runCRISPRessoLoop(tuple(row[1:]))

