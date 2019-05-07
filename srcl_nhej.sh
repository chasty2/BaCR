#!/bin/bash

## srcl_nhej.sh: Single-Read NHEJ CRISPResso Loop
## written by Cody Hasty in vim on Ubuntu 16.04 LTS on 5/3/2019

## part of the BaCR pipeline, srcl_nhej.sh reads input from command line, 
## runs CRISPResso single-read NHEJ analysis, and copies the summary
## pie-chart and allele frequency table to the ProjectID/PieCharts
## folder and FreqTables folder, using the directory  structure created
## by bcp.sh

## Command Line input:
## srcl_nhej.sh projectID R1/R2 amplicon guide

for fastq in $1/$2/*
do
    CRISPResso -r1 $fastq -a $3 -g $4 -o $1/Analyses/
    cpPieChart.sh $1 $fastq
    cpFreqTable.sh $1 $fastq
done
