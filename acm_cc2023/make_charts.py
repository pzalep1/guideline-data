import json
import matplotlib.pyplot as plt
import pandas as pd
import csv
import re

def sanitize_filename(name):
    # Remove characters that are problematic or reserved
    return re.sub(r'[\/:*?"<>|\\\0]', '', name)

with open("bloom_taxons_count_acm.json", 'r') as f:
        data_array = json.load(f)

# Label-to-color mapping
color_map = {
    'Remember Taxon': '#90EE90',
    'Apply Taxon': '#ADD8E6',
    'Evaluate Taxon': '#CBC3E3',
    'Unknown Taxon': '#FFD580'
}

rows = []
csv_filename = 'blooms_charts/all_blooms_breakdown.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Header row
    writer.writerow(['Name', 'Remember %', 'Apply %', 'Evaluate %', 'Unknown %'])

    for data in data_array:
        all_labels = ['Remember Taxon', 'Apply Taxon', 'Evaluate Taxon', 'Unknown Taxon']
        all_values = [
            len(data["remember_outcomes"]),
            len(data["apply_outcomes"]),
            len(data["evaluate_outcomes"]),
            len(data["unknown_bloom"])
        ]
        # For csv
        total = sum(all_values)
        if total == 0:
            percentages = [0.0] * len(all_values)
        else:
            percentages = [(v / total) * 100 for v in all_values]

        # Filter out zero-value entries
        labels = [label for label, value in zip(all_labels, all_values) if value > 0]
        values = [value for value in all_values if value > 0]
        colors = [color_map[label] for label in labels]

        # Create pie chart
        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.title(f"Blooms Distribution for ACM CC2023 KU {data["name"]}")
        plt.axis('equal')  # Equal aspect ratio ensures the pie is circular.

        # Save to file
        plt.savefig(f'blooms_charts/{sanitize_filename(data["name"])}_blooms_breakdown.png', dpi=300)
        plt.close()

        # Now lets get a nice little chart
        remember = len(data.get("remember_outcomes", []))
        apply = len(data.get("apply_outcomes", []))
        evaluate = len(data.get("evaluate_outcomes", []))
        unknown = len(data.get("unknown_bloom", []))
        total = len(data.get("outcomes", []))

        rows.append({
            "Name": data.get("name", ""),
            "Remember \nTaxon": remember,
            "Apply \nTaxon": apply,
            "Evaluate \nTaxon": evaluate,
            "Unknown \nTaxon": unknown,
            "Total \nOutcomes": total
        })

    # Write one row per dataset
        writer.writerow([
            data["name"],
            f"{percentages[0]:.1f}%",
            f"{percentages[1]:.1f}%",
            f"{percentages[2]:.1f}%",
            f"{percentages[3]:.1f}%"
        ])


# Now save it to use a pptx
df = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(10, 0.6 * len(df) + 2))  # Wider for better control
ax.axis('tight')
ax.axis('off')

# Create table
table = ax.table(
    cellText=df.values,
    colLabels=df.columns,
    cellLoc='center',
    loc='center'
)

# Style table
table.auto_set_font_size(True)
# table.set_fontsize(10)
table.scale(1.2, 1.2)

# Adjust column widths manually
col_widths = {
    'Name': 0.4,
    'Remember': 0.12,
    'Apply': 0.12,
    'Evaluate': 0.12,
    'Unknown': 0.12,
    'Total': 0.12
}

for i, col in enumerate(df.columns):
    for j in range(len(df) + 1):  # +1 to include header
        cell = table[j, i]
        cell.set_width(col_widths.get(col, 0.1))
        if j==0:
             cell.set_height(0.025)
# plt.title("Bloom's Taxonomy Outcome Breakdown", fontsize=14, pad=5)
plt.savefig("blooms_charts/blooms_breakdown_table.png", bbox_inches='tight', dpi=600)
plt.close()


