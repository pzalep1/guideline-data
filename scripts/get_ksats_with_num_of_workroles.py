import json

def read_json_file(input_path):
    """Reads a JSON file and returns the data."""
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    return data

def process_data(ku_data, top_range):
    """
    Placeholder for processing logic.
    Modify this function based on your data structure and processing needs.
    """
    print_ksats = []
    for ksat in ku_data:
        if len(ksat["work_roles"]) >= top_range - 1 and len(ksat["work_roles"]) <= top_range:
            print_ksats.append(ksat)
    
    return print_ksats

def write_json_file(output_path, data):
    """Writes data to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    wr_input_file = 'nice/ksat_with_work_role_names.json'

    ku_raw_data = read_json_file(wr_input_file)
    i = 72
    while i > 0: 
        output_file = f'nice/nice_ksats_with_{i}_work_roles.json'
        print(i)
        processed_data = process_data(ku_raw_data, i)
        if len(processed_data) > 0:
            write_json_file(output_file, processed_data)
        i = i - 1

    print(f"Processed data has been written to {output_file}")