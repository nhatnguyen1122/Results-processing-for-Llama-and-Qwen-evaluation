import os
import json
import matplotlib.pyplot as plt

DATASET_DIR = 'dataset'
OUTPUT_DIR = 'plot_models_per_criteria'

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping for short display names
CRITERIA = [
    ('understanding', 'understanding'),
    ('interpersonal_effectiveness', 'interpersonal'),
    ('collaboration', 'collaboration'),
    ('guided_discovery', 'guided_discovery'),
    ('focusing', 'focusing'),
    ('strategy_for_change', 'strategy'),
    ('attitude_change', 'attitude_change')
]

def get_model_name(filename):
    if filename.startswith('CACTUS_eval_'):
        filename = filename[len('CACTUS_eval_'):]
    if filename.endswith('.json'):
        filename = filename[:-len('.json')]
    return filename

def main():
    # Gather all model means for each criteria
    model_names = []
    criteria_means = {short: [] for _, short in CRITERIA}
    for filename in os.listdir(DATASET_DIR):
        if filename.endswith('.json'):
            json_path = os.path.join(DATASET_DIR, filename)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            model_name = get_model_name(filename)
            model_names.append(model_name)
            stats = data.get('criteria_statistics', {})
            for long, short in CRITERIA:
                mean = stats.get(long, {}).get('mean', None)
                criteria_means[short].append(mean)
    # For each criteria, plot the mean across all models
    for short in criteria_means:
        means = criteria_means[short]
        # Sort by mean descending for better visualization
        sorted_data = sorted(zip(model_names, means), key=lambda x: (x[1] is not None, x[1]), reverse=True)
        sorted_names, sorted_means = zip(*sorted_data)
        plt.figure(figsize=(max(10, len(sorted_names)*0.7), 6))
        plt.bar(sorted_names, sorted_means, color='cornflowerblue', edgecolor='black')
        plt.ylabel('Mean Score')
        plt.title(f"Mean of '{short}' Across All Models")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, f'{short}_mean_across_models.png'))
        plt.close()

if __name__ == '__main__':
    main()
