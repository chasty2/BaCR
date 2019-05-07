#!/bin/bash

## cpPieChart: a helper script for the BaCR pipeline to copy the
## pie chart from CRISPResso analyses to ProjectID/PieCharts/, a directory
## structure created with bcp.sh

## written by Cody Hasty in vim on Ubuntu 16.04 LTS on 5/3/2019

## Command line input: cpPieChart.sh projectID fastq

fastqName=$(basename $2 .fastq.gz)
if [ -e $1/Analyses/CRISPResso_on_$fastqName*/*_pie_chart.pdf ]    
then
    echo "copying $fastqName pie-chart to $1/PieCharts/"
    cp $1/Analyses/CRISPResso_on_$fastqName*/*_pie_chart.pdf $1/PieCharts/"$fastqName"_PieChart.pdf
fi


