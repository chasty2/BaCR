#!/bin/bash

#
# bcp: basemount cp
#
# a bash script to copy .fastq files from basemount (a tool to mount one's
# basespace account as a GNU/Linux file system) to a place specified by the 
# user, in bulk, organized by Project ID and Forward/Reverse read. bcp
# puts Illumina next-generation sequencing data in a format that can easily
# be used for subsequent data analysis

# Written by Cody Hasty in vim on Ubuntu 18.04 LTS on 1/7/2019

# Flags: 
#   -p, Projects: bcp will cp .fastq files from a folder in the Projects directory
#   -r, Runs: bcp will cp .fastq files from a folder in the Runs directory
#   NOTE: the runs and projects folders are ordered differently, so it is important to 
#   specify 

# example: bcp -r directory_name projID_1 projID_2 ... projID_n

#--------------------------------------------------------------------------

# build_fastq_directory: mkdir a folder for each project ID with child 
# directories for forward and reverse reads (R1,R2)

function build_fastq_directory ()
{
    for projectID in ${@:3}
    do
        mkdir $projectID
        mkdir $projectID/R1
        mkdir $projectID/R2
        mkdir $projectID/PieCharts
        mkdir $projectID/Analyses
        mkdir $projectID/FreqTables
    done
}

#--------------------------------------------------------------------------

# cp_fastq_files: use cp to copy fastq files from their current destination
# to the directory made with build_fastq_directory. accepts $fastq and 
# $projectID as $1 and $2, respectively

cp_fastq_files()
{
    case $1 in
        *"$2"*R1*.fastq.gz)
            echo copying "$1" to "$2"/R1/
            cp $1 $2/R1/
        ;;
        *"$2"*R2*.fastq.gz)
            echo copying "$1" to "$2"/R2/
            cp $1 $2/R2/
        ;;
    esac
}

#--------------------------------------------------------------------------

# cp_from_Runs: finds .fastq files according to the directory structure of the Runs
# folder and copies them to the proper directory using cp

function cp_from_Runs () 
{
    for index in $2/Properties/Output.Samples/*
    do
        for fastq in $index/Files/*
        do
            for projectID in ${@:3}
            do
                cp_fastq_files $fastq $projectID
            done
        done
    done
}

#--------------------------------------------------------------------------

# cp_from_Projects: finds .fastq files according to the directory structure
# of the Projects folder and copies them to the proper directory using cp

function cp_from_Projects ()
{
    for sampleFolder in $2/Samples/*
    do
        for fastq in $sampleFolder/Files/*
        do
            for projectID in ${@:3}
            do
                cp_fastq_files $fastq $projectID
            done
        done
    done
}

## MAIN ##------------------------------------------------------------------

build_fastq_directory $@
if [ $1 = "-r" ]
then
    cp_from_Runs $@
elif [ $1 = "-p" ]
then
    cp_from_Projects $@
fi

