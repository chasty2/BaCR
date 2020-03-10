## Sample Naming

The BaCR pipeline relies on the naming of samples for the correct sorting and analysis of each sample. The scripts
look for two substrings within the name of each sample: A project ID and a guide ID. The project ID denotes a project,
each sample in a given project. The guide ID denotes the guide RNA used. There should be one guide ID per expected mutation 
outcome.

## Analysis Organization

BaCR will generate one folder per project, and a subfolder for each mutation outcome within that project

## Template Parameters

You only need one entry per expected mutation outcome

Projects: Project ID. There can be duplicates to allow multiple guide IDs. One per project
GuideNames: Guide ID. There should be one per mutation outcome. This entry can be left blank if
    there is only one guide used in a project
R1/R2/PE: denotes forward, reverse strand, and/or paired-end analysis. There can be multiple 
    specifications separated by a comma, a folder will be created for each analysis (example: R1,PE)
Amplicon: The amplicon used in a given sample. Note that for R1 and R2 analyses, the first/last 150bp
    of this entry will be used
GuideSeq: The guide RNA(s) used for a given sample. Note that multiple guides can be specified, separated
    by a comma
HDR: The expected HDR sequence, if any
CR2_Params: Any additional parameters to append to the call to CRISPResso2 from command line for each sample

