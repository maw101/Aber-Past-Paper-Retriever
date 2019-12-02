# Aber Uni Past Paper Retriever
Fetches all Past Paper PDFs for a given module within a given year range.

## Requirements
* Python 3
* [Python 3 Requests](https://pypi.org/project/requests/)

## Usage
Once the requirements are satisfied in a terminal window run:

```
python3 aber_past_paper_retriever.py
```

1) Enter Aberystwyth University Username
2) Enter Account Password
3) Enter your departments URL identifier. This can be found in a past papers web address/URL, examples follow. We always take the value between ../pdf/ and /sem..
    1) https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/compsci/sem1-18/CS23820-18.pdf - in this case we enter 'compsci'.
    2) https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/history/sem2-19/HQ33220-19.pdf - in this case we enter 'history'.
    3) https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/imaps/physics/sem1-17/PH01010-17.pdf  - in this case we enter 'imaps/physics'.
4) Enter the full Module Code including the number of credits it is worth - eg PH01010, CS23820, or HQ33220
5) Enter the First Year to try and retrieve papers for
6) Enter the Last Year you wish to try and retrieve papers for

Papers will then be retrieved and stored within a new folder in the location where the script is being run from.

## Errors
* If you encounter a 401 Unauthorized Error your Aber Credentials (username/password) are either incorrect or you do not have the necessary permissions to view the document.

## License

[GNU General Public License v3.0](https://github.com/maw101/Aber-Past-Paper-Retriever/blob/master/LICENSE)
