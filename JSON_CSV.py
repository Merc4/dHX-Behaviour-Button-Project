# JSON to CSV Decoder Version 0.1
import pandas as pd
from datetime import datetime

def json_to_csv_with_replacement(json_file_path, csv_file_path, config_file_path):
    # Read the config CSV file into a DataFrame
    config_df = pd.read_csv(config_file_path)
    
    # Create a mapping dictionary from the config DataFrame
    replacement_dict = dict(zip(config_df['source data'], config_df['replaced with']))

    # Read the JSON file into a DataFrame
    df = pd.read_json(json_file_path)

    # Replace data based on the config mapping
    for column in df.columns:
        if df[column].dtype == object:  # Checking if the column is of type 'object' (string)
            df[column] = df[column].replace(replacement_dict)

        # Format the 'Timestamp' field
        if column == 'Timestamp':
            df[column] = pd.to_datetime(df[column]).dt.strftime('%d/%m/%Y %H:%M:%S')

    # Save the modified DataFrame to a CSV file
    df.to_csv(csv_file_path, index=False)
    print(f"CSV file saved to {csv_file_path}")

# Ask user for file paths
json_file_path = input("Enter the path to the data JSON file: ")
csv_file_path = input("Enter the path for the output CSV file: ")
config_file_path = input("Enter the path to the configuration (config) CSV file: ")

json_to_csv_with_replacement(json_file_path, csv_file_path, config_file_path)
