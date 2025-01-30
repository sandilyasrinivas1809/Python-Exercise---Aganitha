# Python-Exercise-Aganitha
### Content
* [Overview](#overview)
* [Installation](#installation)
* [Usage](#usage)
* [Process Flow](#process-flow)
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

