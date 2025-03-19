import matplotlib.pyplot as plt
import numpy as np

# Create directory for saving graphs
import os
os.makedirs('graphs', exist_ok=True)

# 1. Accuracy Comparison Graph
def create_accuracy_comparison():
    # Data for the bar graph
    metrics = ['Overall Accuracy', 'Urban Scenarios', 'Rural Scenarios', 'Jailbreak Resistance']
    camera_only = [37.5, 31.3, 46.7, 33.3]
    three_sensors = [60.4, 56.3, 66.7, 88.9]

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Set the width of the bars
    bar_width = 0.35
    x = np.arange(len(metrics))

    # Create the bars
    bars1 = ax.bar(x - bar_width/2, camera_only, bar_width, label='Camera Only', color='#3498db', alpha=0.8)
    bars2 = ax.bar(x + bar_width/2, three_sensors, bar_width, label='Three Sensors (Color Depth)', color='#2ecc71', alpha=0.8)

    # Add labels, title, and legend
    ax.set_xlabel('Metrics', fontsize=12, fontweight='bold')
    ax.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax.set_title('Performance Comparison: Camera-Only vs. Three Sensors (Color Depth)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10)
    ax.legend(fontsize=10)

    # Add value labels on top of each bar
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords='offset points',
                        ha='center', va='bottom',
                        fontsize=9, fontweight='bold')

    add_labels(bars1)
    add_labels(bars2)

    # Add improvement percentages between bars
    for i in range(len(metrics)):
        improvement = three_sensors[i] - camera_only[i]
        ax.annotate(f'+{improvement:.1f}%',
                    xy=((x[i] - bar_width/2 + x[i] + bar_width/2) / 2, (camera_only[i] + three_sensors[i]) / 2),
                    xytext=(0, 0),
                    textcoords='offset points',
                    ha='center', va='center',
                    fontsize=9, fontweight='bold',
                    color='#e74c3c',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#e74c3c', alpha=0.7))

    # Add a grid for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)

    # Set y-axis to start at 0 and end at 100 (percentage)
    ax.set_ylim(0, 100)

    # Add a note about the data source
    plt.figtext(0.5, 0.01, 'Data source: Drone Landing Experiment Results', ha='center', fontsize=8, style='italic')

    # Adjust layout and save
    plt.tight_layout(pad=2.0)
    plt.savefig('graphs/accuracy_comparison.png', dpi=300, bbox_inches='tight')
    print('Created accuracy comparison graph')

# 2. False Positive Rate Graph
def create_false_positive_graph():
    # Data for the false positive rate graph
    methods = ['Camera Only', 'Three Sensors (Color Depth)']
    false_positive_rates = [48.7, 23.1]  # Updated with your total FPR values
    improvement = false_positive_rates[0] - false_positive_rates[1]

    # Create the figure
    plt.figure(figsize=(8, 5))
    
    # Create the bars
    bars = plt.bar(methods, false_positive_rates, color=['#3498db', '#2ecc71'], alpha=0.8)

    # Add labels and title
    plt.xlabel('Method', fontsize=12, fontweight='bold')
    plt.ylabel('False Positive Rate (%)', fontsize=12, fontweight='bold')
    plt.title('False Positive Rate Comparison', fontsize=14, fontweight='bold')

    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{height}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords='offset points',
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold')

    # Add improvement arrow and text
    plt.annotate(f'-{improvement:.1f}%',
                xy=(0.5, (false_positive_rates[0] + false_positive_rates[1]) / 2),
                xytext=(0, 0),
                textcoords='offset points',
                ha='center', va='center',
                fontsize=10, fontweight='bold',
                color='green',
                bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='green', alpha=0.7))

    # Add a grid for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().set_axisbelow(True)

    # Set y-axis to start at 0 and end at 100 (percentage)
    plt.ylim(0, 100)

    # Add a note about the data source
    plt.figtext(0.5, 0.01, 'Data source: Drone Landing Experiment Results', ha='center', fontsize=8, style='italic')

    # Adjust layout and save
    plt.tight_layout(pad=2.0)
    plt.savefig('graphs/false_positive_comparison.png', dpi=300, bbox_inches='tight')
    print('Created false positive rate graph')

# 3. Jailbreak Resistance Graph
def create_jailbreak_graph():
    # Data for the jailbreak resistance graph
    scenarios = ['BurningWrittenOnRoof', 'NPeopleWrittenOnRoof', 'MiscTextWrittenOnRoof', 'Average']
    camera_only_jb = [33.3, 33.3, 33.3, 33.3]
    three_sensors_jb = [100.0, 66.7, 100.0, 88.9]

    # Create the figure
    plt.figure(figsize=(10, 6))
    
    # Set up the x positions
    x = np.arange(len(scenarios))
    bar_width = 0.35

    # Create the bars
    bars1 = plt.bar(x - bar_width/2, camera_only_jb, bar_width, label='Camera Only', color='#3498db', alpha=0.8)
    bars2 = plt.bar(x + bar_width/2, three_sensors_jb, bar_width, label='Three Sensors (Color Depth)', color='#2ecc71', alpha=0.8)

    # Add labels and title
    plt.xlabel('Jailbreak Scenarios', fontsize=12, fontweight='bold')
    plt.ylabel('Resistance (%)', fontsize=12, fontweight='bold')
    plt.title('Jailbreak Resistance Comparison', fontsize=14, fontweight='bold')
    plt.xticks(x, scenarios, fontsize=9)
    plt.legend(fontsize=10)

    # Add value labels on top of each bar
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            plt.annotate(f'{height}%',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords='offset points',
                        ha='center', va='bottom',
                        fontsize=9, fontweight='bold')

    add_labels(bars1)
    add_labels(bars2)

    # Add improvement percentages between bars
    for i in range(len(scenarios)):
        improvement = three_sensors_jb[i] - camera_only_jb[i]
        plt.annotate(f'+{improvement:.1f}%',
                    xy=((x[i] - bar_width/2 + x[i] + bar_width/2) / 2, (camera_only_jb[i] + three_sensors_jb[i]) / 2),
                    xytext=(0, 0),
                    textcoords='offset points',
                    ha='center', va='center',
                    fontsize=9, fontweight='bold',
                    color='#e74c3c',
                    bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='#e74c3c', alpha=0.7))

    # Add a grid for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.gca().set_axisbelow(True)

    # Set y-axis to start at 0 and end at 100 (percentage)
    plt.ylim(0, 100)

    # Add a note about the data source
    plt.figtext(0.5, 0.01, 'Data source: Drone Landing Experiment Results', ha='center', fontsize=8, style='italic')

    # Adjust layout and save
    plt.tight_layout(pad=2.0)
    plt.savefig('graphs/jailbreak_resistance_comparison.png', dpi=300, bbox_inches='tight')
    print('Created jailbreak resistance graph')

# Execute all functions
create_accuracy_comparison()
create_false_positive_graph()
create_jailbreak_graph()

print('All visualizations have been created and saved in the graphs/ directory.')
