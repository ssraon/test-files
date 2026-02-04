#!/usr/bin/env python3
"""
Convert tec_smith_contributions_1.csv to JSON format.
"""

import csv
import json
import sys

def convert_csv_to_json(csv_filename, json_filename):
    """
    Convert a CSV file to JSON format.
    
    Args:
        csv_filename: Path to the input CSV file
        json_filename: Path to the output JSON file
    """
    data = []
    
    print(f"Reading CSV file: {csv_filename}")
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        csv_file = None
        
        for encoding in encodings:
            try:
                csv_file = open(csv_filename, 'r', encoding=encoding, errors='replace')
                print(f"Using encoding: {encoding}")
                break
            except Exception:
                if csv_file:
                    csv_file.close()
                continue
        
        if csv_file is None:
            raise Exception("Could not open file with any supported encoding")
        
        with csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            for row_num, row in enumerate(csv_reader, start=1):
                data.append(row)
                
                # Print progress every 10000 rows
                if row_num % 10000 == 0:
                    print(f"Processed {row_num} rows...")
        
        print(f"Total rows processed: {len(data)}")
        print(f"Writing JSON file: {json_filename}")
        
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=2)
        
        print(f"Successfully converted {csv_filename} to {json_filename}")
        print(f"Output file size: {len(data)} records")
        
    except FileNotFoundError:
        print(f"Error: File '{csv_filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    csv_file = "tec_smith_contributions_1.csv"
    json_file = "tec_smith_contributions_1.json"
    
    convert_csv_to_json(csv_file, json_file)
