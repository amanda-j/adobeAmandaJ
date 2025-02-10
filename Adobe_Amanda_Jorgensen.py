import argparse
import json
import os
from datetime import datetime

def remove_duplicates(input_data):
    changes_made = []
    to_keep = {}

    records = input_data['leads']

    for i, record in enumerate(input_data['leads']):
        record_id = record['_id']
        record_email = record['email']
        record_date =  datetime.fromisoformat(record['entryDate'])

        existing_key = record_email if record_email in to_keep else record_id if record_id in to_keep else None
        
        if existing_key:
            prev_index = to_keep[existing_key]
            prev_record = input_data['leads'][prev_index]
            prev_record_date = datetime.fromisoformat(prev_record['entryDate'])

            if record_date >= prev_record_date:
                if prev_record['_id'] in to_keep:
                    del to_keep[prev_record['_id']]
                if prev_record['email'] in to_keep:
                    del to_keep[prev_record['email']]
                to_keep[record_email] = i
                to_keep[record_id] = i
                changes_made.append({'duplicate': existing_key, 'deleted_record': prev_record, 'kept_record': record})
            else:
                # if prev_record_date is after record_date, then we keep prev_record and remove the current record 
                changes_made.append({'duplicate': existing_key, 'deleted_record': record, 'kept_record': prev_record})
        else:
            to_keep[record_email] = i
            to_keep[record_id] = i

        output_list = [records[x] for x in range(len(records)) if x in to_keep.values()]
        output_data = {'leads': output_list}

    return [output_data, changes_made]

def main():
    parser = argparse.ArgumentParser(description="Remove duplicate entries in JSON file.")
    parser.add_argument("input_file", type=str, help="Enter path to JSON file")
    
    args = parser.parse_args()

    try:
        # read in uploaded json file
        with open(args.input_file, "r", encoding="utf-8") as uploaded_file:
            data = json.load(uploaded_file)

        # remove duplicate records 
        updated_data = remove_duplicates(data)

        create_log_file = {'source': data, 'output': updated_data[0], 'changelog': updated_data[1]}

        # create file name
        input_filename = os.path.splitext(args.input_file)[0]  # remove extension
        output_filename = f"{input_filename}_output.json"
        log_filename = f"{input_filename}_log.json"

        # create output file
        with open(output_filename, "w", encoding="utf-8") as output_file:
            json.dump(updated_data[0], output_file, indent=4)

        # create log file
        with open(log_filename, "w", encoding="utf-8") as log_file:
            json.dump(create_log_file, log_file, indent=4)

        print(f"Processed JSON saved to {output_filename}; {log_filename} contains a record of the original JSON, processed JSON, and which records were removed")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()