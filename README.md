# Python-Exercise-Aganitha
### Content
* [Overview](#overview)
* [Installation](#installation)
* [Usage](#usage)
* [Folder Structure](#folder-structure)
----
### Overview
The PubMed Research Paper Extraction tool is used to extract the following key information using the PubMed API by taking into account the user's query as input -
a.	PubmedID: Unique identifier for the paper.
b.	Title: Title of the paper.
c.	Publication Date: Date the paper was published.
d.	Non-academic Author(s): Names of authors affiliated with non-academic institutions.
e.	Company Affiliation(s): Names of pharmaceutical/biotech companies.
f.	Corresponding Author Email: Email address of the corresponding author

Users have an option to add input the number of research papers from which tthey want to extract this information.
### Installation
This tool depends on conda installation in system.

1. Clone this repository onto your system using git.
2. Run [setup.bat](/setup.bat) to complete setup. It will create a new conda environment.

|:warning: The tool requires python version 3.13.1 to successfully run.|
|----|

### Usage
The user can directly use [run.bat](/run.bat) to run the tool. The batch file activates the environment created in the setup phase and executes the tool.

### Folder Structure
1. The root folder contains the following files:
    - .gitignore: contains the list of files/folders that should not be pushed to GitHub
    - environment.yml: Contains all the setup configuration for running the code
    - main.py: The main python file which will be run while the tool is triggered. It will call the necessary backend scripts.
    - requirements.txt: The required libraries and their versions.

2. src folder: This folder contains the backend python codes which will are imported in the main.py file
    - attribute_extraction.py: Contains different functions to extract the required information
    - log.py: Custom logger file to understand the runs.

Once any user runs the tool, two new folders will be created automatically:
- logs: This folder will keep the logs of all the runs.
- output: If the user wants to save the data into csv, the data will be stored in this folder.