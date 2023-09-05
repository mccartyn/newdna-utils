import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import yaml

def load_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config

def generate_roadmap_from_csv(csv_file, config):
    # Read data from the CSV file
    df = pd.read_csv(csv_file)

    # Convert date strings to datetime objects
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    # Sort items by start date
    df = df.sort_values(by='start_date')

    # Create horizontal bar chart
    y_labels = df['task']
    start_dates = df['start_date']
    end_dates = df['end_date']
    bar_colors = df['bar_color'] if 'bar_color' in df else config.get("default_bar_color", "skyblue")

    plt.figure(figsize=(10, len(df) * 0.5))
    plt.barh(y_labels, end_dates - start_dates, left=start_dates, color=bar_colors)
    plt.xlabel("Timeline")
    plt.ylabel("Tasks")
    plt.title("Project Roadmap")

    # Set the x-axis ticks based on task start dates
    date_format = "%Y-%m-%d"
    date_range = pd.date_range(start=min(start_dates), end=max(end_dates), freq='D')
    plt.xticks(date_range, [date.strftime(date_format) for date in date_range], rotation=45)

    # Save the plot as an image
    plt.tight_layout()
    plt.savefig(config["output_image"], format='jpeg', bbox_inches='tight')

if __name__ == "__main__":
    config = load_config("config.yaml")
    generate_roadmap_from_csv("roadmap.csv", config)

