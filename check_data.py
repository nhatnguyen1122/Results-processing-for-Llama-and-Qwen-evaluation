import os
import json

def analyze_dataset(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    criteria = list(data['config']['evaluation_criteria'].keys())
    issues = []

    for idx, conv in enumerate(data['conversations']):
        scores = conv.get('evaluation_scores', {})
        # Check for missing criteria
        missing = [c for c in criteria if c not in scores]
        if missing:
            issues.append(f"Conversation {idx}: Missing scores for {missing}")
        # Check for unconventional scores
        for k, v in scores.items():
            if not isinstance(v, int) or v < 0 or v > 6:
                issues.append(f"Conversation {idx}: Unconventional score {k}={v}")

    if not issues:
        print(f"{os.path.basename(json_path)}: No missing or unconventional data found.")
    else:
        print(f"{os.path.basename(json_path)}: Issues found:")
        for issue in issues:
            print(issue)

def analyze_all_datasets(dataset_dir):
    for filename in os.listdir(dataset_dir):
        if filename.endswith('.json'):
            analyze_dataset(os.path.join(dataset_dir, filename))

# Usage
analyze_all_datasets('dataset')