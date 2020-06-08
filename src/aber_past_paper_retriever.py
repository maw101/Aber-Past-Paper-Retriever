"""Aberystwyth University Automatic Past Paper Retriever.

This module provides an automated solution to retrieving past papers from the
Abersywtyth University Past Paper's Page for a given Module Code.

If the user is authorised for access to past paper's with their provided
credentials, papers from all available years for a given module are downloaded
in to their own directory.

Requirements:
    requests
    lxml.html

Usage:
    Use the CLI or GUI interface, both of which utilise this class.

"""

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

    def is_existing_file(self, file_url):
        """Checks if a file exists at the given URL.
    
        Args:
            file_url (str): the url to retrieve the file from
        Returns:
            bool: True if a file exists at the given URL, False otherwise.
    
        """
        # get header of file at url
        url_request_response = requests.head(file_url, auth=self.auth_header)
        return url_request_response.headers['Content-Length'] != '' # file exists

    def get_paper(self, pdf_url):
        """Gets a local copy of the paper from the given URL.
    
        Args:
            pdf_url (str): the url to retrieve the file from
    
        """
        if self.is_existing_file(pdf_url):
            # send a HTTP request to the server and save
            # the HTTP response in a response object called r
            url_request_response = requests.get(pdf_url, auth=self.auth_header)
            # raise exception if response not successful
            url_request_response.raise_for_status()

            # get semester ID and PDF name and combine the two
            local_pdf_path = '-'.join(pdf_url.split('/')[-2:])

            with open(local_pdf_path, 'wb') as local_file:
                # Saving received content as a PDF file in binary format
                # write the contents of the response (r.content) to a new file in binary mode.
                local_file.write(url_request_response.content)
            print('Retrieved', pdf_url)
            print('Local PDF path', local_pdf_path)
        else:
            raise ValueError('Failed to find PDF at URL: ' + pdf_url)

    def get_semester_page_links(self):
        """Gets all semester page links from a department's exam paper page.
    
        Returns:
            list (str): a list of URLs leading to all semester exam pages
    
        """
        department_page_response = requests.get(self.department_url, stream=True)
        department_page_response.raw.decode_content = True
        page_tree = lxml.html.parse(department_page_response.raw)
    
        semester_links = page_tree.xpath('/html/body/div[2]/main/div/article/div//a/@href')
        semester_links = [WEBSITE_BASE_URL + sem_url for sem_url in semester_links]
    
        return semester_links

    def find_module_paper_url(self, paper_urls):
        """Searches for a module code within a list of past paper file URLs.
    
        Args:
            paper_urls (list str): a list of URLs leading to all exam paper files
        Returns:
            str containing the module papers URL if module code found, None otherwise
    
        """
        for url in paper_urls:
            if self.module_code in url:
                return url
        return None

    def get_module_paper_for_semester(self, paper_urls):
        """Gets exam paper file (if exists) from a list of exam paper file links.
    
        Args:
            paper_urls (list str): a list of URLs leading to all exam paper files
            module_code (str): the code for the module searching for
            auth_header (HTTPBasicAuth): a authorization header for the request
    
        """
        paper_url = self.find_module_paper_url(paper_urls)
        if paper_url is not None:
            self.get_paper(paper_url)

    def get_all_module_papers(self, semester_page_links):
        """Gets all exam papers for a given module for all semesters.
    
        Args:
            semester_page_links (list str): a list of URLs leading to semesters
        Returns:
            list str: links to all exam papers found for the module
    
        """
        for semester in semester_page_links:
                current_semester_paper_links = self.get_paper_links_for_semester(semester)
                self.get_module_paper_for_semester(current_semester_paper_links)

