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

Upcoming update - I'm taking in assumptions that the UPC count will be the same between 2 files, but will be updating error handling in case they are different. Pandas requires that dataframes are the same to actually compare them.
