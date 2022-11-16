# Regular expressions project #

### This project is dedicated to regular expressions usage. Here you can find possibly useful regular expressions and functions ###

The script is organized in tasks.

## Tasks description ##

- **Task 1** Extract all ftp links from file *references.txt* to a file *ftps*. Note that you will also get the file *unique_ftps* where all links are unique and do not repeat.
- **Task 2** Extract all numbers from the file 2430AD.txt and print them on the screen.
- **Task 3** Extract all words with letter A (irregardlessly of the register) from the file 2430AD.txt and print them on the screen.
- **Task 4** Extract all exclamatory sentences from the file 2430AD.txt and print them on the screen.
- **Task 5** Build a histogram of unique words lenghts proportions from the file 2430AD.txt.
- **Task 6** Write a function to translate Russian language (string format only) to a mockery-Russian language (returns a string).
- **Task 7** Write a function for sentence of precise length extraction from the text. Please note that this function takes two arguments: text (str format only) and n (int format only) and returns a list of tuples with **only words** from sentences with n words. **No punctuation or quote symbols are saved. Numbers are not considered as words.** However, in-word hyphens and  aprostrophes are returned as far as they are considered as a part of the word.


## Installation and usage ##

You can download the whole repository including Python script, Jupyter Notebook, requirements, original file with ftp links and original text file executing the following command:

`git clone <repository url>`

This script is available in Jupyter Notebook *.ipynb* and Python3 script *.py* formats. It was written and is recommended to run with Python3.

**Please note that in this script external library *matplotlib* is used. For correct script usage please install the requirements to your virtual environment**

For these purposes please execute the following commands in you command line (originally executed with Ubuntu OS 22.04.1 LTS version):

`python3 -m venv environment` # creation of virtual environment

`source environment/bin/activate` # activation of virtual environment

If you wish to run the script as Jupyter Notebook and use VSCode, the recommended additional commands are:

`pip3 install ipykernel`

`python3 -m ipykernel install --user --name=projectname`

Then reload VSCode and choose the correct Kernel (will contain the name of your project)

Irregardlessly of your choice (*.ipynb* or *.py*) please upload the requirements to your virtual environment:

`pip install -r requirements.txt`

To deactivate your environment use

`deactivate`