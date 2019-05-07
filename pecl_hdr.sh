#!/bin/bash

## Command Line input: projectID R1/R2/PE amplicon guide hdr

for fRead in $1/R1/*
do
    fReadname=$(basename $fRead _L001_R1_001.fastq.gz)
    rRead=$1/R2/$fReadname*
    echo $fReadname
    echo $rRead
    CRISPResso --max_paired_end_reads_overlap 150 -r1 $fRead -r2 $rRead -a $3 -g $4 -e $5 -o $1/Analyses/
    cpPieChart.sh $1 $fRead
    cpFreqTable.sh $1 $fRead
done

