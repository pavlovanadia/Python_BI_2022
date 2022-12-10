# UNIX tools in python3 #

In that folder you couls find several UNIX tools on Python 3.9.12.

## Functions and description ##

- **wc.py** - imitates the UNIX **wc** function. Counts the number of lines, words and bytes in the file. Can take three flags: -l (line count), -w (word count), -c (byte count). Without flags all three are considered as True by default. The command can take any number of files or work with input if no files were specified. Usage example: `./wc.py -l file.txt`
- **ls_beau.py** - imitates the UNIX **ls** function with output imitatind the **ls** UNIX tool. Prints all files and directories in the specified directory. Can take flag -a (hidden files/directories shown). The command can take any directory and work with wildcards. With no directory specified shows all files and directories in the current directory. Usage example: `./ls.py -a ~/*`. PLEASE NOTE that this function **does not** work correctly in pipe with further functions, thus is recommended as the command to exclusively look at the content of the specified directories.
- **ls_pipe.py** - imitates the UNIX **ls** function with output imitatind the **ls** UNIX tool. Prints all files and directories in the specified directory. Can take flag -a (hidden files/directories shown). The command can take any directory and work with wildcards. With no directory specified shows all files and directories in the current directory. Usage example: `./ls.py -a ~/*`. PLEASE NOTE that this function **does not** have the perfect output but works correctly in pipe with further functions, thus is recommended as the command for pipelines.
- **sort.py** - imitates the UNIX **sort** function. Takes no flags. Can take any number of files or read from command line input. Sorts the content lines in alphabetical order ingoring the lettercase; numbers before letters; if the line starts with "_", it will be sorted according to the first letter or number but before the line that starts with the same letter without "-". If several files are specified then their lines will be sorted together.
- **rm.py** - imitates the UNIX **rm** function. Takes the flag -r (recursive). Takes the path to the file or directory. -r flag is required to recursively remove the directory.
- **cat.py** - imitates the UNIX **cat** function. Takes the path to the file or reads from the input stream. Prints the specified content.

## Installation and usage ##

These functions were originally written and are recommended for usage using Ubuntu OS 22.04.1 LTS version Python 3.9.12 and are recommended to use likewise.

To get all the functions provided it is recommended to copy the repository to your local machine with the command `git clone git@github.com:pavlovanadia/Python_BI_2022.git` and go to the branch 8 with the command 'git checkout homework_8'.

The functions might be executable but it is recommended to make them executable locally using the following command `chmod +x <command_name>`.

The commands could be executed from the folder as following:

`./command_name.py`

To execute the commands from any folder please add them to your PATH variable.