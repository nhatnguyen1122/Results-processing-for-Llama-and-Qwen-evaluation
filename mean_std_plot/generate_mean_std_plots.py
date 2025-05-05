import os
import json
import matplotlib.pyplot as plt

DATASET_DIR = 'dataset'
OUTPUT_DIR = 'mean_std_plot'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_mean_std_plot(json_path, output_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    criteria_stats = data.get('criteria_statistics', {})
    # Use short labels for criteria
    criteria = [
        'understanding',
        'interpersonal',
        'collaboration',
        'guided_discovery',
        'focusing',
        'strategy',
        'attitude_change'
    ]
    means = [criteria_stats.get(c if c != 'interpersonal' and c != 'strategy' else (
        'interpersonal_effectiveness' if c == 'interpersonal' else 'strategy_for_change'), {}).get('mean', 0) for c in criteria]
    stds = [criteria_stats.get(c if c != 'interpersonal' and c != 'strategy' else (
        'interpersonal_effectiveness' if c == 'interpersonal' else 'strategy_for_change'), {}).get('std', 0) for c in criteria]
    total_avg = data.get('total_average', None)

    # Dynamic y-axis scaling for zoom-in effect
    ymin = min([m - s for m, s in zip(means, stds)])
    ymax = max([m + s for m, s in zip(means, stds)])
    margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
    y_lower = max(0, ymin - margin)
    y_upper = min(6, ymax + margin)

    plt.figure(figsize=(10, 6))
    plt.bar(criteria, means, yerr=stds, capsize=8, color='skyblue', edgecolor='black', align='center')
    plt.ylabel('Score')
    plt.ylim(y_lower, y_upper)
    # Format title without leading 'CACTUS_eval_' and ending '.json'
    base_name = os.path.basename(json_path)
    if base_name.startswith('CACTUS_eval_'):
        base_name = base_name[len('CACTUS_eval_'):]
    if base_name.endswith('.json'):
        base_name = base_name[:-len('.json')]
    plt.title(f"Mean and Std of Evaluation Criteria\n{base_name}")
    plt.xticks(rotation=30, ha='center')
    if total_avg is not None:
        plt.axhline(total_avg, color='red', linestyle='--', label=f'Total Average: {total_avg:.2f}')
        plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    for filename in os.listdir(DATASET_DIR):
        if filename.endswith('.json'):
            json_path = os.path.join(DATASET_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace('.json', '.png'))
            generate_mean_std_plot(json_path, output_path)

if __name__ == '__main__':
   main()