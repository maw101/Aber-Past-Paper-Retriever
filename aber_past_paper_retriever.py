import datetime, os, requests, getpass
import lxml.html

# define constants
DEFAULT_YEAR_FROM = 2015
WEBSITE_BASE_URL = 'https://www.aber.ac.uk'

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
    department_url = input("Enter your Department URL from the past papers URL (see README file, leave blank for compsci): ")
    if department_url == '':
        department_url = 'https://www.aber.ac.uk/en/past-papers/compsci/'
        
    module_code = input("Enter Module Code: ")
    if module_code == '':
        raise RuntimeError("No Module Code Given")
    
    print() # print blank line
    return (department_url, module_code)


def get_paper(year, semester, module_code, department, auth_header):
    url = format_pdf_url(year, semester, module_code, department)
    if file_exists(url, auth_header):
        try:
            # send a HTTP request to the server and save
            # the HTTP response in a response object called r
            r = requests.get(url, auth=auth_header)
            # raise exception if response not successful
            r.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print("HTTP Error Occurred:", http_err)
        else:
            local_pdf_path = format_local_pdf_path(year, semester, module_code)

            with open(local_pdf_path, 'wb') as f:
                # Saving received content as a PDF file in binary format 
                # write the contents of the response (r.content) to a new file in binary mode. 
                f.write(r.content)
            print_formatted_retrieval_result(year, semester, module_code, "Retrieved")
    else:
        print_formatted_retrieval_result(year, semester, module_code, "Not Found")


def get_semester_page_links(department_url):
    department_page_response = requests.get(department_url, stream=True)
    department_page_response.raw.decode_content = True
    page_tree = lxml.html.parse(department_page_response.raw)
    
    semester_links = page_tree.xpath('/html/body/div[2]/main/div/article/div//a/@href')
    semester_links = [WEBSITE_BASE_URL + sem_url for sem_url in semester_links]
    
    return semester_links

if __name__ == '__main__':
    AUTH_HEADER = get_auth_header()
    while True:
        DEPARTMENT_URL, MODULE_CODE = get_module_details()

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
        
        # TODO

        print("\nAll Papers in Range Retrieved")

        print() # print blank line
        exit_value = input("Press Enter to EXIT the program, any other input will allow you to enter another module!\n")
        if exit_value == '':
            break
    
