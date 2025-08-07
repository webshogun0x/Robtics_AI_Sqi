import csv
import os
from datetime import datetime

def generate_csv(discrepancies, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{output_dir}/discrepancy_report.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["component", "sqlite_qty", "sheet_qty", "difference"])
        writer.writeheader()
        for row in discrepancies:
            writer.writerow(row)

    return filename
