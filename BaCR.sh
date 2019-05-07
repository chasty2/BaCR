#!/bin/bash

## BaCR: Basemount-CRISPResso pipeline
## first, uses bcp.sh to copy amplicon NGS files from Basespace. Then it
## reads in data from a .csv file and creates an array containing all 
## the info necessary to run CRISPResso on the fastq files corresponding
## to a given project_guide. Requires csvkit

## written by Cody Hasty in vim on Ubuntu 16.04 LTS on 5/3/2019

## Command line input: BaCR.sh -r/-p basemount_dir input.csv

#-------------------------------------------------------------------------

## remove the quotes from the beginning and end of each string in the csv,
## but only if they are present. Important if multiple guides are specified

function removeQuotes 
{
    ## remove beginning quote
    local temp="$1"
    temp="${temp#\"}"
    ## remove end quote
    temp="${temp%\"}" 
    echo "$temp"
}

#-------------------------------------------------------------------------

## uses csvkit to extract data from the csv file and prepares it for entry
## into each projectIDarray, respectively

## populateArray input: projectID loopcounter input.csv

function populateArray
{
    local tempArray=($(csvgrep -c projectID -m $1 $3 | csvcut -c $2))
    local tempArrayUnit=($(removeQuotes ${tempArray[@]:1}))
    echo $tempArrayUnit
}

#-------------------------------------------------------------------------

## runCRISPRessoLoop determines which crispresso analysis to run for a given
## set of fastq files, and runs the script corresponding to that analysis

# runCRISPRessoLoop input: projectID R1/R2/PE amplicon guide(s) HDR

function runCRISPRessoLoop
{
    if [ $2 == "PE" ]
    then
        if [ -z $5 ]
        then
            pecl_nhej.sh $1 $2 $3 $4
        else
            pecl_hdr.sh $@
        fi
    elif [ $2 == "R1" ] || [ $2 == "R2" ]
    then
        if [ -z $5 ]
        then
            srcl_nhej.sh $1 $2 $3 $4
        else
            srcl_hdr.sh $@
        fi
    else    
        echo "invalid entry in R1/R2/PE for $1"
        sleep 3
    fi
}
#-------------------------------------------------------------------------


## MAIN ##

# create array for bcp
projectList=($(csvcut -c projectID $3))
bcp.sh $1 $2 ${projectList[@]:1}

# for each projectID, create projectIDarray and run analysis 
# for each fastq in the set
for projectID in ${projectList[@]:1}
do
    for i in {1..5}
    do
        projIDarray[i]=$(populateArray $projectID $i $3)
    done
    runCRISPRessoLoop ${projIDarray[@]}
done

