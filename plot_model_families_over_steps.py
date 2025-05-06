import csv
import matplotlib.pyplot as plt
import re

CSV_PATH = 'model_criteria_means.csv'
OUTPUT_PNG = 'model_families_over_steps.png'

# Model families to plot
model_families = [
    'Llama-3.2-1B-Instruct',
    'Qwen2.5-1.5B-Instruct',
    'Qwen2.5-3B-Instruct',
    'Qwen2.5-7B-Instruct',
    'Qwen3-0.6B',
    'Qwen3-8B',
]

# Read CSV and organize data
family_data = {family: [] for family in model_families}
with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        model = row['model']
        avg = float(row['average']) if row['average'] else None
        # Extract family and step
        m = re.match(r'(.+)-(\d+)$', model)
        if m:
            family, step = m.group(1), int(m.group(2))
            if family in family_data and avg is not None:
                family_data[family].append((step, avg))

# Plot
plt.figure(figsize=(10, 6))
for family, points in family_data.items():
    if points:
        points.sort()  # sort by step
        steps, avgs = zip(*points)
        plt.plot(steps, avgs, marker='o', label=family)
plt.xlabel('Training Steps')
plt.ylabel('Average Value')
plt.title('Model Families Performance over Training Steps')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(OUTPUT_PNG)
plt.close()
