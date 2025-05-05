import os
import json
import matplotlib.pyplot as plt

DATASET_DIR = 'dataset'
OUTPUT_PNG = 'total_average_all_models.png'

def get_model_name(filename):
    # Remove leading 'CACTUS_eval_' and ending '.json'
    if filename.startswith('CACTUS_eval_'):
        filename = filename[len('CACTUS_eval_'):]
    if filename.endswith('.json'):
        filename = filename[:-len('.json')]
    return filename

def main():
    model_names = []
    total_averages = []
    for filename in os.listdir(DATASET_DIR):
        if filename.endswith('.json'):
            json_path = os.path.join(DATASET_DIR, filename)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            model_names.append(get_model_name(filename))
            total_averages.append(data.get('total_average', 0))
    # Sort by total_average descending for better visualization
    sorted_data = sorted(zip(model_names, total_averages), key=lambda x: x[1], reverse=True)
    sorted_names, sorted_averages = zip(*sorted_data)
    plt.figure(figsize=(max(10, len(sorted_names)*0.7), 6))
    plt.bar(sorted_names, sorted_averages, color='mediumseagreen', edgecolor='black')
    plt.ylabel('Total Average')
    plt.title('Total Average Score of All Models')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(OUTPUT_PNG)
    plt.close()

if __name__ == '__main__':
    main()
