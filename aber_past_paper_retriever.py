import datetime, os, requests, getpass

# define constants
DEFAULT_YEAR_FROM = 2015




def format_pdf_url(year, semester, module_code, department):
    year_two_digit_format = year % 100
    return f'https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/{department}/sem{semester}-{year_two_digit_format}/{module_code}-{year_two_digit_format}.pdf'


def format_local_pdf_path(year, semester, module_code):
    output_file_name = f'{module_code}-{year}-{semester}.pdf'
    output_file_path = os.path.join(module_code, output_file_name)
    return output_file_path;


def print_formatted_retrieval_result(year, semester, module_code, result):
    print(module_code, year, "Semester", semester, result)
    
    
def file_exists(url, auth_header):
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


def get_module_details():
    department = input("Enter your Department URL from the past papers URL (see README file, leave blank for compsci): ")
    if department is '':
        department = "compsci"
        
    module_code = input("Enter Module Code: ")
    if module_code is '':
        raise RuntimeError("No Module Code Given")
        
    try:
        year_from = int(input("Enter Starting Year to Retrieve for: "))
    except ValueError:
        year_from = DEFAULT_YEAR_FROM
    
    try:
        year_to = int(input("Enter End Year to Retrieve for: "))
    except ValueError:
        year_to = datetime.datetime.now().year
    
    print() # print blank line
    return (department, module_code, year_from, year_to)


def get_paper(year, semester, module_code, auth_header, department):
    url = format_pdf_url(year, semester, module_code, department)
    if file_exists(url, auth_header):
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
    AUTH_HEADER = get_auth_header()
    DEPARTMENT_URL_FOLDER, MODULE_CODE, YEAR_FROM, YEAR_TO = get_module_details()

    # get current working directory (CWD) according to OS
    cwd = os.getcwd()

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
            get_paper(year, semester, MODULE_CODE, AUTH_HEADER, DEPARTMENT_URL_FOLDER)

    print("\nAll Papers in Range Retrieved")
    
    
