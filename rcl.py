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

#
##
#

def noNan():
    print('noNaN')

###########################################################################

#
##
#

def allNan():
    print('allNan') 

###########################################################################

#
##
#

def gNameNan():
    print('gNameNan')

###########################################################################

#
##
#

def gSeqNan():
    print('gSeqNan')

###########################################################################

#
##
#

def hdrNan():
    print('hdrNan')

###########################################################################

#
##
#

def cr2ParamsNan():
    print('cr2ParamsNan')

###########################################################################

#
##
#

def gNameGSeqNan():
    print('gNameGSeqNan')

###########################################################################

#
##
#

def gSeqHDRNan():
    print('gNameGSeqNan')

###########################################################################

#
##
#

def hdrCR2ParamsNan():
    print('hdrCR2ParamsNan')

###########################################################################

#
##
#

def 

###########################################################################

#
##
#

###########################################################################

#
##
#

###########################################################################

#
##
#

###########################################################################

#
##
#

###########################################################################

#
##
#

###########################################################################

#
##
#

###########################################################################

#
## Builds a dictionary of inputs that will be used to determine which
## CRISPResso2 parameters will be ran on the .fastq files of a given 
## project. Parameters will be decided based on which inputs are not
## specified ('nan') for the given project
#

# 16 combinations of 4 parameters:
#   1x noNan
#   1x allNan
#   4x combo of 1
#   6x combo of 2
#   4x combo of 3

# NOTE: R1, R2, PE analysis not determined here

def buildLoopDictionary():
    print('Building Loop Dictionary')
    loopDictionary = { (): noNan,                                      # 
                       (GuideNames, GuideSeq, HDR, CR2_Params): allNan,#
                       (GuideNames): gNameNan,                  #4x1combo#
                       (GuideSeq): gSeqNan, #
                       (HDR): hdrNan,   #
                       (CR2_Params): cr2_ParamsNan,#
                       (GuideNames, GuideSeq): gNameGSeqNan,    #6x2combo#
                       (GuideSeq, HDR): gSeqHDRNan, #
                       (HDR, CR2_Params): hdrCR2ParamsNan,#
                       (GuideNames, HDR): gNameHDRNan,#
                       (GuideSeq, CR2_Params): gSeqCR2ParamsNan,
                       (GuideNames, CR2_Params): gNameCR2ParamsNan,
                       (GuideNames, GuideSeq, HDR): gNameGSeqHDRNan, #4x3combo
                       (GuideSeq, HDR, CR2_Params): gSeqHDRCR2ParamsNan,
                       (GuideNames, GuideSeq, CR2_Params): gNameGSeqCR2ParamsNan,
                       (GuideNames, HDR, CR2_Params): gNameHDRCR2ParamsNan}
    return loopDictionary

##### MAIN ################################################################

checkInputs()

loopDictionary = buildLoopDictionary()
print(loopDictionary)


