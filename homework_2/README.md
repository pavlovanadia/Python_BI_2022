# fastq_filtrator module usage #
## Repository information ##

**fastq_filtrator** is a module for filtering .fastq files according to their sequence length, GC-content and reading quality. Please note that **fastq_filtrator** accepts only .fastq file and produces .fastq file or files with readings according to their correspondance to the parameters that you have set.

### Functional ###

**main** - the key function of the module

The arguments of the function are listed below:

- *input_fastq* - argument for the path to your input file. Please note that this file should be in **.fastq format only** and that sequence quality should be measured in terms of **phred33 scale only**

- *output_file_prefix* - argument for the prefix of your output file. For the readings that meet your requirements the suffix "*_passed.fastq*" would be added. For the readings that do not meet the requirements the suffix "*_failed.fastq*" would be added.

- *gc_bounds* - argument for expected percent of **GC-content** of your readings. The **default value is (0, 100)** and accepts all readings according to their GC-content. This argument can accept either a single value (**int or float only**) and in that case will interpret it as an upper bound or two values (**tuple or list only**) and in that case will interpret them as a lower and upper bounds respectively. Please pay attention: *gc_bounds* takes GC-content in **percents** and **includes** both lower and upper bounds as appropriate GC-content for reading. Please note that if your values will not meet the expected format, you will get an ERROR message.

- *length_bounds* - argument for expected **length** of your readings. The **default value is (0, 2\*\*32)**. This argument can accept either a single value (**int or float only**) and in that case will interpret it as an upper bound or two values (**tuple or list only**) and in that case will interpret them as a lower and upper bounds respectively. Please pay attention: *length_bounds* **includes** both lower and upper bounds as appropriate reading length. Please note that if your values will not meet the expected format, you will get an ERROR message.

- *quality_threshold* - argument for **mean quality threshold** of your readings. The default value is 0. This argument can accept only a single value (**int or float only**). All readings with mean reading quality less that threshold values will be considered as failed. Please note that if your values will not meet the expected format, be less that 0 or more than 40, you will get an ERROR message.

- *save_filtered* - if this argument is False which is default value then you will get only one file with readings that have passed this filter. If this argument is True then you will get an **additional file** with readings that have not passed this filter.

### File requirements: ###
- **.fastq** format only
- sequence quality measured in terms of **phred33** scale only

**Please note that if at least one of the readings in your input file does not correspond to .fastq format you are going to have an ERROR message**
An **ERROR** message might occur if:
- the first symbol of the first line in any reading is different from @
- any of the symbols in the second line in any reading is different from A, T, G, C or N
- the first symbol of the third line in any reading is different from +
- any of the symbols in the fourth line in any reading is different from symbols used in phred33 scale

**If an ERROR has occured**
If you have an ERROR message we recommend you to pay attention to the *first* reading that does not correspond to the file format requirements. The number of that reading would be written below the ERROR message. One of the requirements above have not been met by that reading, so we recommend you to check it thoroughly and correct the mistake or delete the reading with incorrect format is the problem could not be solved. After that you should *delete* the files that have been already created with previous readings and try again. 

## Installation and usage ##
To run NA manager you need to have any environment that supports Python3 installed.