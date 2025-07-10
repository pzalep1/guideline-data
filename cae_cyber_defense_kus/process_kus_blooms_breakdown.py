import csv
import sys

def count_custom_matches(csv_path, single_conditions=[], combined_conditions=[]):
    """
    single_conditions: list of tuples like [("Score", ">", 80)]
    combined_conditions: list like [("Score", "+", "Bonus", ">=", 100)]
    """
    count = 0
    try:
        with open(csv_path, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    # Check single-column conditions
                    single_match = all(
                        eval(f"{float(row[col])} {op} {float(val)}")
                        for col, op, val in single_conditions
                    )

                    # Check combined-column conditions
                    combined_match = all(
                        eval(
                            f"{float(row[col1])} {math_op} {float(row[col2])} {comp_op} {float(val)}"
                        )
                        for col1, math_op, col2, comp_op, val in combined_conditions
                    )

                    if single_match and combined_match:
                        count += 1
                except (ValueError, TypeError, ZeroDivisionError):
                    continue  # skip rows with bad or missing data
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return -1
    return count

if __name__ == "__main__":

    # 🔧 Customize conditions below
    single_conditions = [
        # ("Evaluate %", "==", 0)
    ]

    combined_conditions = [
        ("Evaluate %", "+", "Apply %", ">=", .5),    # e.g., Score + Bonus >= 100
    ]

    result = count_custom_matches("blooms_charts/all_blooms_breakdown.csv", single_conditions, combined_conditions)
    print(f"Rows matching conditions: {result}")

