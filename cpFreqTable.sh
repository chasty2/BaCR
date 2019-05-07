#!/bin/bash

## cpFreqTable: a helper script for the BaCR pipeline to copy the allele
## frequency table from CRISPResso analyses to ProjectID/FreqTables/, a directory
## structure created with bcp.sh

## written by Cody Hasty in vim on Ubuntu 16.04 LTS on 5/3/2019

## Command line input: cpFreqTable.sh projectID fastq

##NOTE: this will not work for projects using multiple guides. Debug this

fastqName=$(basename $2 .fastq.gz)
i=1
for freqTable in $1/Analyses/CRISPResso_on_$fastqName*/9.Alleles*.pdf
do
     cp $freqTable $1/FreqTables/"$fastqName"_FreqTable_"$i".pdf
     ((i++))
done
