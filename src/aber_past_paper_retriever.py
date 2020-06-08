import os
import requests
import lxml.html

WEBSITE_BASE_URL = 'https://www.aber.ac.uk'
DEPARTMENT_LISTING_URL = WEBSITE_BASE_URL + '/en/past-papers/'

class PaperRetriever:
    """Represents a Past Paper Retriever from the Aber Uni Website.

    Attributes:
        auth_header (HTTPBasicAuth Header): stores user credential header
        department_url (str): URL for the department
        graduate_level (str): the graduate level of the user
        destination_folder (str): a path for the output folder for PDF's found
        module_code (str): the 7 character module code

    """
    
    