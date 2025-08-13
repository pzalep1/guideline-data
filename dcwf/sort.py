import json
import matplotlib.pyplot as plt
from collections import Counter, defaultdict

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def count_verbs(results):
    """Count occurrences of each verb and track their categories."""
    verb_counts = Counter()
    category_map = defaultdict(set)

    for item in results:
        for verb in item["matched_verb"]:
            verb_counts[verb] += 1
        for verb, category in zip(item["matched_verb"], item["blooms_category"]):
            category_map[verb].add(category)

    return verb_counts, category_map

def plot_verb_distribution(verb_counts, category_map, top_n=20):
    """Plot bar chart of top verbs by frequency, colored by category."""
    # Sort and select top N
    most_common = verb_counts.most_common(top_n)
    verbs, counts = zip(*most_common)
    categories = [next(iter(category_map[verb])) for verb in verbs]  # single category per verb

    # Color mapping
    category_colors = {
        "remember_and_understand": "skyblue",
        "apply_and_analyze": "orange",
        "evaluate_and_synthesize": "lightgreen"
    }
    bar_colors = [category_colors.get(cat, "gray") for cat in categories]

    # Plot
    plt.figure(figsize=(14, 6))
    bars = plt.bar(verbs, counts, color=bar_colors)
    plt.xlabel("Bloom’s Verbs")
    plt.ylabel("Frequency in KSATs")
    plt.title("Distribution of Bloom’s Verbs in Framework")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.legend(handles=[
        plt.Rectangle((0,0),1,1, color=category_colors[k]) for k in category_colors
    ], labels=category_colors.keys(), title="Bloom's Categories")
    plt.show()

def main():
    # This file should be the output from your earlier matching script
    results_file = "ksats_with_blooms.json"
    results = load_json(results_file)

    verb_counts, category_map = count_verbs(results)
    plot_verb_distribution(verb_counts, category_map)

if __name__ == "__main__":
    main()
