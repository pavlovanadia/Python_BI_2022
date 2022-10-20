#!/usr/bin/env python3

NUCLEOTIDES_ALLOWED = set("ATGCNatgcn") # set of allowed nucleotides for .fastq format
QUALITY_SYMBOLS_ALLOWED = set("!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHI") # set of allowed symbols for phred33


def format_check(read):
    """Function for checking whether the single reading is conform to .fastq format"""
    first_line_check = read[0][0] == "@" # does the first line start with "@"?
    second_line_check = set(read[1]).issubset(NUCLEOTIDES_ALLOWED) # are all nucleotides really A, T, G, C or N?
    third_line_check = read[2][0] == "+" # does a line for commentary exist?
    fourth_line_check = set(read[3]).issubset(QUALITY_SYMBOLS_ALLOWED) # is it really calculable using phred33?

    if first_line_check and second_line_check and third_line_check and fourth_line_check:
        return True
    else:
        return False


def gc_check(seq, bound):
    """Function for calculating whether GC-content is appropriate"""
    # borders setting in case only upper border is entered
    if type(bound) == int or type(bound) == float:
        min_bound = 0
        max_bound = float(bound)

    # borders setting in case two borders are entered
    elif type(bound) == tuple or type(bound) == list:
        min_bound = float(bound[0])
        max_bound = float(bound[1])
    
    # if border value is invalid, printing an ERROR message
    else:
        print("ERROR: border value for GC-content input is of invalid type.")
        print("Please input border value for GC-content using int or float type for onpy upper border or tuple or list type for lower and upper borders.")
        exit()

    # check for the valid border values 
    if not 0 <= min_bound <= max_bound <= 100:
        print("ERROR: border values for GC-content input are invalid.")
        print("Please note that border values could not be less than 0 and more that 100 and that lower border should be before upper border.")
        exit()

    # GC-content calculation
    gc_sum = 0
    for nucl in seq.upper():
        if nucl == "G" or nucl == "C":
            gc_sum += 1
    gc_content = gc_sum / len(seq) * 100

    # checking whether GC-content fints into borders
    if min_bound <= gc_content <= max_bound:
        return True
    else:
        return False


def length_check(seq, bound):
    """Function for checking whether sequence length is appropriate"""
    # borders setting in case only upper border is entered
    if type(bound) == int or type(bound) == float:
        min_bound = 0
        max_bound = float(bound)

    # borders setting in case two borders are entered
    elif type(bound) == tuple or type(bound) == list:
        min_bound = float(bound[0])
        max_bound = float(bound[1])

    # if border value is invalid, printing an ERROR message
    else:
        print("ERROR: border value for length input is of invalid type.")
        print("Please input border value for length using int or float type for onpy upper border or tuple or list type for lower and upper borders.")
        exit()
    
    # check for the valid border values 
    if not 0 <= min_bound <= max_bound <= 2**32:
        print("ERROR: border values for length input are invalid.")
        print("Please note that border values could not be less than 0 and more that 2**32 and that lower border should be before upper border.")
        exit()

    # checking whether sequence length is appropriate
    if min_bound <= len(seq) <= max_bound:
        return True
    else:
        return False


def quality_check(seq_qual, threshold):
    """Function for performing read quality check"""
    # check for the valid quality format
    if type(threshold) != int and type(threshold) != float:
        print("ERROR: threshold value input is of invalid type.")
        print("Please input threshold value using int or float type.")
        exit()
    
    # check for the valid threshold value 
    if not 0 <= threshold <= 40:
        print("ERROR: threshold input value is invalid.")
        print("Please note that threshold value could not be less than 0 and more that 40.")
        exit()

    # creating variable to sum up the Q-scores
    q_scores_sum = 0 # here i've decided to sum the Q-scores asap instead of appending Q-scores to the list for memory economy 

    # converting phred33 to Q-scores and summing them up
    for val in seq_qual:
        q_scores_sum += (ord(val) - 33) 
    
    # checking whether the mean read quality is appropriate
    return q_scores_sum / len(seq_qual) >= threshold


def write_good(reading, file_name):
    """Function for writing appropriate readings to a file"""
    # making the filename for readings that passed
    suffix = "{}_passed.fastq"
    passed_file_name = suffix.format(file_name)

    # writing the fastq reading to a passed file
    f = open(passed_file_name, "a")
    for i in reading:
        f.write(i + "\n")
    f.close()


def write_bad(reading, file_name):
    """Function for writing inappropriate readings to a file"""
    # making the filename for readings that failed
    suffix = "{}_failed.fastq"
    failed_file_name = suffix.format(file_name)

    # writing the fastq reading to a failed file
    file = open(failed_file_name, "a")
    for line in reading:
        file.write(line + "\n")
    file.close()            


def main(
    input_fastq, 
    output_file_prefix, 
    gc_bounds=(0, 100), 
    length_bounds=(0, 2**32),
    quality_threshold=0, 
    save_filtered=False):
    """main function for file reading"""
    # file opening and writing each 4 lines to buffer
    with open(input_fastq, 'r') as inp:
        buff = []
        buff_counter = 0
        for line in inp:
            buff.append(line.strip())
            if len(buff) != 4:
                continue # collecting 4 lines of fastq reading to a list

            # checking if the reading in buffer is conform to .fastq format
            buff_counter += 1 # number of fastq readings
            if format_check(buff) == False:
                print("ERROR: at least one of your readings is not conform to .fastq format.")
                print("The number of the first wrong reading is {}.".format(buff_counter))
                print("For expected function performance we recommend you to check your input file and delete incorrect output file or files so that it would not affect the result.")
                exit()

            # checking fastq reading whether GC-content, sequence length and quality are appropriate
            if (gc_check(buff[1], bound=gc_bounds) and 
                length_check(buff[1], bound=length_bounds) and 
                quality_check(buff[3], int(quality_threshold))):

                write_good(buff, output_file_prefix) # writing appropriate fastq readings

            elif save_filtered == True:
                write_bad(buff, output_file_prefix) # writing inappropriate fastq readings

            buff = [] # buffer clearing after processing