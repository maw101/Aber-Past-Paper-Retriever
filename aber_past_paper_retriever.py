import os, requests, getpass

def format_pdf_url(year, semester, module_code):
    return f'https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/compsci/sem{semester}-{year % 100}/{module_code}-{year % 100}.pdf'


def format_local_pdf_path(year, semester, module_code):
    output_file_name = f'{module_code}-{year}-{semester}.pdf'
    output_file_path = os.path.join(module_code, output_file_name)
    return output_file_path;


def get_auth_header():
    # get username and password for authentication
    USERNAME = getpass.getpass("Enter Aberystwyth Username: ")
    
    try: 
        PASSWORD = getpass.getpass("Enter Aberystwyth Password: ")
    except Exception as error: 
        print('ERROR', error)
        
    return requests.auth.HTTPBasicAuth(USERNAME, PASSWORD)