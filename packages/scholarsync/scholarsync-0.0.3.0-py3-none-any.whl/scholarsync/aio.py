from itertools import combinations
from Bio import Entrez
import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urlparse, urljoin
import os
import hashlib
import shutil
from datetime import datetime
from PyPDF2 import PdfReader
from Bio import Medline
import xml.etree.ElementTree as ET
import subprocess
import sys
import os
import habanero
from habanero import cn
import json









"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""-----------------------------------------------------------------------------------------------"""
#  Help Functions
"""-----------------------------------------------------------------------------------------------"""

def entry_point_help():
    def encapsulated_root_help():

        def extract_entry_point_content(file_path, entry_point):
            with open(file_path, 'r') as file:
                content = file.read()
                pattern = f'<{entry_point}>(.*?)</{entry_point}>'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    return match.group(1)
                else:
                    return None

        def export_help(file_path):
            while True:
                export_dir = input("Enter the directory path for exporting help content (type 'cancel' to cancel): ")
                if export_dir.lower() == 'cancel':
                    print("Operation canceled.")
                    return
                elif os.path.isdir(export_dir):
                    break
                else:
                    print("Invalid directory path. Please enter a valid directory path.")

            export_file_path = os.path.join(export_dir, "the_help.txt")
            with open(file_path, 'r') as file:
                with open(export_file_path, 'w') as export_file:
                    export_file.write(file.read())
            print(f"Help content exported to {export_file_path}")

        # Accept file path from user
        def get_help_file_path():
            module_dir = os.path.dirname(__file__)  # Get the directory of the current module
            help_file_path = os.path.join(module_dir,'data', 'help.txt')
            return help_file_path

        file_path = get_help_file_path()

        while True:
            action = input("Choose an action (export_help, entry_point_all, or enter an entry point; type 'quit' to exit): ")
            if action.lower() == 'quit':
                break
            elif action.lower() == 'export_help':
                export_help(file_path)
            elif action.lower() == 'entry_point_all':
                with open(file_path, 'r') as file:
                    print("Content of entire file:")
                    print(file.read())
            else:
                content = extract_entry_point_content(file_path, action)
                if content:
                    print(f"Content of {action}: {content}")
                else:
                    print(f"No content found for {action}")

    encapsulated_root_help()






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""








"""-----------------------------------------------------------------------------------------------"""
# The Pubmed Querying System function entry_point_01
"""-----------------------------------------------------------------------------------------------"""


# Define functions from the script 01  The Pubmed Querying System
#
#
#

def entry_point_01():
    print(f" Hi, very soon we are going to dive into mess of literature mining, Beware ! ")
    encasulated_advanced_pubmed_paper_counter()
    entry_point_01A()   # cahined to entry_point_01A, The Manual Filter

def encasulated_advanced_pubmed_paper_counter():
    from itertools import combinations
    from Bio import Entrez

    def construct_query(terms):
        return ' AND '.join(terms)

    def search_and_store_papers(query_terms, filename,default_search_location, threshold, start_date=None, end_date=None):
        try:
            # Split query terms into individual components
            terms = []
            for term in query_terms:
                if '[' in term and ']' in term:
                    # Term contains explicit field tag, use as is
                    terms.append(term)
                else:
                    # Term does not contain field tag, treat as regular term with default search location (tiab)
                    terms.append(f'{term}[{default_search_location}]')
            # Generate all possible combinations of query terms
            combinations_list = []
            for r in range(1, len(terms) + 1):
                combinations_list.extend(combinations(terms, r))

            total_combinations = len(combinations_list)
            print(f"Total combinations to search: {total_combinations}")

            # Initialize BioPython
            Entrez.email = "your@email.com"  # Set your email here

            # Search and store total number of hits for each combination
            with open(filename, 'w') as file:
                file.write(f"Original Query Terms: {' '.join(query_terms)} \n\n")
                for index, combination in enumerate(combinations_list, start=1):
                    query = construct_query(combination)
                    if start_date and end_date:
                        query += f" AND ({start_date}[Date - Entrez] : {end_date}[Date - Entrez])"

                    print(f"Searching combination {index}/{total_combinations}: {query}")
                    handle = Entrez.esearch(db="pubmed", term=query, retmax=threshold)
                    record = Entrez.read(handle)
                    handle.close()
                    total_hits = int(record["Count"])
                    file.write(f"Combination : {index}/{total_combinations}  ")
                    file.write(f" Query: {query}\n")
                    file.write(f"Total Hits: {total_hits}\n")
                    if total_hits < threshold:
                        id_list = record["IdList"]
                        file.write("PMIDs: " + ', '.join(id_list) + "\n\n")
                    else:
                        file.write("PMIDs: Not fetched (hit count exceeds threshold)\n\n")
            print("Search completed. Results stored in", filename)

        except Exception as e:
            print("An error occurred:", str(e))

    # Example usage
    #if __name__ == "__main__":
    def root_PubMed_search_query():
        try:
            query = input("Enter PubMed search query: ")
            threshold = input("Threshold : ") or 250
            threshold = int(threshold)
            default_search_location = input("Enter the search location (e.g., ti , ab or tiab): ") or "tiab"
            #its a location where to search if the terms dont have the location specified for search ti:tittle, ab : abstract, tiab : title abstract both
            output_file_pubmed_paper_query_name = "output_file_pubmed_paper_query.txt"
            #output_file_pubmed_paper_query = input("Enter output filename: ")
            start_date = input("Enter start date (optional, format YYYY/MM/DD): ")
            end_date = input("Enter end date (optional, format YYYY/MM/DD): ")
            query_terms = query.split(',')
            # Remove leading and trailing whitespace from each term and filter out empty strings
            query_terms = [term.strip() for term in query_terms if term.strip()]
            search_and_store_papers(query_terms, output_file_pubmed_paper_query_name,default_search_location,threshold, start_date=start_date, end_date=end_date)

        except Exception as e:
            print("An error occurred:", str(e))


    root_PubMed_search_query()
















"""-----------------------------------------------------------------------------------------------"""
# The Search Query manual filter function entry_point_01A
"""-----------------------------------------------------------------------------------------------"""

# Define the functions of the script 01A The Graph Maker
#
#
#

def entry_point_01A():
    print(" The Search Query filter \n")
    print(" This will be ugraded shortly ! \n")
    print(" As of now kindly feed the manually filtered pubmed IDs by saving them in file named as pipeline_1.txt in the working directory \n")
    print(" You are advised to run entry_point_09.option.1 The citation script function when you feel you DOI are now fully collected and filtered \n")

# Here is wish to make a sort of html based filtering with graphing utility, that will generate a file named as pipeline_1.txt contating a cenrral list of all the PubMed IDs.



"""-----------------------------------------------------------------------------------------------"""
# The Abstracts Retriver function entry_point_02
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the script 02 The Abstracts Retriver
# (checks pipeline_1.txt for automatic mode)
#
#

def entry_point_02(): # maybe in subsequent updates called by entry_point_01A
    print(" This Entry point is to attempt to fetch the abstracts for the PubMed IDs.  (checks pipeline_1.txt for automatic mode) \n")
    root_abs_downloader()
    entry_point_03()  # Chained to entry_point_04 Pubmed Full text downloader


initialser_counter = 0
no_abstracts_pmid = []  # List to store PubMed IDs for which no abstracts can be fetched
no_full_text_info = []   # List to store PubMed IDs and corresponding DOIs for which full text is not available
full_text_available_pmid = []  # List to store PubMed IDs for which full text is available

