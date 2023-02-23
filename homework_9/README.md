# Classes in Python #

*classes.ipynb* that could be found in this folder is a playground with Python3 classes functional.

## Installation and usage ##

The Jupyter Notebook code was written using and is recommended to be run using Ubuntu OS 22.04.1 LTS version Python 3.9.12 with VSCode.

You can download the whole repository including Python script, Jupyter Notebook, requirements, original file with ftp links and original text file executing the following command:

`git clone <repository url>`

**Please note that in this notebook external library numpy is used. For correct notebook run please install the requirements to your virtual environment**

For these purposes please execute the following commands in you command line (originally executed with Ubuntu OS 22.04.1 LTS version):

`python3 -m venv environment # creation of virtual environment`

`source environment/bin/activate # activation of virtual environment`

If you wish to run the script as Jupyter Notebook and use VSCode, the recommended additional commands are:

`pip3 install ipykernel`

`python3 -m ipykernel install --user --name=projectname`

Then reload VSCode and choose the correct Kernel (will contain the name of your project)

Upload the requirements to your virtual environment:

`pip install -r requirements.txt`

To deactivate your environment use

`deactivate`


## Notebook content ##

### Task 1 ###

**Chat** is a class that has:
- chat_history - attribute that stores all messages in reverse chronological order
- show_last_message - method that prints the information regarding the last message
- get_history_from_time_period - method that takes two optional arguments in datetime format that define the period of the messages to be returned as a Chat object
- show_chat - method that prints all chat messages
- receive - method for receiving messages

**Message** is a class that has:
- text - attribute that is the text of a message
- datetime - attribuute with date and time of the message to be received by Chat object
- user - attribute with user information
- show - method that prints message information
- send - method to send a message to Chat object

**User** is a class that has the following attributes:
- username
- name
- lastname
- status
- birthdate

### Task 2 ###

**Args** is a class that contains arguments and calls for a function with << symbol.

### Task 3 ###

**StrangeFloat** is the class of a parent **float** class that has all **float** attributes and at the same time realises the functional <action>_<number> with the following actions: *add*, *subtract*, *multiply*, *divide*.

### Task 4 ###

No class in this task it just plays with dunders.

### Task 5 ###

**BiologicalSequence** is the class that has abstract methods:
- __len__
- __getitem__
- __str__
- is_valid_alphabet

**BioSeqInterface** is the child **BiologicalSequence** class, an intermediate class for realization of **BiologicalSequence** methods.

**NucleicAcidSequence** is the child **BioSeqInterface** class that has:
- is_valid_alphabet - method to check whether the nucleotide content is ok
- complement - method to get the complement sequence
- gc_content - method for countinggc content of sequence

**AminoAcidSequence** is the child **BioSeqInterface** class that has:
- is_valid_alphabet - method to check whether the aminoacid sequence is ok
- molecular_weight - method for counting the sum of molecular weights of all aminoacids

**DNASequence** is the child **NucleicAcidSequence** class that has:
- transcribe - method for DNA to RNA transcription

**RNASequence** is the child **NucleicAcidSequence** class that has:
- reverse_transcribe - method for RNA to DNA transcription
