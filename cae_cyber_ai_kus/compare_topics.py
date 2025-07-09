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
        logging.FileHandler("output.log"),
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

def find_matching_sequences(lemmas1, lemmas2, min_len=2):
    matches = []
    matcher = SequenceMatcher(None, lemmas1, lemmas2, autojunk=False)
    for match in matcher.get_matching_blocks():
        if match.size >= min_len:
            matches.append(tuple(lemmas1[match.a: match.a + match.size]))
    return matches

def highlight_text1(text1, text2, min_match_len=2):
    words1 = text1.split()
    lems1 = lemmatize_text(text1)
    lems2 = lemmatize_text(text2)

    match_phrases = set(' '.join(seq) for seq in find_matching_sequences(lems1, lems2, min_match_len))

    highlighted = []
    i = 0
    while i < len(words1):
        matched = False
        for length in range(len(words1), 0, -1):
            phrase = ' '.join(words1[i:i+length])
            lemmatized_phrase = ' '.join(lemmatize_text(phrase))
            if lemmatized_phrase in match_phrases:
                highlighted.append(f'<span class="match">{" ".join(words1[i:i+length])}</span>')
                i += length
                matched = True
                break
        if not matched:
            highlighted.append(words1[i])
            i += 1
    return ' '.join(highlighted)

def highlight_all_matches(data_list, output_file, key, min_match_len=2):
    html = [
        '<html><head><style>',
        'body { font-family: Arial, sans-serif; font-size: 16px; }',
        '.match { background-color: #c8e6c9; font-weight: bold; }',
        '.container { display: flex; gap: 40px; margin-bottom: 50px; }',
        '.column { width: 40%; }',
        '.small-column { width: 10% }',
        '.column h2 { margin-bottom: 10px; }',
        '</style></head><body>',
        f'<h1>Outcomes for {key}</h1>',
        f'<div class="container">',
        f'<div class="column"><h2><b>Stoneman Version</b></h2></div>',
        f'<div class="column"><h2><b>AI Suggestion</b></h2></div>',
        f'<div class="small-column"><h2><b>Cosine Similarity</b></h2></div>',
        '</div>'
    ]

    for i, item in enumerate(data_list):
        text1 = item['published']
        text2 = item['suggested']
        text3 = item['cosine']
        highlighted_text1 = highlight_text1(text1, text2, min_match_len)

        html.extend([
            f'<div class="container">',
            f'<div class="column"><p>{highlighted_text1}</p></div>',
            f'<div class="column"><p>{text2}</p></div>',
            f'<div class="small-column"><p>{text3}</p></div>',
            '</div>'
        ])

    html.append('</body></html>')

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
            logger.info(f'Starting {item["key"]}')
            # First compare the descriptions with just plain comparison
            highlight = []
            for suggested_outcome in sub_data["topics"]:
                for published_outcome in item["topics"]:
                    similarity = compare_strings_cosine(published_outcome, suggested_outcome)
                    if similarity > .80:
                        logger.info(f'Cosine similarity for {suggested_outcome} and {published_outcome} in {item["key"]} is {similarity}')
                        highlight.append(
                            {
                                "published": published_outcome,
                                "suggested": suggested_outcome,
                                "cosine": round(similarity, 2)
                            }
                        )

            if len(highlight) > 0:
                highlight_all_matches(highlight, f'topic_htmls/{item["key"]}_topic_text_matches.html', item["key"])
                
        logger.info('Now we can do the extra files my dude')
        other = ["ai_algorithms", "data_management"]
        for ea in other:
            with open(f'ai-feedback/{ea}.json', 'r') as f:
                # This is the data from the AI suggestions
                sub_data = json.load(f)
            logger.info(f'Starting {item["key"]}')
            # compare to the other two that got combined
            highlight = []
            for suggested_outcome in sub_data["topics"]:
                for published_outcome in item["topics"]:
                    similarity = compare_strings_cosine(published_outcome, suggested_outcome)
                    if similarity > .80:
                        logger.info(f'Cosine similarity for {suggested_outcome} and {published_outcome} in {item["key"]} is {similarity}')
                        highlight.append(
                            {
                                "published": published_outcome,
                                "suggested": suggested_outcome,
                                "cosine": round(similarity, 2)
                            }
                        )

            if len(highlight) > 0:
                highlight_all_matches(highlight, f'topic_htmls/{item["key"]}_compare_to_{ea}_for_topic_text_matches.html', item["key"])

if __name__ == "__main__":
    main()