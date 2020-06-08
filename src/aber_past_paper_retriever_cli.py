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


if __name__ == '__main__':
    retriever = aber_past_paper_retriever.PaperRetriever()
    
    username, password = get_credentials()
    retriever.set_auth_header(username, password)

    while True:
        DEPARTMENT_URL, MODULE_CODE = get_module_details()
        retriever.set_department_url(DEPARTMENT_URL)
        retriever.set_module_code(MODULE_CODE) # TODO: NEED TRY CATCH FOR ValueError

        # get current working directory (CWD) according to OS
        CWD = os.getcwd()

        retriever.set_destination_folder(CWD)
        retriever.move_into_module_folder()

        # get papers in our range
        print("Retrieving Papers for", MODULE_CODE)

        retriever.retrieve()

        print("\nAll Semesters Checked. Check folder for any downloaded papers.")

        print() # print blank line
        EXIT_VALUE = input("Press Enter to EXIT the program, any other input" +
                           " will allow you to enter another module!\n")
        if EXIT_VALUE == '':
            break

        retriever.move_out_of_module_folder()
