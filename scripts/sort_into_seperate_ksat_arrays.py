import json

def read_json_file(input_path):
    """Reads a JSON file and returns the data."""
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    return data

def process_data(wr_data, ksat_data):
    """
    Placeholder for processing logic.
    Modify this function based on your data structure and processing needs.
    """
    # Find all of the specific statement types
    for wr in wr_data:
        # Find objects where 'data_list' contains the value 5
        matching_objects = [obj for obj in ksat_data if wr["_id"] in obj["work_roles"] and obj["type"] == "knowledge"]
        wr["knowledge_statements"] = []
        for obj in matching_objects:
            wr["knowledge_statements"].append(f'{obj["element_id"]}: {obj["description"]}')

        matching_objects = [obj for obj in ksat_data if wr["_id"] in obj["work_roles"] and obj["type"] == "skill"]
        wr["skill_statements"] = []
        for obj in matching_objects:
            wr["skill_statements"].append(f'{obj["element_id"]}: {obj["description"]}')

        matching_objects = [obj for obj in ksat_data if wr["_id"] in obj["work_roles"] and obj["type"] == "ability"]
        wr["ability_statements"] = []
        for obj in matching_objects:
            wr["ability_statements"].append(f'{obj["element_id"]}: {obj["description"]}')
        
        matching_objects = [obj for obj in ksat_data if wr["_id"] in obj["work_roles"] and obj["type"] == "task"]
        wr["task_statements"] = []
        for obj in matching_objects:
            wr["task_statements"].append(f'{obj["element_id"]}: {obj["description"]}')
    
    return wr_data

def write_json_file(output_path, data):
    """Writes data to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    wr_input_file = 'dcwf/raw/work_roles.json'
    ksat_input_file = 'dcwf/raw/ksats.json'
    output_file = 'work_roles_just_knowledge.json'

    wr_raw_data = read_json_file(wr_input_file)
    ksat_raw_data = read_json_file(ksat_input_file)
    processed_data = process_data(wr_raw_data, ksat_raw_data)
    write_json_file(output_file, processed_data)

    print(f"Processed data has been written to {output_file}")
