#!/bin/bash

## BaCR: basemount-CRISPResso2 pipeline

## master script of the BaCR pipeline. This script calls the individual
## pieces of the pipeline in order

## 1: bcp.py: copies and organizes files from basemount by project/guide
## 2: rcb.py: runs CRISPRessoBatch on each specified dataset

## command line input: bacr.sh -flag basemount_path input.csv
##      flags:
##          -p      copy from BaseSpace/Projects
##          -r      copy from BaseSpace/Runs
##          -s      skip bcp.py
##          -h      help

bcp.py $1 $2 $3
rcb.py $3
