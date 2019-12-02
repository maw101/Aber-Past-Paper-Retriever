import os, requests, getpass, datetime

DEPARTMENT = 'compsci'
DEFAULT_YEAR_FROM = 2015

def format_pdf_url(year, semester, module_code, department):
    return f'https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/{department}/sem{semester}-{year % 100}/{module_code}-{year % 100}.pdf'


def format_local_pdf_path(year, semester, module_code):
    output_file_name = f'{module_code}-{year}-{semester}.pdf'
    output_file_path = os.path.join(module_code, output_file_name)
    return output_file_path;


def print_formatted_retrieval_result(year, semester, module_code, result):
    print(module_code, year, "Semester", semester, result)


def file_exists(url):
    r = requests.head(url, auth=auth_header) # get header of file at url
    return r.headers['Content-Length'] != '' # file exists


def get_auth_header():
    # get username and password for authentication
    USERNAME = getpass.getpass("Enter Aberystwyth Username: ")
    
    try: 
        PASSWORD = getpass.getpass("Enter Aberystwyth Password: ")
    except Exception as error: 
        print('ERROR', error)
        
    return requests.auth.HTTPBasicAuth(USERNAME, PASSWORD)


def get_paper(year, semester, module_code, auth_header, department):
    url = format_pdf_url(year, semester, module_code, department)
    if file_exists(url):
        try:
            r = requests.get(url, auth=auth_header)
            # raise exception if response not successful
            r.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print("HTTP Error Occurred:", http_err)
        else:
            # send a HTTP request to the server and save
            # the HTTP response in a response object called r
            local_pdf_path = format_local_pdf_path(year, semester, module_code)
        
            with open(local_pdf_path, 'wb') as f:
                # Saving received content as a png file in 
                # binary format 
                # write the contents of the response (r.content) 
                # to a new file in binary mode. 
                f.write(r.content)
            print_formatted_retrieval_result(year, semester, module_code, "Retrieved")
    else:
        print_formatted_retrieval_result(year, semester, module_code, "Not Found")


if __name__ == '__main__':
    import argparse

    auth_header = get_auth_header()

    # get current working directory (CWD) according to OS
    cwd = os.getcwd()

    # initialise a parser to see if the CWD was passed in as an argument when script called
    parser = argparse.ArgumentParser(description="Get Module Code and Years from and Until")
    parser.add_argument('mod_code', type=str, nargs='?', help='module code to retrieve for')
    parser.add_argument('year_from', type=int, nargs='?', help='year to start retrieval from')
    parser.add_argument('year_to', type=int, nargs='?', help='year to stop retrieval')

    args = parser.parse_args()

    # check parsed arguments 
    if args.mod_code is not None:
        MODULE_CODE = args.mod_code
    else:
        raise RuntimeError("No Module Code Given")
    YEAR_FROM = args.year_from if args.year_from is not None else DEFAULT_YEAR_FROM
    YEAR_TO = args.year_to if args.year_to is not None else datetime.datetime.now().year

    # move in to the new directory
    os.chdir(cwd)

    # check if the folder where we are going to write exists
    try:
        os.mkdir(MODULE_CODE)
    except:
        pass
    
    # get papers in our range range
    print("Retrieving Papers for", MODULE_CODE)
    for year in range(YEAR_FROM, YEAR_TO + 1):
        for semester in [1, 2]:
            get_paper(year, semester, MODULE_CODE, auth_header, DEPARTMENT)

    print("\nAll Papers in Range Retrieved")