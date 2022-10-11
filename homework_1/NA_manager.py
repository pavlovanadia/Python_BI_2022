#!/usr/bin/env python3

# Command information
print("""Welcome to the NA manager.
Please enter the command and then enter the sequence.
Command list to choose from is below.

exit - if you want to terminate the program
transcribe - transcribes DNA to RNA
reverse - reverses DNA or RNA sequence
complement - prints the complement sequence
reverse complement - prints the reverse complement sequence
""")

# Dictionary for DNA complement
d2d = {
    "a": "t",
    "t": "a",
    "g": "c",
    "c": "g",
    "A": "T",
    "T": "A",
    "G": "C",
    "C": "G"
}

# Dictionary for RNA complement
r2r = {
    "a": "u",
    "u": "a",
    "g": "c",
    "c": "g",
    "A": "U",
    "U": "A",
    "G": "C",
    "C": "G"
}

# Input and checking for the right sequence
def input_check():
    sequence = input("Enter the sequence: ")
    if "t" in sequence.lower() and "u" in sequence.lower():
        print("Error: your sequence contains both t and u. Please reenter the sequence.")
        sequence = input_check()
        return sequence
    elif not set(sequence.lower()).issubset({"a", "t", "u", "g", "c"}):
        print("Error: your sequence contains non-nucleotide symbols. Please reenter the sequence.")
        sequence = input_check()
        return sequence
    else:
        return sequence

# Transcription function
def transcribe(seq):
    return seq.replace("t", "u").replace("T", "U")

# Function to specify DNA or RNA
def dorr(seq):
    ans = ""
    if "t" in seq.lower():
        ans = "DNA"
    elif "u" in seq.lower():
        ans = "RNA"
    else:
        while ans != "DNA" and ans != "RNA":
            ans = input("Please specify the type of nucleic acid. It might be important for you (DNA/RNA): ").upper()
    return ans 


# Complement function
def complement(seq):
    res = [] # list for faster nucleotide appending to the result sequence
    kind = dorr(seq) 
    if kind == "DNA":
        for nucl in seq:
            res.append(d2d[nucl])
    elif kind == "RNA":
        for nucl in seq:
            res.append(r2r[nucl])
    else:
        print("COMPLETE ERROR PLEASE CONTACT THE REPOSITORY AUTHOR")
        exit
    return "".join(res)

# Reverse complement function
def rev_compl(seq):
    res = [] # list for faster nucleotide appending to the result sequence 
    kind = dorr(seq) 
    if kind == "DNA":
        for nucl in seq:
            res.append(d2d[nucl])
    elif kind == "RNA":
        for nucl in seq:
            res.append(r2r[nucl])
    else:
        print("COMPLETE ERROR PLEASE CONTACT THE REPOSITORY AUTHOR")
        exit
    return "".join(res)[::-1]

while True:
    comm = input("Enter command: ")
    if comm.lower() == "exit":
        break
    elif comm.lower() not in set(["transcribe", "reverse", "complement", "reverse complement"]):
        print("There is no such command. Please reenter the command.")
        continue
    seq = input_check()
    if comm.lower() == "transcribe":
        if "u" in seq.lower():
            print("Error: you can not transcribe RNA. Please reenter the sequence.")
            seq = input_check()
        print(transcribe(seq))
    elif comm.lower() == "reverse":
        print(seq[::-1])
    elif comm.lower() == "complement":
        print(complement(seq))
    elif comm.lower() == "reverse complement":
        print(rev_compl(seq))
        
print("Thanks for using the NA manager.")