<p align="center">
  <img src="docs/img/logo.png" alt="D3b Ingest Packages" width="660px">
</p>


# 👋 Welcome

Hi! Thank you for visiting this repo. In short, the main purpose of this repo
is to store and version control the ingest packages (bundles of data wrangling code) 
for each unique dataset that must be ingested into D3b or external systems.  

The repo also has a nifty Github workflow that runs the ingest package for 
each pull request and then creates an "ingest data portal" where people can 
explore the cleaned data as it is being developed.

![Workflow Diagram](docs/img/diagram.png)

## Background
Most of our datasets contain clinical data from research studies in the 
[NIH Kids First Program](https://kidsfirstdrc.org/)
and need to be ingested into the [Kids First Dataservice](https://github.com/kids-first/kf-api-dataservice)
or [Kids First FHIR Dataservice](https://github.com/kids-first/kf-api-fhir-service).

### Datasets
These datasets consist of many (usually 10+) messy tabular files that have to be 
cleaned up, merged, and transformed before they can be ingested into our systems.

### Ingest
Almost every dataset is a "snowflake" - has a different format and content than
the others. This means we can't just write one bit of ETL code and run it to 
ingest every dataset. The [Kids First Ingest Library](https://github.com/kids-first/kf-lib-data-ingest) 
helps us with this problem. 

The ingest library is a Python library that enables us to write 
data wrangling and ingest code in a standard way for these snowflake datasets
and run this code to ETL the datasets into various downstream systems. 

### 💡 Read First
If you are unfamiliar with this library or the term "ingest package", head on
over to the [Kids First Ingest Library documentation](https://kids-first.github.io/kf-lib-data-ingest/)
to learn more before moving forward.

# 👩‍💻 TODO - Quick Start 

## Setup Dev Environment
- Create virtualenv
- Install requirements
- See More details for additional setup steps if you want to run the full 
ingest pipeline locally

## Development Workflow

### Local Development
- Create a branch
- Make change
- Dry run ingest / run ingest locally
- Update run.yaml
- Commit locally

### Push Code to Github
- Push code to github

### View Results
- PR label
- Github workflow log

# 👩‍💻 ⚡️ Advanced 

- How to run docker-compose to setup and run the full ingest pipeline locally

# Resources

 - Kids First Help Center

