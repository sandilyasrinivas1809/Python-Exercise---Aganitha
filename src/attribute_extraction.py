#==============================================================================
# Importing the modules
#==============================================================================

import requests
import pandas as pd
pd.set_option('display.max_rows', 20)
import os
import re
import xml.etree.ElementTree as ET
from tqdm import tqdm
from src.log import debug_logger

logging = debug_logger()

OUTPUT_FOLDER_PATH = r"output"
OUTPUT_FOLDER = rf"{OUTPUT_FOLDER_PATH}"
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

def fetch_pubmed_ids(query:str,max_papers:int = 20) -> list:
    """
    Fetch PubMed IDs for the given query.
    Parameters
    ----------
    query : str
        Input query provided by the user.

    Returns
    -------
    id_list : list
        List of research paper ids.

    """
    if max_papers > 10000:
        max_papers = 10000
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json","retmax" : max_papers}
    response = requests.get(base_url, params=params)
    data = response.json()
    id_list = data['esearchresult']['idlist']
    return id_list

def fetch_pubmed_details(pmid:str) -> ET:
    """
    Fetch details of a PubMed article by ID in XML format.
    Parameters
    ----------
    pmid : str
        Research paper id.

    Returns
    -------
    resp : ET(XML)
        Content of the paper.

    """
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": pmid}
    response = requests.get(base_url, params=params)
    resp = ET.fromstring(response.content)
    return resp

def fields_extraction(xml_data:ET) -> dict:
    """
    Extract required data from PubMed XML.
    Parameters
    ----------
    xml_data : ET(XML)
        Content of the paper in XML format.

    Returns
    -------
    attribute_dict : JSON
        Required attributes.

    """
    root = xml_data
    # Extract PubMed ID
    try:
        pubmed_id = root.find(".//PMID").text
    except AttributeError:
        pubmed_id = "ID not present"
    except Exception as e:
        logging.info(e)
        pubmed_id = "Could not extract"

    try:
        title = root.find(".//ArticleTitle").text
    except AttributeError:
        title = "Title not present"
    except Exception as e:
        logging.info(e)
        title = "Could not extract"

    try:
        pub_date = root.find(".//ArticleDate")
    except AttributeError:
        pub_date = "Date not present"
    except Exception as e:
        logging.info(e)
        pub_date = "Could not extract"

    if pub_date is not None:
        pub_date = f"{pub_date.find('Year').text}-{pub_date.find('Month').text}-{pub_date.find('Day').text}"
    else:
        pub_date = "N/A"
    # Extract Authors and Affiliations
    non_academic_authors = []
    company_affiliations = set()
    corresponding_author_email = ""
    for author in root.findall(".//Author"):
        try:
            last_name = author.find("LastName").text
        except AttributeError:
            last_name = "Last name is not present"
        except Exception as e:
            logging.info(e)
            last_name = "Could not extract"

        try:
            fore_name = author.find("ForeName").text
        except AttributeError:
            fore_name = "First name is not present"
        except Exception as e:
            logging.info(e)
            fore_name = "Could not extract"
            
        if "not present" or "Could not extract" in fore_name:
            full_name = f"{last_name}"
        elif "not present" or "Could not extract" in last_name:
            full_name = f"{fore_name}"
        else:
            full_name = f"{fore_name} {last_name}"
             
        try:
            affiliations = author.findall(".//Affiliation")
        except AttributeError:
            affiliations = "Affiliations is not present"
        except Exception as e:
            logging.info(e)
            affiliations = "Could not extract"

        if "not present" or "Could not extract" not in affiliations:
            for aff in affiliations:
                aff_text = aff.text
                if "Therapeutics" in aff_text or "Pharmaceuticals" in aff_text or "Biotech" in aff_text:
                    non_academic_authors.append(full_name)
                    company_affiliations.add(aff_text)
                if "@" in aff_text:
                    pattern = r"Electronic address:\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})"
                    match = re.search(pattern, aff_text)
                    if match:
                        email = match.group(1)
                    else:
                        email = 'Not found'
                    corresponding_author_email = email
                
    attribute_dict = { "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ', '.join(non_academic_authors) if non_academic_authors else 'None',
            "Company Affiliation(s)": ', '.join(company_affiliations) if company_affiliations else 'None',
            "Corresponding Author Email": corresponding_author_email if corresponding_author_email else 'Not found'
        }

    return attribute_dict

def save_data_to_file(data:list,file_name:str = "") -> pd.DataFrame:
    """
    Save the data to required output file
    Parameters
    ----------
    data:list
        List which contains extracted attribute data for the specified number of papers 

    file_name:str
        Name of the output file
    
    Returns
    -------
    attribute_dict : JSON
        Required attributes.
    """
    final_data = pd.json_normalize(data)
    if file_name:
        output_file_name = f"{OUTPUT_FOLDER}/{file_name}" 
        print(output_file_name)
        if ".xlsx" in file_name:
            final_data.to_excel(output_file_name,index = False)
        elif ".csv" in file_name:
            final_data.to_csv(output_file_name,index = False)
        else:
            final_data.to_csv(f"{output_file_name}.csv",index = False)
    return final_data