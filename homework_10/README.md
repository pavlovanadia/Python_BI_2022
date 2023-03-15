# Iterators and Decorators #

Task dedicated to iterators and decorators in python3.

## File content ##

Tasks and description of classes and functions for each task:

> Task 1: create ***MyDict*** class 

- *MyDict* - class that fully imitates *dict* class, but while iterating it returns both keys and values.

> Task 2: create ***iter_append*** function

- *iter_append* - function that takes two arguments: iterator and item; while iterating returns all iterator elements and item in the end.

> Task 3: make two classes return objects of their own type but not their parent's type

- *MyString* - class.
- *MySet* - class.

> Task 4: make the decorator ***switch_privacy***

- *switch_privacy* - class decorator that switches all public methods of a class to private methods of a class; all private methods of a class to public methods of a class; protected methods and dunder methods do not change.

> Task 5: make the context manager ***OpenFasta***

- *FastaRecord* - dataclass, contains sequence, id and descroption of the record.  
- *OpenFasta* - context manager that takes path to file; had method *read_record()* and *read_records()* that are analogical to readline() and readlines() of open context manager. read_record* and *read_records* return FastaRecord object.

> Task 6: get all possible non-unique offspting genotypes by combining parents' alleles

> **Example**: non-unique crossing of Aa and Aa parents will be AA, Aa, Aa, aa.

- *Alleles* - class for alleles for one gene and probability of one-gene genotype. 
    - Attributes: *first*, *second*, *p* (probabiblity, default=1.0).
    - *combinations* - method that takes two instances of Alleles class and returns a list of Alleles objects, each of which represents one-gene genotype of offspring. **Eg**: par1.combinations(par2).
- *Genotype* - class for alleles of several genes.
    - *get_alleles* - method to unfold string representation of genotype into list of Alleles instances.
    - *mate* - method to combine genotypes of two individuals, returns only list of lists of possible one-gene genotypes for all genes.
    - *startswith* - method to check if the genotype of an individuals corresponds to prefix (Genotype class object as well).
    - *gtype_prob* - method to extract the probability of current genotype according to probabilities of each gene allele combinations.
- *combinations* - recursive function that takes list of lists of one-gene alleles for several genes and yields all genotype combinations.
- *unique_gtypes* - function that takes list of lists of possible one-gene genotypes for all genes and returns all possible unique genotypes.
- *non_unique_gtypes* - function that takes list of lists of possible one-gene genotypes for all genes and returns all possible non-unique genotypes.
- *unique_offspring* - function that takes two string representations of both parents' genotypes and returns all unique offspring genotypes.
- *non_unique_offspring* - function that takes two string representations of both parents' genotypes and returns all non-unique offspring genotypes.
- *get_offspring_genotype_probability* - function that takes string representations of parents' and offspring genotypes and returns probability of such offspring if crossing both parents.

## Installation and usage ##

The Jupyter Notebook code was written using and is recommended to be run using Ubuntu OS 22.04.1 LTS version Python 3.9.12 with VSCode.

No external libraries needed.

You can download the whole repository including Python script, Jupyter Notebook, data folder with test .fasta file executing the following command:

`git clone <repository url>`
