# Aber Uni Past Paper Retriever
Fetches all Past Paper PDFs for a given module within a given year range - upto and including 2018.

Past Papers are stored at [aber.ac.uk/en/past-papers/](https://www.aber.ac.uk/en/past-papers/).

## Requirements
* [Python 3](https://www.python.org/downloads/) (utilises os, datetime, getpass libraries)
* [Python 3 Requests](https://pypi.org/project/requests/) Library

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
3) Enter your departments URL identifier. This can be found in a past papers web address/URL, examples follow. We always take the value between ../pdf/ and /sem..
    1) <https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/compsci/sem1-18/CS23820-18.pdf> - in this case we enter 'compsci'.
    2) <https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/history/sem2-19/HQ33220-19.pdf> - in this case we enter 'history'.
    3) <https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/imaps/physics/sem1-17/PH01010-17.pdf>  - in this case we enter 'imaps/physics'.
    4) <https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/smba/ugrad/sem1-18/AC10510-18.pdf> - in this case we enter 'smba/ugrad'.
4) Enter the full Module Code including the number of credits it is worth - eg PH01010, CS23820, or HQ33220
5) Enter the First Year to try and retrieve papers for
6) Enter the Last Year you wish to try and retrieve papers for

Papers will then be retrieved and stored within a new folder in the location where the script is being run from.

#### Example Output
```sh
username@computername:~/Documents/ppr$ python3 aber_past_paper_retriever.py 
Enter Aberystwyth Username: 
Enter Aberystwyth Password: 
Enter your Department URL from the past papers URL (see README file, leave blank for compsci): 
Enter Module Code: CS15020
Enter Starting Year to Retrieve for: 2016
Enter End Year to Retrieve for: 2019

Retrieving Papers for CS15020
CS15020 2016 Semester 1 Retrieved
CS15020 2016 Semester 2 Not Found
CS15020 2017 Semester 1 Not Found
CS15020 2017 Semester 2 Retrieved
CS15020 2018 Semester 1 Not Found
CS15020 2018 Semester 2 Retrieved
CS15020 2019 Semester 1 Not Found
CS15020 2019 Semester 2 Not Found

All Papers in Range Retrieved
```


### find_departments_url_identifier.py
Identifies value to be used in step 3 above. 

In a terminal window run:

```sh
python3 find_departments_url_identifier.py
```

Then enter a full URL for a past paper such as those given in the examples in step 3.

#### Example Output
```sh
username@computername:~/Documents/ppr$ python3 find_departments_url_identifier.py 
Enter the full URL for a single past paper: https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/smba/ugrad/sem1-18/AC10510-18.pdf

Your URL Identifier is:
smba/ugrad
```

## Errors
* If you encounter a 401 Unauthorized Error your Aber Credentials (username/password) are either incorrect or you do not have the necessary permissions to view the document.

## License

[GNU General Public License v3.0](https://github.com/maw101/Aber-Past-Paper-Retriever/blob/master/LICENSE)
