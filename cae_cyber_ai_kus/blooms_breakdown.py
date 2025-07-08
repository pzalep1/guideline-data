import logging
import json

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
    with open("ai_kus.json", 'r') as f:
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

        for outcome in ku["outcomes"]:
            # Split the outcome into a list of words and then get verb
            first_word = outcome.split()[0]

            # Convert the verb to lowercase
            verb = first_word.lower()

            if verb in remember_and_understand:
                ku["remember_outcomes"].append(outcome)
            
            elif verb in apply_and_analyze:
                ku["apply_outcomes"].append(outcome)
            
            elif verb in evaluate_and_synthesize:
                ku["evaluate_outcomes"].append(outcome)
            
            else: 
                ku["unknown_bloom"].append(outcome)
            

    with open('bloom_taxons_count.json', 'w') as f:
        json.dump(data_array, f, indent=4)

if __name__ == "__main__":
    main()