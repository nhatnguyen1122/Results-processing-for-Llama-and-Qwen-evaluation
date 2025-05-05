import os
import json
import matplotlib.pyplot as plt

DATASET_DIR = 'dataset'
OUTPUT_DIR = 'box_plot'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_box_plot(json_path, output_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    criteria = list(data['config']['evaluation_criteria'].keys())
    # Collect scores for each criterion
    scores = {c: [] for c in criteria}
    for conv in data['conversations']:
        eval_scores = conv.get('evaluation_scores', {})
        for c in criteria:
            v = eval_scores.get(c, None)
            if isinstance(v, int):
                scores[c].append(v)
    # Prepare data for boxplot
    data_to_plot = [scores[c] for c in criteria]
    plt.figure(figsize=(10, 6))
    plt.boxplot(data_to_plot, labels=criteria, patch_artist=True)
    # Format title without leading 'CACTUS_eval_' and ending '.json'
    base_name = os.path.basename(json_path)
    if base_name.startswith('CACTUS_eval_'):
        base_name = base_name[len('CACTUS_eval_'):]
    if base_name.endswith('.json'):
        base_name = base_name[:-len('.json')]
    plt.title(f"Box Plot of Evaluation Criteria\n{base_name}")
    plt.ylabel('Score')
    plt.ylim(0, 6)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    for filename in os.listdir(DATASET_DIR):
        if filename.endswith('.json'):
            json_path = os.path.join(DATASET_DIR, filename)
            output_path = os.path.join(OUTPUT_DIR, filename.replace('.json', '.png'))
            generate_box_plot(json_path, output_path)

if __name__ == '__main__':
    main()
