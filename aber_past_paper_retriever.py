import os, requests, getpass

DEPARTMENT = 'compsci'

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


def get_paper(year, semester, module_code, auth_header):
    url = format_pdf_url(year, semester, module_code)
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