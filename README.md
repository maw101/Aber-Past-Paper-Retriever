# Aber Uni Past Paper Retriever
Fetches all Aberystwyth University Past Paper PDFs for a given module.

[CLI](src/aber_past_paper_retriever_cli.py) and [GUI](src/aber_past_paper_retriever_gui.py) interfaces provided.

The underlying [paper retriever class](src/aber_past_paper_retriever.py) supports retrieval operations.

Past Papers are stored at [aber.ac.uk/en/past-papers/](https://www.aber.ac.uk/en/past-papers/).

## Requirements
* [Python 3](https://www.python.org/downloads/) (utilises os, datetime, getpass libraries)
* [Python 3 Requests](https://pypi.org/project/requests/) Library
* [lxml.html](https://lxml.de/lxmlhtml.html)

## Usage
### aber_past_paper_retriever_cli.py
Once the requirements are satisfied:

Clone or download the project to your machine.

Then in a terminal window run:

```sh
python3 aber_past_paper_retriever_cli.py
```

1) Enter Aberystwyth University Username
2) Enter Account Password
3) Enter your departments past paper page URL [Go to this page](https://www.aber.ac.uk/en/past-papers/) and click on your department.
4) Enter the Module Code - eg PH01010, CS23820, or HQ33220

Papers will then be retrieved and stored within a new folder in the location where the script is being run from.

#### Example 1
This example is for a Computer Science Module with Module Code CS26520.

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

#### Example 2
This example is for an International Politics Module with Module Code IQ30320.

```text
Enter Aberystwyth Username: 
Enter Aberystwyth Password: 
Enter your Department URL from the past papers URL (see README file, leave blank for compsci): https://www.aber.ac.uk/en/past-papers/interpol/
Enter Module Code: IQ30320

Retrieving Papers for IQ30320
Retrieved PDF from URL: https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/interpol/sem1-19/IQ30320-19.pdf
Retrieved PDF from URL: https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/interpol/sem1-18/IQ30320-18.pdf
Retrieved PDF from URL: https://www.aber.ac.uk/en/media/departmental/examinations/pastpapers/pdf/interpol/sem2-16/IQ30320-16.pdf

All Semesters Checked. Check folder for any downloaded papers.

Press Enter to EXIT the program, any other input will allow you to enter another module!
```

### aber_past_paper_retriever_gui.py
Once the requirements are satisfied:

Clone or download the project to your machine.

Then in a terminal window run:

```sh
python3 aber_past_paper_retriever_gui.py
```

This will run the GUI interface for the retriever.

![](README_ASSETS/gui_example_1.png)

Provide options for each field in turn starting with the first.

Any errors encountered will be shown to the user.

## Errors
* If you encounter a 401 Unauthorized Error your Aber Credentials (username/password) are either incorrect or you do not have the necessary permissions to view the document.

## License

[GNU General Public License v3.0](https://github.com/maw101/Aber-Past-Paper-Retriever/blob/master/LICENSE)
