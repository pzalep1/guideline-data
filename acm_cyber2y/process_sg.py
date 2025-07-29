import json
import re
from collections import defaultdict

def process_guidelines(input_file, output_file):
    # Read input JSON
    with open(input_file, 'r') as f:
        data = json.load(f)

    grouped = defaultdict(lambda: {"name": "", "key": "", "outcomes": []})

    for item in data["results"]:
        name_raw = item.get("guidelineName", "")
        description = item.get("guidelineDescription", "").strip()

        # Extract name (everything before the bracket)
        name_match = re.match(r"^(.*?)\s*\[", name_raw)
        name = name_match.group(1).strip() if name_match else name_raw.strip()

        # Extract key (inside brackets, before dash)
        key_match = re.search(r"\[(.*?)-", name_raw)
        key = key_match.group(1).strip() if key_match else ""

        key_id = f"{name}_{key}"  # Unique key for grouping

        grouped[key_id]["name"] = name
        grouped[key_id]["key"] = key
        grouped[key_id]["outcomes"].append(description)

    # Convert dict to list
    output = list(grouped.values())

    # Write to output file
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Processed {len(output)} guideline groups into '{output_file}'")

# Example usage
process_guidelines('sg_kus.json', 'cyber2y_kus.json')

