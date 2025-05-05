import os
import json
import csv

# Path to the dataset directory
dataset_dir = 'dataset'
# Output CSV file
output_csv = 'model_criteria_means.csv'

# List all JSON files in the dataset directory
json_files = [f for f in os.listdir(dataset_dir) if f.endswith('.json')]

# Store results: {model_name: {criteria: mean, ...}, ...}
results = {}

# Set of all criteria (to ensure consistent column order)
all_criteria = set()

for json_file in json_files:
    with open(os.path.join(dataset_dir, json_file), 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Use model name from config or filename
        model_name = data.get('config', {}).get('finetuned_model', os.path.splitext(json_file)[0])
        # Remove leading 'PQPQPQHUST/CACTUS-' if present
        prefix = 'PQPQPQHUST/CACTUS-'
        if model_name.startswith(prefix):
            model_name = model_name[len(prefix):]
        criteria_stats = data.get('criteria_statistics', {})
        results[model_name] = {}
        for crit, stats in criteria_stats.items():
            mean = stats.get('mean')
            results[model_name][crit] = mean
            all_criteria.add(crit)

# Sort criteria for consistent column order
criteria_list = sorted(all_criteria)

# Add 'average' as the last column
criteria_list_with_avg = criteria_list + ['average']

# Write to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Header
    writer.writerow(['model'] + criteria_list_with_avg)
    # Rows
    for model, crit_means in results.items():
        # Compute average of all criteria for this model (ignore missing/empty values)
        values = [crit_means.get(crit, None) for crit in criteria_list]
        valid_values = [v for v in values if isinstance(v, (int, float))]
        avg = sum(valid_values) / len(valid_values) if valid_values else ''
        row = [model] + values + [avg]
        writer.writerow(row)

print(f"CSV file '{output_csv}' created successfully.")