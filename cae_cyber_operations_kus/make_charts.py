import json
import matplotlib.pyplot as plt

with open("bloom_taxons_count.json", 'r') as f:
        data_array = json.load(f)

# Label-to-color mapping
color_map = {
    'Remember Taxon': '#90EE90',
    'Apply Taxon': '#ADD8E6',
    'Evaluate Taxon': '#CBC3E3',
    'Unknown Taxon': '#FFD580'
}

for data in data_array:
    all_labels = ['Remember Taxon', 'Apply Taxon', 'Evaluate Taxon', 'Unknown Taxon']
    all_values = [
        len(data["remember_outcomes"]),
        len(data["apply_outcomes"]),
        len(data["evaluate_outcomes"]),
        len(data["unknown_bloom"])
    ]

    # Filter out zero-value entries
    labels = [label for label, value in zip(all_labels, all_values) if value > 0]
    values = [value for value in all_values if value > 0]
    colors = [color_map[label] for label in labels]

    # Create pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title(f"Blooms Distribution for Cyber Operations {data["name"]}")
    plt.axis('equal')  # Equal aspect ratio ensures the pie is circular.

    # Save to file
    plt.savefig(f'blooms_charts/{data["key"]}_blooms_breakdown.png', dpi=300)

    # Display
    plt.show()
