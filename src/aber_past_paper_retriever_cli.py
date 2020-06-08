"""Aberystwyth University Automatic Past Paper Retriever CLI Interface.

This module provides a CLI interface for retrieving past papers from the
Abersywtyth University Past Paper's Page for a given Module Code.

Requirements:
	getpass
    requests
    lxml.html

Example:
	$ python3 aber_past_paper_retriever_cli.py

"""

import os
import getpass
import aber_past_paper_retriever

def get_credentials():
    """Gets username and password credentials.

	Returns:
		(str, str): (username, password)

	"""
    try:
        username = getpass.getpass("Enter Aberystwyth Username: ")
    except getpass.GetPassWarning as warning:
        print('Warning:', warning)

    try:
        password = getpass.getpass("Enter Aberystwyth Password: ")
    except getpass.GetPassWarning as warning:
        print('Warning:', warning)

    return (username, password)


def get_module_details():
    """Gets department URL and module code from the user.

	Returns:
		tuple (str, str): department url and module code in a tuple

	"""
    department_url = input("Enter your Department URL from the past papers" +
                           " URL (see README file, leave blank for compsci): ")
    if department_url == '':
        department_url = 'https://www.aber.ac.uk/en/past-papers/compsci/'

    module_code = input("Enter Module Code: ")
    if module_code == '':
        raise RuntimeError("No Module Code Given")

    print() # print blank line
    return (department_url, module_code)
