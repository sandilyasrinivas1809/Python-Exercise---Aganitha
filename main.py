#==============================================================================
# Importing the modules
#==============================================================================

import xml.etree.ElementTree as ET
from tqdm import tqdm
from src.log import debug_logger,normal_logger
from src.attribute_extraction import fetch_pubmed_ids,fetch_pubmed_details,fields_extraction,save_data_to_file
import sys
import argparse  

# Defining the command line arguments
parser = argparse.ArgumentParser(usage = "Please enter the search query and the number of relevant research papers to be extracted from PubMed API.")  

#giving the user an option to run in debug mode if needed
parser.add_argument('-d', '--debug', action = 'store_true', help = 'Enable Debug mode') 

#giving the user an option to enter the file name if needed 
parser.add_argument('-f', '--file',  help = 'Specify a file name')  
  
args = parser.parse_args()  

if args.file:
    print(f"File name : {args.file}\n")  

if args.debug:  
    logging = debug_logger()
    print("Debug mode is enabled. You will see logs of the current run on the terminal.")  
else:
    logging = normal_logger()


def main() -> None:
    """
    Main function to execute the tool. 
    Takes PubMed search query and number of papers to extract as user input.
    Parses each paper to extract required information and saves the data to excel if the user provides file name.
    """
    query = input("Please enter PubMed search query below.\nExample queries are:\n1.COVID-19 vaccine efficacy\n2.Diabetes treatment and management\
                   \n3.CRISPR gene editing in biotechnology\n")

    number_of_papers_input = int(input("Enter the number of research paper information you would like to extract. By default it will extract information from 20 papers.Max value is 10,000: "))
    pmids = fetch_pubmed_ids(query,number_of_papers_input)
    if len(pmids) == 0:
        print("Please check your input query")
        sys.exit()
    else:
        logging.info(f"Found {len(pmids)} papers.")
    filtered_data = []
    for pmid in tqdm(pmids):
        logging.info(f"Started processing the paper with ID: {pmid}")
        xml_data = fetch_pubmed_details(pmid)
        article_data = fields_extraction(xml_data)
        logging.info(f"Completed processing the paper with ID: {pmid}")
        filtered_data.append(article_data)
    final_data = save_data_to_file(filtered_data,args.file)
    if args.file:
        print("File Saved successfully in output folder")
    else:
        print(final_data)

if __name__ =="__main__":
    main()