def fetch_abstracts(pmid_list, num_pmid):
    global initialser_counter
    Entrez.email = "your.email@example.com"  # Set your email address
    handle = Entrez.efetch(db="pubmed", id=pmid_list, rettype="medline", retmode="text")
    records = Medline.parse(handle)
    abstracts = []

    for record in records:
        print(f"Trying {initialser_counter} / {num_pmid} ")
        #print(f"Trying {initialser_counter} / {num_pmid}  {record} ")
        full_text = record.get('LID', 'N/A')  # Check if Full Text link is available
        if full_text == 'N/A':
            full_text = "Full text not available"
            doi = record.get('AID', 'N/A')
            no_full_text_info.append((record.get('PMID', 'N/A'), doi))  # Add PubMed ID and DOI to the list
        else:
            full_text = "Full text available"
            full_text_available_pmid.append(record.get('PMID', 'N/A'))  # Add PubMed ID to the list

        abstract = record.get('AB', 'N/A')
        if abstract == 'N/A':
            no_abstracts_pmid.append(record.get('PMID', 'N/A'))  # Add PubMed ID to the list

        doi = record.get('AID', 'N/A')  # Assign DOI or 'N/A' if not available
        initialser_counter += 1

        abstracts.append({
            'pmid': record.get('PMID', 'N/A'),
            'title': record.get('TI', 'N/A'),  # Retrieve article title ('TI' field)
            'abstract': abstract,
            'full_text': full_text,
            'doi': doi
        })

    return abstracts




def save_abstracts_to_xml(pmid_list, output_file):
    num_pmid = len(pmid_list)  # Get the number of PubMed IDs
    abstracts = fetch_abstracts(",".join(pmid_list), num_pmid)  # Pass pmid_list and num_pmid

    root = ET.Element("PubmedArticleSet")

    for idx, abstract_info in enumerate(abstracts, start=1):
        article = ET.SubElement(root, "PubmedArticle")
        medline_citation = ET.SubElement(article, "MedlineCitation", PMID=abstract_info['pmid'])

        article_title = ET.SubElement(medline_citation, "ArticleTitle")
        article_title.text = abstract_info['title']  # Set article title from retrieved data

        # Add full text availability information
        full_text = ET.SubElement(medline_citation, "FullTextAvailability")
        full_text.text = abstract_info['full_text']

        abstract_element = ET.SubElement(medline_citation, "Abstract")
        abstract_text = ET.SubElement(abstract_element, "AbstractText")
        abstract_text.text = abstract_info['abstract']  # Set abstract text from retrieved data

        # Add DOI if available
        doi = abstract_info.get('doi', 'N/A')
        if doi != 'N/A':
            doi_element = ET.SubElement(medline_citation, "DOI")
            doi_element.text = f"https://doi.org/{doi}"

        # Add numbering to each article
        article_number = ET.SubElement(article, "ArticleNumber")
        article_number.text = str(idx)

    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)

    print(f"Abstracts downloaded and saved to '{output_file}'")
    print(f"Number of PubMed IDs processed: {len(pmid_list)}")

def read_pmid_input():
    print(" Trying to fetch the abstracts for the PubMed IDs, checking for Pipeline mode")
    # Get the current directory
    current_directory = os.getcwd()
    # Define the file path
    input_pipeline_1 = os.path.join(current_directory, "pipeline_1.txt")

    if os.path.exists(input_pipeline_1):
        with open(input_pipeline_1, 'r') as file:
            if file.read(1):
                print(" Detected Pipeline input file, entering automatic mode ")
                user_input = input_pipeline_1
            else:
                print(" Detected Empty Pipeline input file, entering manual mode ")
                user_input = input("Enter PubMed IDs directly or specify a path to a text file: ").strip()

    else:
        print(" Can't Detect Pipeline input file, entering manual mode ")
        user_input = input("Enter PubMed IDs directly or specify a path to a text file: ").strip()
    pmid_list = []

    if user_input.lower().endswith('.txt'):
        # User provided a file path, read PubMed IDs from the file
        try:
            with open(user_input, 'r') as file:
                for line in file:
                    ids = [pmid.strip() for pmid in line.split(',') if pmid.strip()]
                    pmid_list.extend(ids)
        except FileNotFoundError:
            print(f"Error: File '{user_input}' not found.")
            return None
    else:
        # User provided PubMed IDs directly (comma-separated)
        pmid_list = [pmid.strip() for pmid in user_input.split(",") if pmid.strip()]

    # Count the number of PubMed IDs detected
    num_pmid = len(pmid_list)
    print(f"Total Number of PubMed ID detected {num_pmid}")

    return pmid_list, num_pmid

#if __name__ == "__main__":

def root_abs_downloader():
    pmid_list, num_pmid = read_pmid_input()

    if pmid_list:
        #output_path = input("Enter path to save the output XML file (e.g., /path/to/abstracts.xml): (optional)").strip()
        output_path = ""

        if output_path:
            output_file = output_path
        else:
            # If the file doesn't exist, create a new filename with a timestamp
            timestamp = time.strftime("%Y%m%d%H%M%S")
            output_file = f"abstracts_{timestamp}.xml"

        # Check if the provided output file path exists or not
        if not os.path.exists(output_file):
            # If the file doesn't exist, create a new filename with a timestamp
            timestamp = time.strftime("%Y%m%d%H%M%S")
            output_file = f"abstracts_{timestamp}.xml"

        save_abstracts_to_xml(pmid_list, output_file)

    # Save PubMed IDs with no abstracts to a file
    with open("no_abstracts_pmid.txt", "w") as abstracts_file:
        for pmid in no_abstracts_pmid:
            abstracts_file.write(pmid + "\n")

    # Save PubMed IDs and corresponding DOIs with no full text to a file
    with open("no_full_text_doi.txt", "w") as full_text_file:
        for pmid, doi in no_full_text_info:
            full_text_file.write(f"PubMed ID: {pmid}, DOI URL: https://doi.org/{doi}\n")

    # Save PubMed IDs with full text available to a file
    with open("full_text_available_pmid.txt", "w") as full_text_file:
        for pmid in full_text_available_pmid:
            full_text_file.write(pmid + "\n")




"""-----------------------------------------------------------------------------------------------"""
# The Full Text PubMed Retriver Function Entry_point_03
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the 03 script The full text PubMed retriver (pdf and HTML)
# This will not take consideration of what abstract downloader says about the full text availibility, we can use that for checking and establishing the consensus. This will use the Final starter input (pipeline_1.txt)
# (checks pipeline_1.txt for automatic mode),
# This suports resume capabilities

def entry_point_03(): # called by entry_point_02
    print(" This entry point is to attempt full text download of PDF and HTML from the PubMed IDs, (checks pipeline_1.txt for automatic mode) and supports resume capabilities. \n")
    encapsulated_root_check_pre_existing_file_pubmed_full_text_downloader()
    #entry_point_04() # chained to call entry point 04 , to fetch the PMCID and the DOIs for the PubMed IDs (no full text available )

