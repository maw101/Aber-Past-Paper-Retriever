import os
import requests
import lxml.html
import re

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

    def set_module_code(self, module_code):
        """Sets the module code attribute.

        Attributes:
            module_code (str): the new value for the module code attribute

        """
        # validate
        validation_result = re.match('^[A-Z]{2,3}[0-9]{4,5}$', module_code)
        if validation_result is None:
            raise ValueError('Invalid Module Code Provided')
        self.module_code = module_code

    def set_destination_folder(self, destination_folder):
        """Sets the destination folder path attribute.

        Attributes:
            destination_folder (str): the new value for the destination path

        """
        self.destination_folder = destination_folder

    def set_graduate_level(self, graduate_level):
        """Sets the user graduate level attribute.

        Attributes:
            graduate_level (str): the new value for the graduate level attribute

        """
        self.graduate_level = graduate_level

    def move_into_module_folder(self):
        """Moves into the module folder."""
        # move in to the destination directory
        os.chdir(self.destination_folder)

        # check if the folder where we are going to write exists
        try:
            os.mkdir(self.module_code)
        except OSError:
            pass

        # move in to the module directory
        os.chdir(self.module_code)

    def move_out_of_module_folder(self):
        """Moves out of the module folder."""
        # move in to the destination directory
        os.chdir('..')
