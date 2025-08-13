import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def flatten_blooms_verbs(blooms_data):
    """Create a mapping from verb to category."""
    verb_to_category = {}
    for category, data in blooms_data["taxons"].items():
        for verb in data["verbs"]:
            verb_to_category[verb.lower()] = category
    return verb_to_category

def write_to_json(results, filename="ksats_with_blooms.json"):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✅ Results written to {filename}")

def assign_all_blooms_categories(ksats, verb_to_category):
    """Attach all matching Bloom's verbs and categories to each KSAT."""
    results = []

    for ksat in ksats:
        description = ksat["description"].lower()
        matched_verbs = []
        matched_categories = set()

        for verb, category in verb_to_category.items():
            # Allow matching verbs like "carry out", "back up", etc.
            if f" {verb} " in f" {description} " or description.startswith(verb + " ") or description.endswith(" " + verb):
                matched_verbs.append(verb)
                matched_categories.add(category)
            
        results.append({
            "id": ksat["_id"],
            "description": ksat["description"],
            "work_roles": ksat["work_roles"],
            "element_id": ksat["element_id"],
            "type": ksat["type"],
            "matched_verb": matched_verbs,
            "blooms_category": list(matched_categories)
        })

    return results

def main():
    ksats_file = "ksat_with_work_role_names.json"
    blooms_file = "blooms.json"

    ksats_data = load_json(ksats_file)
    blooms_data = load_json(blooms_file)

    # If your ksats.json is a list (not wrapped in a key), no need to access ["ksats"]
    ksats = ksats_data if isinstance(ksats_data, list) else ksats_data["ksats"]
    
    verb_to_category = flatten_blooms_verbs(blooms_data)
    results = assign_all_blooms_categories(ksats, verb_to_category)

    print(len(results))
    write_to_json(results)

if __name__ == "__main__":
    main()
