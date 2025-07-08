import json
import os
from sentence_transformers import SentenceTransformer, util
import re
from difflib import SequenceMatcher
import spacy
import logging


logger = logging.getLogger(__name__)

logging.basicConfig(   
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("description_htmls/output.log"),
        logging.StreamHandler()
    ]
)

# Configuration
input_array_path = 'ai_kus.json'   # JSON file containing the array
target_directory = 'ai-feedback'               # Directory containing secondary JSON files
lookup_key = 'key'                       # Attribute to use for lookup
filename_template = '{}.json'           # e.g., if ID is 'abc123' -> 'abc123.json'

# Load SentenceTransformer model
model = SentenceTransformer('all-mpnet-base-v2')

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def compare_strings_cosine(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2).item()

    return similarity

def lemmatize_text(text):
    """Tokenize and lemmatize text using spaCy."""
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if token.is_alpha]

def find_matching_sequences(lemmas1, lemmas2, min_len=2):
    """Find common subsequences of lemmas using SequenceMatcher."""
    matches = []
    matcher = SequenceMatcher(None, lemmas1, lemmas2, autojunk=False)

    for match in matcher.get_matching_blocks():
        if match.size >= min_len:
            match_seq = tuple(lemmas1[match.a: match.a + match.size])
            matches.append(match_seq)
    return matches

def highlight_matches(text1, text2, output_file, min_match_len=2):
    words1 = text1.split()
    lems1 = lemmatize_text(text1)
    lems2 = lemmatize_text(text2)

    match_phrases = set(' '.join(seq) for seq in find_matching_sequences(lems1, lems2, min_match_len))

    highlighted_text1 = []
    i = 0
    while i < len(words1):
        matched = False
        for length in range(len(words1), 0, -1):
            phrase = ' '.join(words1[i:i+length])
            lemmatized_phrase = ' '.join(lemmatize_text(phrase))
            if lemmatized_phrase in match_phrases:
                highlighted_text1.append(f'<span class="match">{" ".join(words1[i:i+length])}</span>')
                i += length
                matched = True
                break
        if not matched:
            highlighted_text1.append(words1[i])
            i += 1

    # HTML output with side-by-side columns
    html = [
        '<html><head><style>',
        'body { font-family: Arial, sans-serif; font-size: 16px; }',
        '.match { background-color: #c8e6c9; font-weight: bold; }',
        '.container { display: flex; gap: 40px; }',
        '.column { width: 45%; }',
        '.column h2 { margin-bottom: 10px; }',
        '</style></head><body>',
        '<div class="container">',
        '<div class="column"><h2>Stoneman Version (Overlaps Highlighted)</h2><p>',
        ' '.join(highlighted_text1),
        '</p></div>',
        '<div class="column"><h2>AI Suggestion</h2><p>',
        text2,
        '</p></div>',
        '</div></body></html>'
    ]

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
            logger.info(f'Cosine similarity for descriptions of {item["key"]}: {similarity}')

            highlight_matches(item["description"], sub_data["description"], f'description_htmls/{item["key"]}_text_matches.html')
                
        else:
            print(f"File not found: {filepath}")

if __name__ == "__main__":
    main()
