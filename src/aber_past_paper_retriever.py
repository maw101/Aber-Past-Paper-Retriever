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
    
    def set_auth_header(self, username, password):
        """Sets the authentication header attribute.

        Attributes:
            username (str): the username
            password (str): the password

        """
        # encode HTTPBasicAuth header
        self.auth_header = requests.auth.HTTPBasicAuth(username, password)

    def set_department_url(self, department_url):
        """Sets the department URL attribute.

        Attributes:
            department_url (str): the new value for the department URL attribute

        """
        self.department_url = department_url
        
        # check to see if we are on the Business School intermediary graduate level page
        if self.department_url[-6:] == '/smba/':
            if self.graduate_level == 'Undergraduate':
                self.department_url = self.department_url + 'ugrad/'
            else:
                self.department_url = self.department_url + 'postg/'

    