def encapsulated_root_check_pre_existing_file_pubmed_full_text_downloader():
    def fetch_articles(feeder_pubmed_ids, filename, total_ids):
        Entrez.email = 'your_email@example.com'  # Provide your email here

        # Create a timestamped directory to store files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_directory = f"output_{timestamp}"
        os.makedirs(output_directory)  # Create the main output directory

        pdf_count = 0
        html_count = 0
        current_counter_initialiser = 0
        not_available_ids = 0


        for feeder_pubmed_id in feeder_pubmed_ids:
            pubmed_id_no_full_text = ""
            try:
                handle = Entrez.efetch(db="pubmed", id=feeder_pubmed_id, rettype="medline", retmode="xml")
                record = Entrez.read(handle)

                # Extract the PMCID from the record
                pmcid = record['PubmedArticle'][0]['PubmedData']['ArticleIdList'][1]

                # Check if full text is available for the article
                current_counter_initialiser += 1
                print(f"Trying {current_counter_initialiser}/{total_ids} PubMed ID: {feeder_pubmed_id}  \n")
                if pmcid.startswith('PMC'):
                    print(f"      Downloading full-text for PubMed ID: {feeder_pubmed_id} (PMCID: {pmcid})")

                    # Create subdirectory for the current PubMed ID
                    subdir_path = os.path.join(output_directory, feeder_pubmed_id)
                    os.makedirs(subdir_path)

                    # Download PDF
                    pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
                    download_file(pdf_url, os.path.join(subdir_path, f"{feeder_pubmed_id}_fulltext.pdf"))
                    pdf_count += 1

                    # Download HTML if available
                    html_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/"
                    download_file(html_url, os.path.join(subdir_path, f"{feeder_pubmed_id}_fulltext.html"))
                    html_count += 1

                else:
                    print(f"      Full-text not available for PubMed ID: {feeder_pubmed_id} \n")
                    not_available_ids += 1
                    pubmed_id_no_full_text = feeder_pubmed_id


                # Add a delay between requests to avoid rate limiting
                time.sleep(1)  # Pause for 1 second before next request

            except Exception as e:
                print(f"Error processing PubMed ID {feeder_pubmed_id}: {e}")

            remove_word_from_file(filename, feeder_pubmed_id )
            update_pubmed_no_full_text(pubmed_id_no_full_text)

        summary(pdf_count,html_count,not_available_ids, total_ids)


    def download_file(url, filepath):
        try:
            print(f"      Downloading from URL: {url}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            response = requests.get(url, headers=headers, allow_redirects=True)
            final_url = response.url  # Get the final URL after following redirects
            print(f"      Final URL after redirects: {final_url}")
            print(f"      HTTP Status Code: {response.status_code}")

            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"      Downloaded: {filepath} \n")
            else:
                print(f"      Failed to download from {url} (Status Code: {response.status_code})")

        except requests.exceptions.RequestException as e:
            print(f"      Error downloading from URL {url}: {e}")


    def remove_word_from_file(file_path, feeder_pubmed_id):
        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()
        # Remove the word from the content
        modified_content = content.replace(feeder_pubmed_id, '')

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(modified_content)


    def update_pubmed_no_full_text(pubmed_id_no_full_text):
        pubmed_no_full_text_file = "pubmed_no_full_text_file.txt"
        try:
            # Try to open the file in append mode
            with open(pubmed_no_full_text_file, 'a') as file:
                # Add the string to the file on a new line
                file.write('\n' + pubmed_id_no_full_text)
        except FileNotFoundError:
            # If the file doesn't exist, create it and add the string
            with open(pubmed_no_full_text_file, 'w') as file:
                file.write(pubmed_id_no_full_text)


    def summary(pdf_count,html_count,not_available_ids, total_ids):
        # Print summary
        print(f"\nSummary:")
        print(f"Total number of input PubMed IDs: {total_ids}")
        print(f"Number of PubMed IDs for which PDFs were downloaded: {pdf_count}")
        print(f"Number of PubMed IDs for which HTML files were downloaded: {html_count}")
        print(f"Number of PubMed IDs for which full text was not available: {not_available_ids}")
        print(f"List of PubMed IDs with no full text available saved to 'not_available_ids.txt'")


    def remove_pubmed_no_full_text_file_txt():
        try:
            os.remove("pubmed_no_full_text_file.txt")
            print(f"File pubmed_no_full_text_file.txt successfully removed.")
        except OSError as e:
            print(f"Error (Previous file 'pubmed_no_full_text_file.txt' might not be existing ): {e.strerror} \n")

    def write_pubmed_ids_to_secondary_input_file(pubmed_ids, filename, total_ids):
        feeder_pubmed_ids = []
        with open(filename, 'w') as file:
            for pubmed_id in pubmed_ids:
                file.write(pubmed_id + '\n')
                feeder_pubmed_ids.append(pubmed_id)

        print(f"Total number of remaining input PubMed IDs : {total_ids}")
        fetch_articles(feeder_pubmed_ids, filename, total_ids)
        return feeder_pubmed_ids

    def get_id(ids_input, filename):
        if os.path.isfile(ids_input):  # If input is a file
            with open(ids_input, 'r') as file:
                pubmed_ids = []
                for line in file:
                    line_ids = line.strip().split(',')
                    line_ids = [id.strip() for id in line_ids if id.strip()]
                    pubmed_ids.extend(line_ids)
                    total_ids = len(pubmed_ids)
                write_pubmed_ids_to_secondary_input_file(pubmed_ids, filename, total_ids)
        else:  # If input is comma-separated IDs
            pubmed_ids = [id.strip() for id in ids_input.split(',')if id.strip()]
            total_ids = len(pubmed_ids)
            write_pubmed_ids_to_secondary_input_file(pubmed_ids, filename, total_ids)
    #    print(f"Total number of input PubMed IDs: {total_ids}")
        return pubmed_ids

    def root_check_pre_existing_file_pubmed_full_text_downloader():
        filename = "remaining_id.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                if file.read(1):
                    print("WARNING! Unfinished Download was found. If you don't restart now, it can't be resumed later. All previous progress will be safe.")
                    confirm_new_session = input("Do you want to resume the previous download? Type 'Y' or 'yes' to resume, or 'N' for 'no': ")
                    if confirm_new_session.lower() in ['y', 'yes']:
                        ids_input = filename
                    else:
                        print("Checking pipeline mode.")
                        if os.path.exists("pipeline_1.txt"):
                            with open("pipeline_1.txt", 'r') as file:
                                if file.read(1):
                                    confirm_new_session = input("Enter Pipeline Mode? Type 'Y' or 'yes' to enter, or 'N' for 'no': ")
                                    if confirm_new_session.lower() in ['y', 'yes']:
                                        remove_pubmed_no_full_text_file_txt()
                                        ids_input = "pipeline_1.txt"
                                    else:
                                        print(" Starting new session, entering full manual mode. ")
                                        remove_pubmed_no_full_text_file_txt()
                                        print("Entering full Manual mode, no remaining_id.txt and pipeline_1.txt was found, nor the script is in pipeline mode.")
                                        ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs: ")
                                    get_id(ids_input, filename)

                                else:
                                    remove_pubmed_no_full_text_file_txt()
                                    print("'pipeline_1.txt' might be empty, Entering full manual mode.")
                                    print("Entering full Manual mode, no remaining_id.txt was found, nor the script is in pipeline mode.")
                                    ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs: ")
                                get_id(ids_input, filename)

                        print("Started a new session, clearing remaining_id.txt.")
                        remove_pubmed_no_full_text_file_txt()
                        ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs: ")
                    get_id(ids_input, filename)

                else:
                    print("'remaining_id.txt' might be empty, checking pipeline mode.")
                    if os.path.exists("pipeline_1.txt"):
                        with open("pipeline_1.txt", 'r') as file:
                            if file.read(1):
                                confirm_new_session = input("Enter Pipeline Mode? Type 'Y' or 'yes' to enter , or 'N' for 'no': ")
                                if confirm_new_session.lower() in ['y', 'yes']:
                                    remove_pubmed_no_full_text_file_txt()
                                    ids_input = "pipeline_1.txt"
                                else:
                                    print(" Starting new session, entering full manual mode. ")
                                    remove_pubmed_no_full_text_file_txt()
                                    print("Entering full Manual mode, no remaining_id.txt and pipeline_1.txt was found, nor the script is in pipeline mode.")
                                    ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs: ")
                                get_id(ids_input, filename)

                            else:
                                remove_pubmed_no_full_text_file_txt()
                                print("'pipeline_1.txt' might be empty, Entering full manual mode.")
                                print("Entering full Manual mode, no remaining_id.txt was found, nor the script is in pipeline mode.")
                                ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs: ")
                            get_id(ids_input, filename)

                    else:
                        remove_pubmed_no_full_text_file_txt()
                        print("Entering Manual mode, no remaining_id.txt was found, nor the script is in pipeline mode.")
                        ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs: ")
                        get_id(ids_input, filename)

        elif os.path.exists("pipeline_1.txt"):
            print(" No remaing Downloads detected, found traces for pipeline mode : ")
                    #if os.path.exists("pipeline_1.txt"):
            with open("pipeline_1.txt", 'r') as file:
                if file.read(1):
                    confirm_new_session = input("Enter Pipeline Mode? Type 'Y' or 'yes' to enter, or 'N' for 'no': ")
                    if confirm_new_session.lower() in ['y', 'yes']:
                        ids_input = "pipeline_1.txt"
                        remove_pubmed_no_full_text_file_txt()
                    else:
                        print(" Pipeline mode file might be empty, proceding to manual mode. \n")
                        remove_pubmed_no_full_text_file_txt()
                        print("Entering full Manual mode, no remaining_id.txt was found, nor the script is in pipeline mode.\n")
                        ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs: ")
                    get_id(ids_input, filename)

                else:
                    remove_pubmed_no_full_text_file_txt()
                    print("Entering full Manual mode, no remaining_id.txt was found, nor the script is in pipeline mode.\n")
                    ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs:\n ")
                get_id(ids_input, filename)


        else:
            remove_pubmed_no_full_text_file_txt()
            print("Entering full Manual mode, no remaining_id.txt was found, nor the script is in pipeline mode.")
            ids_input = input("Enter PubMed IDs separated by commas or specify a text file containing the IDs: ")
            get_id(ids_input, filename)

    root_check_pre_existing_file_pubmed_full_text_downloader()



