import logging
import json
from collections import Counter

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

def main():
    # Read the array of objects
    with open("cd_kus.json", 'r') as f:
        data_array = json.load(f)
    
    with open("blooms.json", "r") as f:
        blooms = json.load(f)

    remember_and_understand = blooms["taxons"]["remember_and_understand"]["verbs"]
    apply_and_analyze = blooms["taxons"]["apply_and_analyze"]["verbs"]
    evaluate_and_synthesize = blooms["taxons"]["evaluate_and_synthesize"]["verbs"]

    for ku in data_array:
        ku["remember_outcomes"] = []
        ku["apply_outcomes"] = []
        ku["evaluate_outcomes"] = []
        ku["unknown_bloom"] = []

        # Initialize a counter for the verbs
        verb_counter = Counter()

        for outcome in ku["outcomes"]:
            # Get the first word (verb) of the outcome
            first_word = outcome.split()[0]
            verb = first_word.lower()

            # Count the verb
            verb_counter[verb] += 1

            # Classify the outcome into Bloom's categories
            if verb.rstrip(',') in remember_and_understand:
                ku["remember_outcomes"].append(outcome)
            elif verb.rstrip(',') in apply_and_analyze:
                ku["apply_outcomes"].append(outcome)
            elif verb.rstrip(',') in evaluate_and_synthesize:
                ku["evaluate_outcomes"].append(outcome)
            else:
                ku["unknown_bloom"].append(outcome)

        # Save the verb counts to the dict if needed
        ku["verb_counts"] = dict(verb_counter)
            

    with open('bloom_taxons_count_acm.json', 'w') as f:
        json.dump(data_array, f, indent=4)

if __name__ == "__main__":
    main()