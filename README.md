# Aber Uni Past Paper Retriever
Fetches all Past Paper PDFs for a given module within a given year range - upto and including 2018.

Past Papers are stored at [aber.ac.uk/en/past-papers/](https://www.aber.ac.uk/en/past-papers/).

## Requirements
* [Python 3](https://www.python.org/downloads/) (utilises os, datetime, getpass libraries)
* [Python 3 Requests](https://pypi.org/project/requests/) Library
* [lxml.html](https://lxml.de/lxmlhtml.html)

## Usage
### aber_past_paper_retriever.py
Once the requirements are satisfied:

Clone or download the project to your machine.

Then in a terminal window run:

```sh
python3 aber_past_paper_retriever.py
```

1) Enter Aberystwyth University Username
2) Enter Account Password
3) Enter your departments past paper page URL [Go to this page](https://www.aber.ac.uk/en/past-papers/) and click on your department.
4) Enter the Module Code - eg PH01010, CS23820, or HQ33220

Papers will then be retrieved and stored within a new folder in the location where the script is being run from.

#### Example Output
```text
Enter Aberystwyth Username: 
Enter Aberystwyth Password: 
Enter your Department URL from the past papers URL (see README file, leave blank for compsci): 
Enter Module Code: CS26520

Retrieving Papers for CS26520
Retrieved PDF from URL: https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/compsci/sem2-19/CS26520-Artificial-Intelligence.pdf
Retrieved PDF from URL: https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/compsci/sem2-18/CS26520-18.pdf
Retrieved PDF from URL: https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/compsci/sem2-17/CS26520-17.pdf

All Semesters Checked. Check folder for any downloaded papers.

Press Enter to EXIT the program, any other input will allow you to enter another module!
```

## Errors
* If you encounter a 401 Unauthorized Error your Aber Credentials (username/password) are either incorrect or you do not have the necessary permissions to view the document.

## License

[GNU General Public License v3.0](https://github.com/maw101/Aber-Past-Paper-Retriever/blob/master/LICENSE)
