
# PCGC Curation Ingest Package

## Study KF ID - SD_PREASA7S

## Description

This ingest package contains the necessary code needed to generate the
curation tables that will be given to a curator to fill in. 

It includes:

- `curation_package` - ingest package responsible for pulling all PCGC phenotype
   and diagnosis, merging it into one table
- `curation_package/scripts` - a script to generate the 2 curation tables

### Input - Data
The input data includes all phenotypes and diagnoses from:

- PCGC (`SD_PREASA7S`)
- PCGC/King cohort in INCLUDE (`SD_Z6MWD3H0`). 

Specifically the data types are:

- Cardiac abnormalities
- Non-cardiac findings
- Karyotype abnormalities
- Diagnoses

### Run
```
> kidsfirst ingest d3b_ingest_packages/packages/PCGC/curation_package --no_validate  --stages=et
> python d3b_ingest_packages/packages/PCGC/curation_package/scripts/generate_curation_tables.py
```
### Output - Curation Tables

#### participant_condition_curation.csv

The table of unique condition (phenotype/diagnosis) terms in PCGC study

#### participant_condition_free_text_curation.csv

The table of unique condition (phenotype/diagnosis) terms and associated free text values in PCGC study

