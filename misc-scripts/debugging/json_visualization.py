import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Directory containing JSON files
input_directory = '/Users/rishimehta/Desktop/fallyx_github/multimodal-model/FALLDATA/FALLDATA R2 -> 05:29:2024/downdata_json'
output_directory = '/Users/rishimehta/Desktop/fallyx_github/multimodal-model/FALLDATA/FALLDATA R2 -> 05:29:2024/downdata_outputgraphs'

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Loop through all files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(input_directory, filename)
        
        # Load the JSON data
        with open(file_path, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        # Generate timestamps if your data lacks them
        start_date = '2023-01-01 00:00:00'
        timestamps = pd.date_range(start=start_date, periods=len(df), freq='S')
        df['timestamp'] = timestamps

        # Convert timestamp to datetime for better visualization
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Create a figure and a set of subplots
        fig, ax1 = plt.subplots(figsize=(14, 6))

        # Plot Accelerometer Data on the first y-axis
        ax1.plot(df['timestamp'], df['Ax'], label='Accel Ax', color='tab:red')
        ax1.plot(df['timestamp'], df['Ay'], label='Accel Ay', color='tab:green')
        ax1.plot(df['timestamp'], df['Az'], label='Accel Az', color='tab:blue')
        ax1.set_xlabel('Timestamp')
        ax1.set_ylabel('Acceleration', color='tab:red')
        ax1.tick_params(axis='y', labelcolor='tab:red')
        ax1.set_ylim(-6, 6)  # Adjust the limit according to your data
        ax1.legend(loc='upper left')
        ax1.tick_params(axis='x', rotation=45)

        # Create a second y-axis for the Gyroscope data
        ax2 = ax1.twinx()
        ax2.plot(df['timestamp'], df['Gx'], label='Gyro Ax', color='tab:purple')
        ax2.plot(df['timestamp'], df['Gy'], label='Gyro Ay', color='tab:orange')
        ax2.plot(df['timestamp'], df['Gz'], label='Gyro Az', color='tab:brown')
        ax2.set_ylabel('Gyroscope', color='tab:purple')
        ax2.tick_params(axis='y', labelcolor='tab:purple')
        ax2.set_ylim(-1000, 1000)  # Adjust the limit according to your data
        ax2.legend(loc='upper right')

        # Add a title and adjust layout
        plt.title(f'Accelerometer and Gyroscope Data Over Time for {filename}')
        fig.tight_layout()

        # Save the plot to the output directory
        output_filepath = os.path.join(output_directory, filename.replace('.json', '.png'))
        plt.savefig(output_filepath)
        plt.close()  # Close the plot to free up memory

print("All plots are saved.")