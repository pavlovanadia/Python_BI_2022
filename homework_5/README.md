# Homework on pandas and visualization #


function `read_gff` takes path to a gff file and reads it returning pandas dataset

function `read_bed6` takes path to a bed6 file and reads it returning pandas dataset

then there is a piece of code that shortens the information in the attributes column to just rRNA type

For each chromosome the number of each rRNA type is counted and visualised as a barplot

And then in # task 4 a bedtools intersect tool is realised

Then there is volcano plot (task 5) built on the data of gene expressions, it visualizes significance and direction of gene expression change

After that in task 6 a pie chart is made

Task 7 was EDA analysis of coved data

### Installation and usage ###

I recommend using python3 and virtual environment

`python3 -m venv environment`

`source environment/bin/activate`

Please install the requirements.txt. `pip install -r requirements.txt`

For that clone the repository (you will also get the datasets used) `git clone <repository url>`

If you wish to use Jupyter notebook please make sure that you set your Kernel to the virtual environment

`pip3 install ipykernel`

`python3 -m ipykernel install --user`