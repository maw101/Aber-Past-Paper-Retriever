"""Aberystwyth University Automatic Past Paper Retriever.

This module provides an automated solution to retrieving past papers from the
Abersywtyth University Past Paper's Page for a given Module Code.

If the user is authorised for access to past paper's with their provided
credentials, papers from all available years for a given module are downloaded
in to their own directory.

Requirements:
	getpass
    requests
    lxml.html

Example:
	$ python3 aber_past_paper_retriever.py

"""

import os
import getpass
import requests
import lxml.html

# define constants
WEBSITE_BASE_URL = 'https://www.aber.ac.uk'

def is_existing_file(url, auth_header):
    """Checks if a file exists at the given URL.

	Args:
		url (str): the url to retrieve the file from
		auth_header (HTTPBasicAuth): a authorization header for the request
	Returns:
		bool: True if a file exists at the given URL, False otherwise.

	"""
    # get header of file at url
    url_request_response = requests.head(url, auth=auth_header)
    return url_request_response.headers['Content-Length'] != '' # file exists


def get_auth_header():
    """Gets username and password for authorization header.

	Returns:
		auth_header (HTTPBasicAuth): a authorisation header with the users details

	"""
    try:
        username = getpass.getpass("Enter Aberystwyth Username: ")
    except getpass.GetPassWarning as warning:
        print('Warning:', warning)

    try:
        password = getpass.getpass("Enter Aberystwyth Password: ")
    except getpass.GetPassWarning as warning:
        print('Warning:', warning)

    return requests.auth.HTTPBasicAuth(username, password)


def get_module_details():
    """Gets department URL and module code from the user.

	Returns:
		tuple (str, str): department url and module code in a tuple

	"""
    department_url = input("Enter your Department URL from the past papers \
                           URL (see README file, leave blank for compsci): ")
    if department_url == '':
        department_url = 'https://www.aber.ac.uk/en/past-papers/compsci/'

    module_code = input("Enter Module Code: ")
    if module_code == '':
        raise RuntimeError("No Module Code Given")

    print() # print blank line
    return (department_url, module_code)


def get_paper(pdf_url, auth_header):
    """Gets a local copy of the paper from the given URL.

	Args:
		pdf_url (str): the url to retrieve the file from
		auth_header (HTTPBasicAuth): a authorization header for the request

	"""
    if is_existing_file(pdf_url, auth_header):
        try:
            # send a HTTP request to the server and save
            # the HTTP response in a response object called r
            url_request_response = requests.get(pdf_url, auth=auth_header)
            # raise exception if response not successful
            url_request_response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print('HTTP Error Occurred:', http_err)
        else:
            # get semester ID and PDF name and combine the two
            local_pdf_path = '-'.join(pdf_url.split('/')[-2:])

            with open(local_pdf_path, 'wb') as local_file:
                # Saving received content as a PDF file in binary format
                # write the contents of the response (r.content) to a new file in binary mode.
                local_file.write(url_request_response.content)
            print('Retrieved PDF from URL:', pdf_url)
    else:
        print('Failed to find PDF at URL:', pdf_url)


def get_semester_page_links(department_url):
    """Gets all semester page links from a department's exam paper page.

	Args:
		department_url (str): the url for the department's exam paper page
	Returns:
		list (str): a list of URLs leading to all semester exam pages

	"""
    department_page_response = requests.get(department_url, stream=True)
    department_page_response.raw.decode_content = True
    page_tree = lxml.html.parse(department_page_response.raw)

    semester_links = page_tree.xpath('/html/body/div[2]/main/div/article/div//a/@href')
    semester_links = [WEBSITE_BASE_URL + sem_url for sem_url in semester_links]

    return semester_links


def get_paper_links_for_semester(semester_url):
    """Gets all exam paper file links from a semester's exam paper page.

	Args:
		semester_url (str): the url for the semester's exam paper page
	Returns:
		list (str): a list of URLs leading to all exam paper files

	"""
    semester_page_response = requests.get(semester_url, stream=True)
    semester_page_response.raw.decode_content = True
    page_tree = lxml.html.parse(semester_page_response.raw)

    paper_links = page_tree.xpath('/html/body/div[2]/main/div/article/div//a/@href')
    paper_links = [WEBSITE_BASE_URL + paper_url for paper_url in paper_links]

    return paper_links

def find_module_paper_url(paper_urls, module_code):
    """Searches for a module code within a list of past paper file URLs.

	Args:
        paper_urls (list str): a list of URLs leading to all exam paper files
		module_code (str): the code for the module searching for
	Returns:
		str containing the module papers URL if module code found, None otherwise

	"""
    for url in paper_urls:
        if module_code in url:
            return url
    return None

def get_module_paper_for_semester(paper_urls, module_code, auth_header):
    """Gets exam paper file (if exists) from a list of exam paper file links.

	Args:
        paper_urls (list str): a list of URLs leading to all exam paper files
        module_code (str): the code for the module searching for
		auth_header (HTTPBasicAuth): a authorization header for the request

	"""
    paper_url = find_module_paper_url(paper_urls, module_code)
    if paper_url is not None:
        get_paper(paper_url, auth_header)


if __name__ == '__main__':
    AUTH_HEADER = get_auth_header()

    while True:
        DEPARTMENT_URL, MODULE_CODE = get_module_details()

        # get current working directory (CWD) according to OS
        CWD = os.getcwd()

        # move in to the current working directory
        os.chdir(CWD)

        # check if the folder where we are going to write exists
        try:
            os.mkdir(MODULE_CODE)
        except OSError as error:
            print(error)

        # move in to the module directory
        os.chdir(MODULE_CODE)

        # get papers in our range
        print("Retrieving Papers for", MODULE_CODE)

        SEMESTER_PAGE_LINKS = get_semester_page_links(DEPARTMENT_URL)

        for semester in SEMESTER_PAGE_LINKS:
            CURRENT_SEMESTER_PAPER_LINKS = get_paper_links_for_semester(semester)
            get_module_paper_for_semester(CURRENT_SEMESTER_PAPER_LINKS, MODULE_CODE, AUTH_HEADER)

        print("\nAll Semesters Checked. Check folder for any downloaded papers.")

        print() # print blank line
        EXIT_VALUE = input("Press Enter to EXIT the program, any other input \
                           will allow you to enter another module!\n")
        if EXIT_VALUE == '':
            break

        os.chdir('..') # move up one directory