"""-----------------------------------------------------------------------------------------------"""
# The PMCID and the DOIs Retriver Function Entry_point_04
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the first script
# This entry point is to try to fetch the PMCID and the DOIs for the PubMed IDs. ( For which no full text was downloaded )
# It uses the file 'pubmed_no_full_text_file.txt' created by the entry point 03
#

def entry_point_04(): # called by entry_point_03
    root_fetch_pmc_and_DOI()
    entry_point_05() # chained to Entry Point 05, Url transformer

def root_fetch_pmc_and_DOI():
    print(" This entry point is to try to fetch the PMCID and the DOIs for the PubMed IDs. ( For which no full text was downloaded ) \n")
    # Check if pubmed_no_full_text_file.txt exists in the current directory
    input_file_path = 'pubmed_no_full_text_file.txt'
    if not os.path.exists(input_file_path):
        # If input.txt doesn't exist, ask the user for input
        print("File 'pubmed_no_full_text_file.txt' not found in current directory. Entering Manual Mode \n")
        input_ids = input("Enter File Path or PubMed IDs (comma-separated): \n ").strip()
    else:
        # Read PubMed IDs from input.txt
        input_ids = input_file_path

        if input_ids.endswith('.txt'):
            # Read PubMed IDs from file
            try:
                with open(input_ids, 'r') as file:
                    pubmed_ids = []
                    for line in file:
                        ids = line.strip().split(',') # this is line wise stripping can accept file with comma delimited multiple entries per line , last id dont require comma at the end
                        pubmed_ids.extend(ids)
            except FileNotFoundError:
                print(f"Error: File '{input_ids}' not found.")
                return
        else:
            # Split comma-separated IDs
            pubmed_ids = [id.strip() for id in input_ids.split(',')]

    choice = input("Include reasons for PubMed IDs with no PMCIDs found? (yes/no): ").strip().lower()
    include_reason = choice == 'yes'

    process_pubmed_ids(pubmed_ids, include_reason)


