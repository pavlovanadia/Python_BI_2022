# Internet #

Task dedicated to Internet surfing using Python3.

## Repository content ##

This repository contains *HW_3.ipynb* Jupyter Notebook file with completed tasks and is accompanied with *genscan_module.py* which contains function to use GENSCAN online tool, *requirements.txt*, *OAS1.txt*  protein gene test file for GENSCAN online tool utilite and *movies.tsv* file with parsed top-250 movies according to IMDb.

## Task 1 ##

Task is dedicated to IMDb top-250 movies parsing and analysis:
* top-4 movies by rating
* top-4 years by mean movie rating
* barplot with top directors that have more than 2 movies in top sorted by movie number
* top-4 directors according review number
* *movies.tsv* file creation with all 250 movies

## Task 2 ##

Task is dedicated to decorator *telegram_logger* creation that logs decorated functions and sends the report with function name, function runtime and errors if occured to telegram chatbot.

## Task 3 ##

*genscan_module* Python API creation, also realised as console utilite. GENSCAN tool finds and cuts introns from nucleotide sequence.
*genscan_module* has **run_genscan** function that takes the following arguments (or this module can takes these arguments from console as well):

* sequence - string representation of DNA sequence, default is None.
* sequence_file - file qith DNA sequence, default is None.

`Please note that either sequence or sequence_file must be defined.`

`Please note that your sequence_file can contain just text representation of DNA sequence or be a FASTA file (example file is of the first type).`

`Please note that if your sequence_file contains more than one FASTA records, GENSCAN will join them and consider as one DNA sequence.`

* organism - default "Vertebrate", can be changed to "Arabidopsis" or "Maize".
* exon_cutoff - exon cutoff option, default 1.0, can be changed to 0.5, .025, 0.1, 0.05, 0.02, 0.01.
* sequence_name - does not affect the output nor via API, neither if using the online tool.
* print_options - default "Predicted peptides only", can be sqitched to "Predicted CDS and peptides", is not used in the API, because it foocuses on the predicted peptide and its structure exclusively.

## Installation and usage ##

The Jupyter Notebook and python file module were written using and is recommended to be run using Ubuntu OS 22.04.1 LTS version Python 3.9.12 with VSCode.

To clone the repositore to your local machine:

`git clone <repository url>`

External libraries were used, so *requirements.txt* upload is necessary for the correct code execution.

`pip install -r requirements.txt`

