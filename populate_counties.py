#!/usr/bin/env python3
"""
Populate county fields in JSON records based on zip code and state.
"""

import json
import zipcodes
import sys

def populate_counties(json_filename, output_filename=None):
    """
    Populate county fields in JSON records based on zip code.
    
    Args:
        json_filename: Path to the input JSON file
        output_filename: Path to the output JSON file (defaults to overwriting input)
    """
    if output_filename is None:
        output_filename = json_filename
    
    print(f"Loading JSON file: {json_filename}")
    
    try:
        with open(json_filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Total records: {len(data)}")
        print("Populating county fields...")
        
        updated_count = 0
        not_found_count = 0
        cache = {}  # Cache zip code lookups for better performance, key: (zipcode, state)
        
        for i, record in enumerate(data):
            if (i + 1) % 10000 == 0:
                print(f"Processed {i + 1} records... (Updated: {updated_count}, Not found: {not_found_count})")
            
            zipcode = record.get('Zip', '').strip()
            state = record.get('State', '').strip()
            
            if not zipcode:
                continue
            
            # Use composite cache key for state-specific lookups
            cache_key = (zipcode, state)
            
            # Check cache first
            if cache_key in cache:
                county = cache[cache_key]
            else:
                # Look up the county
                county = None
                try:
                    results = zipcodes.matching(zipcode)
                    
                    if results:
                        # If state is provided, try to match it
                        if state:
                            for result in results:
                                if result.get('state', '').upper() == state.upper():
                                    county = result.get('county', '')
                                    break
                        
                        # If no state match or state not provided, use first result
                        if county is None and results:
                            county = results[0].get('county', '')
                except ValueError:
                    # Invalid zip code format, skip
                    pass
                
                # Cache the result (even if None)
                cache[cache_key] = county
            
            # Update the record if county was found
            if county:
                record['County'] = county
                updated_count += 1
            else:
                not_found_count += 1
        
        print(f"\nTotal records processed: {len(data)}")
        print(f"Counties populated: {updated_count}")
        print(f"Counties not found: {not_found_count}")
        
        print(f"\nWriting updated JSON file: {output_filename}")
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"Successfully updated {output_filename}")
        
    except FileNotFoundError:
        print(f"Error: File '{json_filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    json_file = "tec_smith_contributions_1.json"
    populate_counties(json_file)
