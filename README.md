This command-line program processes a JSON file containing number of identically structured records and removes duplicates based on the following rules:

1) The most recent record (by date) is preferred.
2) Duplicates are identified based on matching IDs or emails. Both must be unique in the final dataset.
3) If dates are identical, the last record in the list is preferred.

The program also creates a log containing the changes made during de-duplication, including the source record, the final output record, and field changes.


Usage:

Run the program with:
python3 Adobe_Amanda_Jorgensen.py <input_json_file>
Here, <input_json_file> is the path to the input JSON file containing records to be processed.
