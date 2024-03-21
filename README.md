# Inventory Comparison

This is a quick and simple comparison between 2 inventory files.

_Note - They both need to be csv files._

1. Create the virtual environment.
   `python -m venv venv`

2. Source into the virtual environment.
   `source venv/bin/activate`

3. Install requirements.
   `pip install -r requirements.txt`

4. Run the program.
   `python main.py`

## How to use

Upon running the program you will be given a choice of 5 options.

1.  Compare inventory files to see percent increase or decrease in specific UPCs.

- This will compare 2 inventory csv files to check for percent increase or decrease with regards to specific UPCs. This will output to the inventory_comparisons directory.

2.  Compare inventory files to see UPCs that are missing from either file.

- This will compare 2 inventory files to check for missing UPCs, and will report which file that UPC is missing from in a separate column. This will output to the upc_comparisons directory.

3.  Parse through edi files to create a csv of contained UPCs for comparison in one of other methods.

- This will parse through a singular edi file and give you a csv of the UPCs contained inside of it. The output will be in the edi_to_csv directory.

4.  Give a length value for the active products in the inventory file in question.

- This will print out the length of the inventory file in question to the console for a quick analysis.

5.  Parse through a directory of edi files to create csvs of contained UPCs for comparison in one of the other methods.

- This will parse the directory you input and create a batch of csv files with the UPCs in the edi files within the batch_edi_to_csv directory.
