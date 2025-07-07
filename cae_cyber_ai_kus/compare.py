import json
import os
from sentence_transformers import SentenceTransformer, util
import re
from difflib import SequenceMatcher

# Configuration
input_array_path = 'ai_kus.json'   # JSON file containing the array
target_directory = 'ai-feedback'               # Directory containing secondary JSON files
lookup_key = 'key'                       # Attribute to use for lookup
filename_template = '{}.json'           # e.g., if ID is 'abc123' -> 'abc123.json'

model = SentenceTransformer('all-mpnet-base-v2')

def compare_strings_cosine(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2).item()

    return similarity

def tokenize(text):
    # Simple tokenizer: lowercased words only
    return re.findall(r'\b\w+\b', text.lower())

def find_matching_sequences(words1, words2, min_len=2):
    matches = []
    len1, len2 = len(words1), len(words2)
    matcher = SequenceMatcher(None, words1, words2, autojunk=False)

    for match in matcher.get_matching_blocks():
        if match.size >= min_len:
            match_seq = tuple(words1[match.a: match.a + match.size])
            matches.append(match_seq)
    return matches

def highlight_matches(text1, text2, output_file, min_match_len=2):
    original_words = text1.split()
    lower_words1 = tokenize(text1)
    lower_words2 = tokenize(text2)

    matches = find_matching_sequences(lower_words1, lower_words2, min_len=min_match_len)
    flat_matches = set(' '.join(seq) for seq in matches)

    html = ['<html><head><style>',
            'body { font-family: Arial, sans-serif; font-size: 16px; }',
            '.match { background-color: #c8e6c9; font-weight: bold; }',
            '</style></head><body>',
            '<h2>Text 1 with Highlighted Matches</h2>',
            '<p>']

    i = 0
    while i < len(original_words):
        # Try to match the longest sequence from this point
        matched = False
        for length in range(len(original_words), 0, -1):
            phrase = ' '.join(original_words[i:i+length]).lower()
            if phrase in flat_matches:
                html.append(f'<span class="match">{" ".join(original_words[i:i+length])}</span> ')
                i += length
                matched = True
                break
        if not matched:
            html.append(original_words[i] + ' ')
            i += 1

    html.append('</p></body></html>')

    with open(output_file, 'w') as f:
        f.write('\n'.join(html))

    print(f"[+] HTML file created: {output_file}")

def main():
    # Read the array of objects
    with open(input_array_path, 'r') as f:
        data_array = json.load(f)

    # Process each element in the array
    for item in data_array:
        # item is the finalized data
        if lookup_key not in item:
            print(f"Skipping item without '{lookup_key}': {item}")
            continue

        # Construct filename from the attribute
        filename = filename_template.format(item[lookup_key])
        filepath = os.path.join(target_directory, filename)

        # Read the corresponding JSON file if it exists
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                # This is the data from the AI suggestions
                sub_data = json.load(f)
            
            # First compare the descriptions with just plain comparison
            similarity = compare_strings_cosine(sub_data["description"], item["description"])
            print(f'Cosine similarity for descriptions of {item["key"]}: {similarity}')

            highlight_matches(sub_data["description"], item["description"], f'{item["key"]}_text_matches.html')
                
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
