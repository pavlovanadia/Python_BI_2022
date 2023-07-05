#!/usr/bin/env python3

import requests
from dataclasses import dataclass
from typing import List
import argparse
import sys


@dataclass
class Intron:
    order: int
    start: int
    end: int


@dataclass
class Exon:
    order: int
    start: int
    end: int


@dataclass
class GenscanOutput:
    status: str
    cds_list: List[str]
    intron_list: List[Intron]
    exon_list: List[Exon]


def load_sequence_from_file(sequence_file):
    with open(sequence_file, "r") as f:
        sequence = f.read()
    return sequence


def run_genscan(
        sequence=None, 
        sequence_file=None, 
        organism="Vertebrate", 
        exon_cutoff=1.00, 
        sequence_name="",
        print_options="Predicted peptides only"
        ):
    if sequence_file is None and sequence is None:
        raise ValueError("Sequence or sequence file must be specified")
    PRINT_OPTION_1 = "Predicted peptides only"
    PRINT_OPTION_2 = "Predicted CDS and peptides"
    ALLOWED_PRINT_OPTIONS = {PRINT_OPTION_1, PRINT_OPTION_2}
    if print_options not in ALLOWED_PRINT_OPTIONS:
        message = f"Error! --print_options must be one of the {ALLOWED_PRINT_OPTIONS}. Got {print_options}."
        raise ValueError(message)
    
    ORGANISM_OPTIONS = {"Vertebrate", "Arabidopsis", "Maize"}
    if organism not in ORGANISM_OPTIONS:
        message = f"Error! --organism must be one of the {ORGANISM_OPTIONS}. Got {organism}."
        raise ValueError(message)
    
    EXON_CUTOFF_OPTIONS = {1.0, 0.5, 0.25, 0.1, 0.05, 0.02, 0.01}
    if exon_cutoff not in EXON_CUTOFF_OPTIONS:
        message = f"Error! --exon_cutoff must be one of the {EXON_CUTOFF_OPTIONS}. Got {exon_cutoff}."
        raise ValueError(message)
    

    url = "http://hollywood.mit.edu/cgi-bin/genscanw_py.cgi"
    data = {
        "-o": organism,
        "-e": exon_cutoff,
        "-n": sequence_name,
        "-p": print_options,
    }

    if sequence:
        data["-s"] = sequence
    elif sequence_file:
        data["-s"] = load_sequence_from_file(sequence_file)

    response = requests.post(url, data=data)
    response_text = response.text
    status_code = response.status_code

    intron_list = []
    exon_list = []

    cds_list = []
    peptise_start = ">/tmp/"
    inside_cds = False
    prot_end = "</pre>"
    cds = ""

    for line in response.text.split("\n"):
        if line.startswith(" "):
            columns = line.split()
            if len(columns) >= 9 and columns[1] in ["Intr", "Init", "Term"]:
                start = int(columns[3])
                end = int(columns[4])
                order = int(columns[0].split(".")[1])
                exon_list.append(Exon(order=order, start=start, end=end))
        
        if line.startswith(peptise_start):
            inside_cds = True
        elif line.startswith(prot_end):
            cds_list.append(cds)
            cds = ""
            inside_cds = False
        elif inside_cds:
            cds += line

    if len(exon_list) <= 1: # no introns found
        pass
    else:
        for i in range(1, len(exon_list)):
            prev_exon = exon_list[i - 1]
            curr_exon = exon_list[i]
            order = i
            start = prev_exon.end + 1
            end = curr_exon.start - 1
            intron_list.append(Intron(order=order, start=start, end=end))

    genscan_output = GenscanOutput(
        status=status_code,
        cds_list=cds_list,
        intron_list=intron_list,
        exon_list=exon_list
    )

    return genscan_output

def parse_args():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--sequence",
        "-s",
        type=str,
        default=None,
        help="String representation of sequence."
    )
    ap.add_argument(
        "--sequence_file",
        "--sf",
        type=str,
        default=None,
        help="File with sequence."
    )
    ap.add_argument(
        "--organism",
        "-o",
        default="Vertebrate",
        help="Organism."
    )
    ap.add_argument(
        "--exon_cutoff",
        "-e",
        default=1.0,
        type=float,
        help="Exon cutoff parameter."
    )
    ap.add_argument(
        "--sequence_name",
        "-n",
        default="",
        help="Sequence name."
    )
    ap.add_argument(
        "--print_options",
        "-p",
        default="Predicted peptides only",
        help="Print option parameter."
    )

    if len(sys.argv) < 2:
        ap.print_help()
        sys.exit(0)
    args = ap.parse_args()
    if args.sequence is None and args.sequence_file is None:
        print("Error, aequence or aequence file must be specified.")
        sys.exit(0)
    return args


if __name__ == "__main__":
    args = parse_args()
    result = run_genscan(
        sequence=args.sequence,
        sequence_file=args.sequence_file,
        organism=args.organism,
        exon_cutoff=args.exon_cutoff,
        sequence_name=args.sequence_name,
        print_options=args.print_options
    )
    print(result)