def get_pmcid(pubmed_id):
    # Function implementation...
    base_url = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
    params = {
        'ids': pubmed_id,
        'format': 'json'
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if 'records' in data and data['records']:
        record = data['records'][0]
        return record.get('pmcid', 'Not Found')
    elif 'status' in data and data['status'] == 'error':
        reason = data['message']
        return f'Not Found: {reason}'
    else:
        return 'Not Found: Unknown reason'


def get_doi_from_pubmed_id(pubmed_id):
    # Function implementation...
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        doi_tag = soup.find("meta", {"name": "citation_doi"})

        if doi_tag and doi_tag.get("content"):
            return doi_tag["content"]
        else:
            print(f"No DOI found for PubMed ID: {pubmed_id}")
    else:
        print(f"Failed to retrieve PubMed page for ID: {pubmed_id}")

    return None

def process_pubmed_ids(pubmed_ids, include_reason):
    # Function implementation...
    pmc_ids_found = []
    dois = []
    pmids_not_found = []
    pmids_no_doi = []

    total_pubmed_ids = len(pubmed_ids)  # Total number of PubMed IDs provided

    for index, pubmed_id in enumerate(pubmed_ids, start=1):
        pubmed_id = pubmed_id.strip()

        # Display current working PubMed ID's index and total count
        print(f"Processing PubMed ID {index}/{total_pubmed_ids}: {pubmed_id}")

        # Get PMC ID and print status
        pmcid = get_pmcid(pubmed_id)
        pmcid_status = f"Fetched: {pmcid}" if not pmcid.startswith('Not Found') else f"Not Fetched: {pmcid}"
        print(f"PubMed ID: {pubmed_id} - PMC ID Status: {pmcid_status}")

        if pmcid.startswith('Not Found'):
            if include_reason:
                reason_parts = pmcid.split(': ', 1)
                if len(reason_parts) > 1:
                    reason = reason_parts[1]
                else:
                    reason = 'Reason not available'
                pmids_not_found.append(f"{pubmed_id} - {reason}")
            else:
                pmids_not_found.append(pubmed_id)
        else:
            pmc_ids_found.append(pmcid)

        # Attempt to retrieve DOI and print DOI status
        doi = get_doi_from_pubmed_id(pubmed_id)
        doi_status = f"Fetched: {doi}" if doi else "Not Fetched"
        print(f"PubMed ID: {pubmed_id} - DOI Status: {doi_status}")

        if doi:
            dois.append(f"https://doi.org/{doi}")
        else:
            pmids_no_doi.append(pubmed_id)

    pmc_ids_count = len(pmc_ids_found)
    dois_count = len(dois)
    pmids_no_doi_count = len(pmids_no_doi)

    # Print summary
    print(f"Total PubMed IDs provided: {total_pubmed_ids}")
    print(f"PMC IDs retrieved: {pmc_ids_count}")
    print(f"DOIs retrieved: {dois_count}")
    print(f"PubMed IDs with no DOI retrieved: {pmids_no_doi_count}")

    # Write PubMed IDs with no DOI retrieved to a text file
    if pmids_no_doi:
        output_file_no_doi = 'pmids_no_doi.txt'
        with open(output_file_no_doi, 'w') as file:
            file.write("PubMed IDs with no DOI found:\n")
            for pmid in pmids_no_doi:
                file.write(f"{pmid}\n")
        print(f"PubMed IDs with no DOI found saved to '{output_file_no_doi}'.")

    # Write results to separate files
    if pmc_ids_found:
        output_file_found = 'pmc_ids_found.txt'
        with open(output_file_found, 'w') as file:
            file.write("Found PMCIDs:\n")
            for pmcid in pmc_ids_found:
                file.write(f"{pmcid}\n")
        print(f"Found PMCIDs saved to '{output_file_found}'.")

    if dois:
        output_file_dois = 'dois_found.txt'
        with open(output_file_dois, 'w') as file:
            file.write("Found DOIs:\n")
            for doi in dois:
                file.write(f"{doi} \n")
        print(f"Found DOIs saved to '{output_file_dois}'.")

    if pmids_not_found:
        if include_reason:
            output_file_not_found = 'pmids_not_found_with_reason.txt'
        else:
            output_file_not_found = 'pmids_not_found.txt'
        with open(output_file_not_found, 'w') as file:
            if include_reason:
                file.write("PubMed IDs with reasons for no PMCIDs found:\n")
            else:
                file.write("PubMed IDs with no PMCIDs found:\n")
            for item in pmids_not_found:
                file.write(f"{item}\n")
        print(f"PubMed IDs with {'reasons for ' if include_reason else ''}no PMCIDs found saved to '{output_file_not_found}'.")





"""-----------------------------------------------------------------------------------------------"""
# The URL trasformer Function Entry_point_05
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the fifth script
#
#
#

# Default URL prefixes if no file or interactive input is provided
DEFAULT_URL_PREFIXES = [
   "https://sci-hub.se",
   "https://sci-hub.3800808.com"
]

def entry_point_05(): # called by entry_point_04
    print(" This entry point is the bulk url transformer. \n")
    root_url_transformer()
    entry_point_06()  # Chained to entry_point_06 ,main_crawler_downloader 3rd party retriver


def root_url_transformer():
         # Transform PubMed IDs
        transformed_url_path = "dois_found.txt"
        if file_exists(transformed_url_path):
            print(f"The file '{transformed_url_path}' was found in the current directory. \n Entering Automatic mode ")
            pubmed_ids_path = transformed_url_path
            operation_choice = "prefix"
            url_prefixes_path = ""
            url_prefixes = DEFAULT_URL_PREFIXES  # Use default prefixes if no file path is expected

        if not file_exists(transformed_url_path):
            print(f"The file '{transformed_url_path}' was not found in the current directory.")
            # Prompt user for the file path
            transformed_url_path = input("Enter the path to the transformed URL file: ")
            pubmed_ids_path = transformed_url_path
            # Prompt for operation choice
            operation_choice = input("Choose operation ('prefix' to add prefixes, 'strip' to remove prefixes): ").strip().lower()
            while operation_choice not in ['prefix', 'strip']:
                print("Invalid operation choice. Please choose 'prefix' or 'strip'.")
                operation_choice = input("Choose operation ('prefix' to add prefixes, 'strip' to remove prefixes): ").strip().lower()

            # Determine URL prefixes based on user input
            url_prefixes_path = input("Enter the path to the URL prefixes file (leave blank if not using file): ")
            if url_prefixes_path:
                url_prefixes = read_file_lines(url_prefixes_path)
            else:
                url_prefixes = DEFAULT_URL_PREFIXES  # Use default prefixes if no file path is provided

        # Transform PubMed IDs based on operation choice
        transformed_ids = transform_pubmed_ids(pubmed_ids_path, operation_choice, url_prefixes)


def file_exists(file_path):
    return os.path.isfile(file_path)

def read_file_lines(file_path):
    # Function implementation...
    """Read lines from a file and return them as a list."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def transform_pubmed_ids(pubmed_ids_path, operation_choice, url_prefixes=None):
    # Read PubMed IDs from the file
    pubmed_ids = read_file_lines(pubmed_ids_path)

    # Determine URL prefixes to use
    if not url_prefixes:
        url_prefixes = DEFAULT_URL_PREFIXES  # Use default prefixes if none provided

    # Process each PubMed ID based on operation choice
    transformed_ids = []
    for pubmed_id_line in pubmed_ids:
        pubmed_id_line = pubmed_id_line.strip()
        if pubmed_id_line:  # Check if line is not empty
            if operation_choice == 'prefix':
                # Split IDs based on comma, space, or tab
                pubmed_ids_split = re.split(r'[,\s\t]+', pubmed_id_line)
                # Prefix each PubMed ID with URL prefixes
                for pid in pubmed_ids_split:
                    for prefix in url_prefixes:
                        transformed_ids.append(f"{prefix}/{pid}")
            elif operation_choice == 'strip':
                # Strip existing prefixes from PubMed IDs
                stripped_id = pubmed_id_line
                for prefix in url_prefixes:
                    if stripped_id.startswith(prefix):
                        stripped_id = stripped_id[len(prefix):].lstrip('/')
                        break  # Stop after stripping the first matching prefix
                transformed_ids.append(stripped_id)

     # Output file path
    output_file_path = "transformed_pubmed_ids.txt"

    # Write transformed IDs to output file
    write_transformed_ids(output_file_path, transformed_ids)

    print(f"Transformation completed. Transformed IDs saved in '{output_file_path}'.")

    return transformed_ids



def write_transformed_ids(output_file_path, transformed_ids):
    # Function implementation...
    """Write transformed IDs to an output file."""
    with open(output_file_path, 'w') as outfile:
        for transformed_id in transformed_ids:
            outfile.write(transformed_id + ',')


"""-----------------------------------------------------------------------------------------------"""
# The URL reverse transformer Function Entry_point_5A
"""-----------------------------------------------------------------------------------------------"""


# Define functions for entry point 5A
# This is a reverse url transformer for the DOIs having prefixes of the third party URL
#
#

def entry_point_5A(): #chained from entry_point_06(), main crawler downloader from the third party sources
    root_url_reverse_transformer()
    entry_point_07AUTO()  #chained back to entry_point_07, deduplicator script(functions)

def root_url_reverse_transformer():
         # Transform PubMed IDs
        transformed_url_path_5A = "urls_without_pdf.txt"
        if file_exists_5A(transformed_url_path_5A):
            print(f" The file '{transformed_url_path_5A}' was found in the current directory. Continuing Automatic mode ")
            pubmed_ids_path_5A = transformed_url_path_5A
            operation_choice_5A = "strip"
            url_prefixes_path_5A = ""
            url_prefixes_5A = DEFAULT_URL_PREFIXES  # Use default prefixes if no file path is expected

        transformed_ids_5A = transform_pubmed_ids_5A(pubmed_ids_path_5A, operation_choice_5A, url_prefixes_5A)


def file_exists_5A(file_path_5A):
    return os.path.isfile(file_path_5A)

def read_file_lines_5A(file_path_5A):
    # Function implementation...
    """Read lines from a file and return them as a list."""
    with open(file_path_5A, 'r') as file:
        lines_5A = file.readlines()
    return lines_5A

def transform_pubmed_ids_5A(pubmed_ids_path_5A, operation_choice_5A, url_prefixes_5A=None):
    # Read PubMed IDs from the file
    pubmed_ids_5A = read_file_lines_5A(pubmed_ids_path_5A)

    # Determine URL prefixes to use
    if not url_prefixes_5A:
        url_prefixes_5A = DEFAULT_URL_PREFIXES  # Use default prefixes if none provided

    # Process each DOI based on operation choice
    transformed_ids_5A = []
    for pubmed_id_line_5A in pubmed_ids_5A:
        pubmed_id_line_5A = pubmed_id_line_5A.strip()
        if pubmed_id_line_5A:  # Check if line is not empty
            if operation_choice_5A == 'strip':
                # Strip existing prefixes from PubMed IDs
                stripped_id_5A = pubmed_id_line_5A
                for prefix_5A in url_prefixes_5A:
                    if stripped_id_5A.startswith(prefix_5A):
                        stripped_id_5A = stripped_id_5A[len(prefix_5A):].lstrip('/')
                        break  # Stop after stripping the first matching prefix
                transformed_ids_5A.append(stripped_id_5A)

     # Output file path
    output_file_path_5A = "urls_without_pdf.txt"

    # Write transformed IDs to output file
    write_transformed_ids_5A(output_file_path_5A, transformed_ids_5A)

    print(f" Reverse Transformation completed. Stripped DOIs saved in '{output_file_path_5A}' \n.")

    return transformed_ids_5A

def write_transformed_ids_5A(output_file_path_5A, transformed_ids_5A):
    # Function implementation...
    """Write transformed IDs to an output file."""
    with open(output_file_path_5A, 'w') as outfile_5A:
        for transformed_id_5A in transformed_ids_5A:
            outfile_5A.write(transformed_id_5A.strip() + '\n')





"""-----------------------------------------------------------------------------------------------"""
# The Main Crawler Downloader Function Entry_point_06
"""-----------------------------------------------------------------------------------------------"""


# Define functions from the sixth script
# This is main crawler downloader from the third party sources
#
#

def entry_point_06(): # called by entry_point_06, url transformer
    root_main_crawler_downloader()
    entry_point_5A() #chained back to entry_point_07, deduplicator script(functions)

def root_main_crawler_downloader():
# Crawl and Download from URLs
        if os.path.exists('transformed_pubmed_ids.txt'):
            print("File transformed_pubmed_ids.txt found, entering automatic mode ")
            file_path = 'transformed_pubmed_ids.txt'
            with open(file_path, 'r') as file:
                urls = []
                for line in file:
                        line = line.strip()
                        urls.extend(line.split(','))
                #content = file.read().strip()  # Read the file content and strip leading/trailing whitespace
                #urls = content.split(',')      # Split the content by commas
                print("Total URLs:", len(urls))
            crawl_and_download(urls)




        else:
            print("File transformed_pubmed_ids.txt not found, entering manual mode ")
            input_mode = input("Enter '1' to input URLs directly, '2' to specify a file path containing URLs: ")

            if input_mode == '1':
            # Input multiple URLs directly (comma-delimited)
                urls = input("Enter comma-separated URLs: ").split(',')
                print("\n Total URLs:", len(urls))
                crawl_and_download(urls)
            elif input_mode == '2':
                file_path = input("Enter file path containing URLs: ")
                with open(file_path, 'r') as file:
                    urls = []
                for line in file:
                        line = line.strip()
                        urls.extend(line.split(','))
                    #content = file.read().strip()  # Read the file content and strip leading/trailing whitespace
                    #urls = content.split(',')
                        print("\n Total URLs:", len(urls))
                        crawl_and_download(urls)
            else:
                print("Invalid input mode. Please enter '1' or '2'.")
        exit()


def extract_base_url(url):
    # Function implementation...
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def extract_src_urls(soup):
    # Function implementation...
    src_urls = []

    # Find all elements that might contain 'src' attributes
    elements_with_src = soup.find_all(['iframe', 'embed', 'object', 'video', 'audio', 'source', 'img', 'script', 'link', 'division', 'div', 'a'])

    # Extract 'src' attributes from elements
    for element in elements_with_src:
        if element.has_attr('src'):
            src_urls.append(element['src'])

        # Check additional attributes like 'data-src' or 'href' for certain elements
        if element.name == 'script' and element.has_attr('src'):
            src_urls.append(element['src'])
        elif element.name == 'link' and element.has_attr('href'):
            src_urls.append(element['href'])
        elif element.name == 'a' and element.has_attr('href'):
            src_urls.append(element['href'])
        elif element.name == 'source' and element.has_attr('src'):
            src_urls.append(element['src'])

    return src_urls

def print_src_with_pdf(src_urls):
    pdf_urls = [url for url in src_urls if '.pdf' in url.lower()]

    print("\nList of 'src' attributes containing '.pdf':")
    for url in pdf_urls:
        print(url)

    return pdf_urls


def download_pdfs(pdf_urls, base_url):
    if not pdf_urls:
        print("No PDF files found.")
        return

    print("\nAttempting to download PDF files:")
    for url in pdf_urls:
        # Resolve relative URLs against the base URL
        full_url = urljoin(base_url, url)

        try:
            print(full_url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(full_url, headers=headers, stream=True)
            response.raise_for_status()

            # Extract filename from URL and append '.pdf' extension
            filename = full_url.split('/')[-1]
            if not filename.lower().endswith('.pdf'):
                filename += '.pdf'

            # Save PDF content to a file with the correct filename and extension
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Downloaded PDF: {filename}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading PDF from {full_url}: {e}")

def crawl_and_download(urls):
    total_urls = len(urls)
    pdf_urls_found = 0
    pdfs_downloaded = 0
    subcounter_nth_url = 0
    initialiser_no_pdf_url = 0
    urls_without_pdf = []


    for url in urls:

        subcounter_nth_url += 1
        print(f"\n Trying {subcounter_nth_url}/{total_urls} Of the Total Url Supplied:  {url} \n " )

        try:
            # Send a GET request to the URL
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad responses

            # Extract base URL from the current URL
            base_url = extract_base_url(url)
            print(f"     The Base Url detected was : {base_url}" )
            print(f"     Sleeping for 5 Seconds to allow page to load" )

            # Wait for 5 seconds to allow the page to load completely
            time.sleep(5)

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract all 'src' attributes from the HTML
            src_urls = extract_src_urls(soup)

            # Filter and collect 'src' attributes containing '.pdf'
            pdf_urls = [urljoin(base_url, src) for src in src_urls if '.pdf' in src.lower()]
            subcounter_total_pdf_url_in_this_link = len(pdf_urls)
            print(f"          Total Pdf Url detected in this page were : {subcounter_total_pdf_url_in_this_link}" )
            print("          The PDF URLs detected List is :")
            subcounter_initialiser_pdf_listing = 0
            for url in pdf_urls:
                subcounter_initialiser_pdf_listing += 1
                print(f"          {subcounter_initialiser_pdf_listing}/{subcounter_total_pdf_url_in_this_link} : {url} ")


            # Count PDF URLs found
            pdf_urls_found += len(pdf_urls)
            #print(f" Total Pdf Url detected in this page were : {pdf_urls_found}" )

            subcounter_nth_pdf_url = 0

            # Attempt to download PDF files using resolved URLs and base URL
            for pdf_url in pdf_urls:
                try:
                    subcounter_nth_pdf_url += 1
                    print(f"\n          Trying {subcounter_nth_pdf_url}/{subcounter_total_pdf_url_in_this_link}/{subcounter_nth_url}/{total_urls} : {pdf_url} " )
                    response = requests.get(pdf_url, headers=headers, stream=True)
                    response.raise_for_status()

                    # Extract filename from URL and append '.pdf' extension
                    filename = pdf_url.split('/')[-1]
                    if not filename.lower().endswith('.pdf'):
                        filename += '.pdf'

                    # Save PDF content to a file with the correct filename and extension
                    with open(filename, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    # Increment count of downloaded PDFs
                    pdfs_downloaded += 1
                    print(f"\n Downloaded PDF: {filename} \n {pdfs_downloaded} PDF downloaded yet. ")

                except requests.exceptions.RequestException as e:
                    print(f"\n Error downloading PDF from {pdf_url}: {e} \n \n")
                    print(f"\n Downloaded PDF: {filename} \n {pdfs_downloaded} PDF downloaded yet. ")


            #if not pdf_urls:
            #    urls_without_pdf.append(url)

        except requests.exceptions.RequestException as e:
            initialiser_no_pdf_url += 1
            urls_without_pdf.append(url)
            print(f" Error occurred while processing {url}: {e} \n \n")
            print(f"\n {pdfs_downloaded} PDF downloaded yet. ")
            print(f" Number of URLs for which no PDF could be downloaded : {initialiser_no_pdf_url}")



    # Print summary
    print("\n----- Summary -----")
    print(f"Total input URLs: {total_urls}")
   # print(f"Total PDF URLs found: {pdf_urls_found}")
    print(f"Total PDFs downloaded: {pdfs_downloaded}")
    ratio = pdfs_downloaded/total_urls
    print(f"Url to PDF ratio : {ratio} \n\n ")



    # Save URLs without PDFs to a text file
    if urls_without_pdf:
        total_urls_without_pdf = len(urls_without_pdf)
        print(f"Number of URLs for which no PDF could be downloaded : {total_urls_without_pdf}")
        with open('urls_without_pdf.txt', 'w') as file:
            for url in urls_without_pdf:
                file.write(url.strip() + " \n")
        print(f"List of URLs for which no PDF could be downloaded saved to 'urls_without_pdf.txt' \n")
        print(f"Starting to Unprefix the Transformed DOI of the URLs for which no PDF could be downloaded \n Entering Entry point 5A ")
        entry_point_5A()






"""-----------------------------------------------------------------------------------------------"""
# The Deduplicator Function Entry_point_07AUTO / Function Entry_point_07_manual
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the seventh script
# This is deduplicator script
#
#
def entry_point_07_manual(): #called from main central script
    duplicate_main_manual()
    entry_point_08_AUTO() # chained to entry_point_08, Pdf to txt convertor

def entry_point_07AUTO(): #chained from enrtry_point_05A, reverse url transformer for the DOIs
    duplicate_main_auto()
    entry_point_08_AUTO() # chained to entry_point_08, Pdf to txt convertor

def calculate_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)  # Read in 64k chunks
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def copy_unique_files(source_directory, file_extension=None):
    sub_counter_permission_denied_files = 0

    # Create a timestamp for the destination directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    destination_dir_timestamped = f"no_duplicates_{timestamp}"

    # Create the timestamped destination directory
    os.makedirs(destination_dir_timestamped, exist_ok=True)

    # Dictionary to store hashes and corresponding file paths
    hash_to_path = {}

    # Convert the provided extension to lowercase for case-insensitive comparison
    if file_extension:
        file_extension = file_extension.lower()

    # Iterate over files in the source directory
    for file_name in os.listdir(source_directory):
        file_path = os.path.join(source_directory, file_name)
        if os.path.isfile(file_path):  # Check if it's a file (not a directory)
            # Get the lowercase extension of the file
            file_ext = os.path.splitext(file_name)[1].lower()
            # Check if the file extension matches the provided extension (case-insensitive)
            if file_extension and not file_ext == file_extension:
                continue  # Skip files with non-matching extensions
            try:
                file_hash = calculate_hash(file_path)
                if file_hash not in hash_to_path:
                    hash_to_path[file_hash] = file_path
            except PermissionError:
                sub_counter_permission_denied_files += 1
                # print(f"Permission denied for file: {file_path}. Skipping.")

    # Copy unique files to the destination directory
    for file_hash, file_path in hash_to_path.items():
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_dir_timestamped, file_name)
        shutil.copy2(file_path, destination_path)

    return sub_counter_permission_denied_files  # Return the count of permission denied files

def duplicate_summary_print(source_directory, file_extension=None):
    # Print total number of files in source directory
    if file_extension:
        # If file_extension is provided, count only files with that extension
        total_files_source = sum(1 for file_name in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, file_name)) and file_name.lower().endswith(file_extension))
    else:
        # If file_extension is not provided, count all files
        total_files_source = sum(1 for file_name in os.listdir(source_directory) if os.path.isfile(os.path.join(source_directory, file_name)))
    print(f" Total number of files in the source directory: {total_files_source}")

##       # List files in source and destination directories
##    source_files = set(os.listdir(source_directory))
##    destination_directory = f"no_duplicates_{datetime.now().strftime('%Y%m%d%H%M%S')}"
##    destination_files = set(os.listdir(destination_directory))
##

    # Print total number of files in destination directory
    destination_directory = f"no_duplicates_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    total_files_destination = sum(1 for _ in os.listdir(destination_directory) if os.path.isfile(os.path.join(destination_directory, _)))
    print(f" Total number of files in the destination directory: {total_files_destination}")


##    # Find missing files in the destination directory
##    missing_files = source_files - destination_files
##    if missing_files:
##        print(" Missing files in the destination directory:")
##        for file_name in missing_files:
##            print(f"  - {file_name}")


# Modified duplicate_main_manual function
def duplicate_main_manual():
    source_directory = input(r"path/to/source_directory: ")
    file_extension = input("'.txt'. Change this to the desired file extension, or leave as None to include all files: ")
    sub_counter_permission_denied_files = copy_unique_files(source_directory, file_extension)
    print(f" File extension used for target and scan duplicates was {file_extension}")
    print(f" Total files Skipped due to permission denied {sub_counter_permission_denied_files}")
    duplicate_summary_print(source_directory, file_extension)


def duplicate_main_auto():
    print(f" Welcome to Entry point 4 : Duplicate removal. This is to ensure we have only one copy of the downloaded corpus. As we used multiple mirrors to download, there can be redundancy of PDFs. This will create a time-stamped final output directory for you, and no alteration would be made to the current working directory.")
    source_directory = os.getcwd()
    sub_counter_permission_denied_files = 0
    file_extension = '.pdf'
    copy_unique_files(source_directory, file_extension)
    print(f" File extension used for target and scan duplicates was {file_extension}")
    print(f" Total files Skipped due to permission denied {sub_counter_permission_denied_files}")
    duplicate_summary_print(source_directory, file_extension)
    #pdf_2_txt_auto() # Calling Fifth Script in automatic mode






"""-----------------------------------------------------------------------------------------------"""
# The PDF to TXT convertor Function Entry_point_08_auto / entry_point_08_manual
"""-----------------------------------------------------------------------------------------------"""

# Define functions from the Eighth script
# This is pdf to txt convertor script/functions
#
#
def entry_point_08_manual(): #called from main central script
    pdf_2_txt_manual()
    # may in future chained to thhe summarisation modules

def entry_point_08_auto(): #chained from entry_point_07AUTO and entry_point_07_manual
    pdf_2_txt_auto()
    # may in future chained to thhe summarisation modules

def extract_text_from_pdf(pdf_path, output_directory):
    if os.path.isfile(pdf_path) and pdf_path.endswith('.pdf'):
        pdf_files = [pdf_path]
    elif os.path.isdir(pdf_path):
        pdf_files = [os.path.join(pdf_path, file) for file in os.listdir(pdf_path) if file.endswith('.pdf')]
    else:
        print("Invalid input: Not a valid PDF file or directory path.")
        return

    num_files = len(pdf_files)
    print("Number of PDF files detected: ", num_files)

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print("Created output directory:", output_directory)

    # Iterate over each PDF file
    for i, file_path in enumerate(pdf_files, start=1):
        file_name = os.path.basename(file_path)
        output_file = os.path.splitext(file_name)[0] + '.txt'

        print("Processing PDF file {}/{}: {}".format(i, num_files, file_name))

        pdf = PdfReader(file_path)

        with open(os.path.join(output_directory, output_file), 'w', encoding='utf-8') as f:
            for page_num in range(len(pdf.pages)):
                pageObj = pdf.pages[page_num]

                try:
                    txt = pageObj.extract_text()
                  # print(''.center(100, '-'))
                except:
                    pass
                else:
                    f.write('Page {0}\n'.format(page_num+1))
                    f.write(''.center(100, '-'))
                    f.write(txt)

        print("Text extraction completed for {}.".format(file_name))

def pdf_2_txt_auto():
    pdf_path = r'/path/to/pdf/files'  # Replace with the path to your PDF file or directory

    # Create output directory in the same path as the source directory
    output_directory = os.path.join(os.path.dirname(pdf_path), datetime.now().strftime("%Y%m%d_%H%M%S") + "_pdf_2_txt")

    extract_text_from_pdf(pdf_path, output_directory)

def pdf_2_txt_manual():
    pdf_path = input(r"Enter the path to the PDF file or directory: ")

    # Create output directory in the same path as the source directory
    output_directory = os.path.join(os.path.dirname(pdf_path), datetime.now().strftime("%Y%m%d_%H%M%S") + "_pdf_2_txt")

    extract_text_from_pdf(pdf_path, output_directory)





"""-----------------------------------------------------------------------------------------------"""
# Utilities Subsection entry_point_09() # currently only called manually
"""-----------------------------------------------------------------------------------------------"""


# define function for ninth scrit
# The Utilties
#
#
def entry_point_09(): # currently only called manually

    print(" The Utilities  \n Type '10' to exit Utilities and return to the main section !\n")

    while True:
        entry_point = input("Select an entry point:\n"


                            "1.          Citations \n"
                            "2.          More otions will be available soon \n"
                            "3.          More options will be available soon \n"
                            "3A.         Image maniulation detection will be available soon \n"
                            "3B.         Summarization will be available soon \n"
                            "3C.         Feature extraction will be available soon \n"
                            "1111.      Check for the Updates \n"
                            "1112.      The License \n"
                            "999.        Clear Screen\n"
                            "000.        Exit\n"
                            "Enter your choice (1/10): ")

        if entry_point == '1':
            entry_point_Util_01() # The Citation

        elif entry_point == '1111':
            entry_point_Util_1111() # The updater

        elif entry_point == '1112':
            entry_point_Util_1112() # The License

        elif entry_point == '999':
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen command


        elif entry_point == '000' :
            print("Exiting the Utilities section. Back in Main section \n")
            break
        else :
            print("Invalid Selection")



"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
This the Subsection Utilities executed under entry_point_9 #utilities
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The Citation script function entry_point_Util_01
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def entry_point_Util_01(): # called by entry_point_09.option.1 The citation script function
    print(" Welcome to the Citation Entry_point  (entry_point_Util_01)")
    encapsulated_citations()



def encapsulated_citations():
    # Function to retrieve citations for given DOIs in the specified format and style
    def retrieve_citations(identifiers, style):
        citations = []
        for identifier in identifiers:
            doi = extract_doi(identifier)
            if doi:
                citation = cn.content_negotiation(ids=doi, format="citeproc-json", style=style)
                citations.append(citation)
            else:
                print(f"Invalid DOI or DOI URL: {identifier}")
        return citations

    # Function to extract DOI from a string (DOI or DOI URL)
    def extract_doi(identifier):
        if identifier.startswith("https://doi.org/"):
            return identifier[len("https://doi.org/"):]
        else:
            return identifier

    # Function to export citations to a file in the specified format
    def export_citations_to_file(citations, file_format, output_dir):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"citations_{timestamp}.{file_format}"
        file_path = os.path.join(output_dir, file_name)

        if file_format == "txt":
            with open(file_path, "w") as file:
                for citation in citations:
                    file.write(citation + "\n\n")
        elif file_format == "ris":
            with open(file_path, "w") as file:
                for citation in citations:
                    file.write(citation + "\n\n")
        elif file_format == "bib":
            with open(file_path, "w") as file:
                for citation in citations:
                    file.write(citation + "\n\n")
        elif file_format == "json":
            with open(file_path, "w") as file:
                json.dump(citations, file, indent=4)
        elif file_format == "csl":
            root = ET.Element("root")

            for citation in citations:
                ET.SubElement(root, "citation", {"data": citation})

            tree = ET.ElementTree(root)
            tree.write(file_path, encoding="utf-8", xml_declaration=True)
        else:
            print("Unsupported file format.")

        print(f"Citations exported to {file_path}")

    # Main function
    def encapsulated_citations_main():
        # Ask for input file path containing the list of DOIs
        input_file_path = input("Enter the path to the input file containing the list of DOIs: ")
        with open(input_file_path, "r") as file:
            identifiers = [line.strip() for line in file if line.strip()]

        # Ask for output directory path
        output_dir = input("Enter the path to the output directory for saving exported citations: ")
        os.makedirs(output_dir, exist_ok=True)

        # Available citation styles
        available_styles = [
            "apa",
            "mla",
            "chicago-fullnote-bibliography",
            "harvard1",
            "american-sociological-association",
            "american-antiquity",
            "american-medical-association",
            "ieee",
            "vancouver",
            "turabian-fullnote-bibliography",
            "american-chemical-society",
            "bluebook",
            "apsa",
            "council-of-science-editors"
            # Add more citation styles here as needed
        ]

        # Display available styles for user selection
        print("Select the citation style:")
        for i, style in enumerate(available_styles, 1):
            print(f"{i}. {style}")

        # Ask user to select citation style
        style_selection = int(input("Enter the number corresponding to the desired style: ")) - 1
        selected_style = available_styles[style_selection]

        # Retrieve citations
        citations = retrieve_citations(identifiers, selected_style)

        # Print citations
        for i, citation in enumerate(citations, 1):
            print(f"Citation {i}:")
            print(citation)
            print()

        # Export citations to a file
        available_file_formats = ["txt", "ris", "bib", "json", "csl"]
        print("Select the file format for exporting citations:")
        for i, file_format in enumerate(available_file_formats, 1):
            print(f"{i}. {file_format}")
        file_format_selection = int(input("Enter the number corresponding to the desired file format: ")) - 1
        selected_file_format = available_file_formats[file_format_selection]

        export_citations_to_file(citations, selected_file_format, output_dir)

    encapsulated_citations_main()





'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The updater script function entry_point_Util_1111
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def entry_point_Util_1111(): # called by entry_point_09.option.1111 The updater script function
    print(" Checking for the available updates : ")
    root_updater_main_function()

def download_file(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except:
        print(".\n.")
        pass

    #sys.exit()


def calculate_hash(contents):
    return hashlib.sha256(contents.encode()).hexdigest()

def root_updater_main_function():
    #url = "https://raw.githubusercontent.com/ydv-amit-ydv/af_chainsaw/main/test.py"
    url = ""
    remote_file_contents = download_file(url)

    if remote_file_contents:
        local_hash = calculate_hash(open(sys.argv[0], 'r').read())
        remote_hash = calculate_hash(remote_file_contents)

        if local_hash != remote_hash:
            with open(sys.argv[0], 'w') as file:
                file.write(remote_file_contents)
                print(".\n.\n.\n")



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
The License entry_point_Util_1112
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def entry_point_Util_1112():
    print("Checking for the available updates:")
    encapsulated_the_license_function()

def encapsulated_the_license_function():
    # Function to read the contents of license.txt file
    def read_license_file():
        module_dir = os.path.dirname(__file__)  # Get the directory of the current module
        license_file_path = os.path.join(module_dir, 'data', 'LICENSE.txt')
        with open(license_file_path, 'r') as file:
            license_content = file.read()
        return license_content

    # Display the contents of license.txt file
    print("License Agreement:")
    print(read_license_file())
    input("Press any key to go back...")






"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



# Main entry point for the combined script

def main():
    while True:
        try:
            print("Welcome to the Combined Data Mining Utility !\n By Using this script you agree to LICENSE")
            root_updater_main_function()
            while True:
                entry_point = input("Select an entry point :\n"
                                    "00.        Help \n"
                                    "1.         PubMed search/query \n"
                                    "2.         Get abstracts from PubMed IDs\n"
                                    "3.         Attempt Full Text Download from PubMed\n"
                                    "4.         Process PubMed IDs to get DOI for 3rd party search\n"
                                    "5.         Url Transform PubMed IDs for 3rd party search \n"
                                    "6.         Crawl and Download from URLs\n"
                                    "7.         Remove Duplicates\n"
                                    "8.         PDF_2_txt\n"
                                    "9.         Additional Utilities\n"
                                    "999.       Clear Screen\n"
                                    "0000.      Exit\n"
                                    "Enter your choice (1/2/3/4/5/6/7/8/9/999/10): ")

                if entry_point == '00' or entry_point.lower() == 'help':
                    entry_point_help()

                elif entry_point == '1':
                    entry_point_01() # This is to make the PubMed search
                    return

                elif entry_point == '1A':
                    entry_point_01A() #Graph maker based on the n of pubmed_ids retrived
                    return

                elif entry_point == '2':
                    entry_point_02() # This is to retrive abstracts from PubMed

                elif entry_point == '3':
                    entry_point_03() # This is to attempt full text downloads from the Pubmed this have resume capabilities

                elif entry_point == '4':
                    entry_point_04() # Get DOI from Pubmed_Id

                elif entry_point == '5':
                    entry_point_05() # Transform DOI (prefix) entry_point5A : exceuted after 3 to strip back the transformed Doi to DOI

                elif entry_point == '6':
                    entry_point_06() # Main scrapper and downloader

                elif entry_point == '7':
                    entry_point_07_manual() #as multiple sources can be used , so remove duplicate downloads

                elif entry_point == '8':
                    entry_point_08_manual() # to get txt files from the pdf file

                elif entry_point == '9':
                    entry_point_09() # Additional Utility

                elif entry_point == '999':
                    os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen command

                elif entry_point == '0000' :
                    print("Exiting the Utility.")
                    #break
                    return
                else :
                    print("Invalid Selection")


        except Exception as e:
            print("An error occurred:", e)
            print("\n \n \n")
            continue  # Restart the loop from the beginning


    return


if __name__ == "__main__":
    main()
