import json

def read_json_file(input_path):
    """Reads a JSON file and returns the data."""
    with open(input_path, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    return data

def process_data(ku_data):
    """
    Placeholder for processing logic.
    Modify this function based on your data structure and processing needs.
    """
    # Find all of the specific statement types
    optional = [
        "AAL",
        "ACR",
        "ANT",
        "ALG",
        "ATC",
        "BCO",
        "BCD",
        "CCO",
        "CCR",
        "CPS",
        "CSE",
        "DBA",
        "DST",
        "DMS",
        "DAT",
        "DVF",
        "DCO",
        "DFS",
        "EBS",
        "FAC",
        "FMD",
        "FPM",
        "HRE",
        "HFS",
        "HOF",
        "IAA",
        "IAC",
        "IAS",
        "ICS",
        "IDR",
        "ITC",
        "IDS",
        "LCS",
        "LLP",
        "MEF",
        "MOT",
        "NWF",
        "NSA",
        "NTP",
        "OSA",
        "OSH",
        "OST",
        "PBE",
        "PTT",
        "PRI",
        "QAT",
        "RFP",
        "SPP",
        "SAS",
        "SRE",
        "SSA",
        "SCS",
        "SCA",
        "SPG",
        "SSE",
        "THI",
        "VTT",
        "VLA",
        "WAS",
        "WSN"
    ]
    optional_kus = []
    for ku in ku_data:
        if ku["key"] in optional:
            optional_kus.append(ku)
    
    return optional_kus

def write_json_file(output_path, data):
    """Writes data to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4)

if __name__ == "__main__":
    wr_input_file = 'cae_cyber_defense_kus/cd_kus.json'
    output_file = 'cae_cyber_defense_kus/pos/optional_knowledge_units.json'

    ku_raw_data = read_json_file(wr_input_file)
    processed_data = process_data(ku_raw_data)
    write_json_file(output_file, processed_data)

    print(f"Processed data has been written to {output_file}")