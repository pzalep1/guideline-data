import pandas as pd
import json

def calculate_bloom_percentages(data):
    table_data = []

    for obj in data:
        total = len(obj.get("outcomes", []))
        remember = len(obj.get("remember_outcomes", []))
        apply = len(obj.get("apply_outcomes", []))
        evaluate = len(obj.get("evaluate_outcomes", []))

        if total == 0:
            remember_pct = apply_pct = evaluate_pct = 0
        else:
            remember_pct = round((remember / total) * 100, 2)
            apply_pct = round((apply / total) * 100, 2)
            evaluate_pct = round((evaluate / total) * 100, 2)

        table_data.append({
            "Name": obj.get("name", ""),
            "Key": obj.get("key", ""),
            "Total Outcomes": total,
            "Remember (%)": remember_pct,
            "Apply (%)": apply_pct,
            "Evaluate (%)": evaluate_pct,
            "Remember + Apply (%)": round(remember_pct + apply_pct, 2),
            "Apply + Evaluate (%)": round(apply_pct + evaluate_pct, 2)
        })

    return pd.DataFrame(table_data)

def calculate_summary_stats(df: pd.DataFrame):
    total_kus = len(df)
    stats = {
        "Remember ≥ 50%": (df["Remember (%)"] >= 50).sum(),
        "Apply ≥ 50%": (df["Apply (%)"] >= 50).sum(),
        "Evaluate ≥ 50%": (df["Evaluate (%)"] >= 50).sum(),
        "Remember + Apply ≥ 50%": (df["Remember + Apply (%)"] >= 50).sum(),
        "Apply + Evaluate ≥ 50%": (df["Apply + Evaluate (%)"] >= 50).sum()
    }

    print("📊 Summary Stats (KUs with ≥ 50%):")
    for label, count in stats.items():
        pct = round((count / total_kus) * 100, 2) if total_kus > 0 else 0
        print(f"- {label}: {count} / {total_kus} ({pct}%)")

# === 🔽 MAIN EXECUTION 🔽 ===

# Path to your JSON file
json_file_path = "bloom_taxons_count_acm_adjusted_unknowns.json"

# Load JSON data
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Compute table
df = calculate_bloom_percentages(data)

# Save to CSV
csv_output_path = "bloom_percentages_report.csv"
df.to_csv(csv_output_path, index=False)
print(f"✅ Report saved to: {csv_output_path}")

# Print summary
calculate_summary_stats(df)
