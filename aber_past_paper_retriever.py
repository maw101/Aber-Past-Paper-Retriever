import os, requests, getpass
import lxml.html

# define constants
WEBSITE_BASE_URL = 'https://www.aber.ac.uk'

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
    if file_exists(pdf_url, auth_header):
        try:
            # send a HTTP request to the server and save
            # the HTTP response in a response object called r
            r = requests.get(pdf_url, auth=auth_header)
            # raise exception if response not successful
            r.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print('HTTP Error Occurred:', http_err)
        else:
            # get semester ID and PDF name and combine the two
            local_pdf_path = '-'.join(pdf_url.split('/')[-2:])

            with open(local_pdf_path, 'wb') as f:
                # Saving received content as a PDF file in binary format
                # write the contents of the response (r.content) to a new file in binary mode.
                f.write(r.content)
            print('Retrieved PDF from URL:', pdf_url)
    else:
        print('Failed to find PDF at URL:', pdf_url)


def get_semester_page_links(department_url):
    department_page_response = requests.get(department_url, stream=True)
    department_page_response.raw.decode_content = True
    page_tree = lxml.html.parse(department_page_response.raw)

    semester_links = page_tree.xpath('/html/body/div[2]/main/div/article/div//a/@href')
    semester_links = [WEBSITE_BASE_URL + sem_url for sem_url in semester_links]

    return semester_links


def get_paper_links_for_semester(semester_url):
    semester_page_response = requests.get(semester_url, stream=True)
    semester_page_response.raw.decode_content = True
    page_tree = lxml.html.parse(semester_page_response.raw)

    paper_links = page_tree.xpath('/html/body/div[2]/main/div/article/div//a/@href')
    paper_links = [WEBSITE_BASE_URL + paper_url for paper_url in paper_links]

    return paper_links

def find_module_paper_url(paper_urls, module_code):
    for url in paper_urls:
        if module_code in url:
            return url
    return None

def get_module_paper_for_semester(paper_urls, module_code, auth_header):
    paper_url = find_module_paper_url(paper_urls, module_code)
    if paper_url is not None:
        get_paper(paper_url, auth_header)


if __name__ == '__main__':
    AUTH_HEADER = get_auth_header()

    while True:
        DEPARTMENT_URL, MODULE_CODE = get_module_details()

        # get current working directory (CWD) according to OS
        cwd = os.getcwd()

        # move in to the current working directory
        os.chdir(cwd)

        # check if the folder where we are going to write exists
        try:
            os.mkdir(MODULE_CODE)
        except:
            pass

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
        exit_value = input("Press Enter to EXIT the program, any other input \
                           will allow you to enter another module!\n")
        if exit_value == '':
            break
        else:
            os.chdir('..') # move up one directory
