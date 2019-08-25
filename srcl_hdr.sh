#!/bin/bash

## srcl_hdr.sh: Single-Read HDR CRISPResso Loop
## written by Cody Hasty in vim on Ubuntu 16.04 LTS on 5/3/2019

## part of the BaCR pipeline, srcl_hdr.sh reads input from command line, 
## runs CRISPResso single-read hdr analysis, and copies the summary
## pie-chart to the ProjectID/PieCharts folder, using the directory 
## structure created by bcp.sh

## Command Line input:
## srcl_nhej.sh projectID R1/R2 amplicon guide hdr_sequence

for fastq in $1/$2/*
do
    CRISPResso -r1 $fastq -a $3 -g $4 -e $5 -o $1/Analyses/
    cpPieChart.sh $1 $fastq
    cpFreqTable.sh $1 $fastq
done
