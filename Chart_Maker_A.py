# Chart Maker A Version 0.1
# This create heatmaps of each activities for each user.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ask the user for the path of the CSV file and the output directory
csv_file_path = input("Please enter the path of the Data CSV file: ")
output_directory = input("Please enter the path where you'd like to save the output charts: ")

# Ensure the output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Read the CSV file, using the first row as the header
df = pd.read_csv(csv_file_path, header=0)

# Convert 'time' to a datetime object with the specified format
df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')

# Extract the hour and date
df['hour'] = df['time'].dt.hour
df['date'] = df['time'].dt.date

# Create an empty list to store DataFrame fragments
heatmap_data_fragments = []

# Iterate over each user, event, and date to count events per hour
for user in df['user'].unique():
    user_df = df[df['user'] == user]
    for event in user_df['event'].unique():
        event_df = user_df[user_df['event'] == event]
        for date in event_df['date'].unique():
            date_df = event_df[event_df['date'] == date]
            hour_count = date_df['hour'].value_counts().sort_index()
            for hour in range(24):
                if hour not in hour_count:
                    hour_count.at[hour] = 0
            fragment = pd.DataFrame({
                'user': user, 
                'event': event, 
                'date': date, 
                'hour': hour_count.index, 
                'event_count': hour_count.values
            })
            heatmap_data_fragments.append(fragment)

# Concatenate all fragments into a single DataFrame
heatmap_data = pd.concat(heatmap_data_fragments)

# Pivot the data for the heat map
pivot_df = heatmap_data.pivot_table(index=['user', 'event', 'date'], columns='hour', values='event_count', fill_value=0)

# Plotting and saving
for user in df['user'].unique():
    for event in df['event'].unique():
        if (user, event) in pivot_df.index:
            user_event_data = pivot_df.loc[(user, event)]
            plt.figure(figsize=(12, 6))
            sns.heatmap(user_event_data, annot=True, fmt="g", cmap="YlGnBu")
            plt.title(f"Heat Map for User: {user}, Event: {event}")
            plt.ylabel('Date')
            plt.xlabel('Hour')

            # Save the figure in the specified output directory
            plt.savefig(os.path.join(output_directory, f'heatmap_{user}_{event}.png'))

            plt.close()  # Close the figure after saving
