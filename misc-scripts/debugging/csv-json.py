import argparse
import os
import csv
import json


def csv_columns_to_json(csv_file_path, json_file_path):
    data = {}

    try:
        with open(csv_file_path, mode='r', encoding='utf-8-sig', errors='ignore') as csv_file:
            csv_reader = csv.reader(csv_file)

            # Read the first row to get the location
            location_row = next(csv_reader)
            data['Location'] = "None"  # Assuming 'Location' is the first entry of the first row

            # Read the second row as headers and ignore it
            headers = next(csv_reader)

            # Read the remaining rows (data starting from the third row) and transpose them
            columns = list(zip(*csv_reader))  # Transpose the CSV rows to columns

            # Assuming a specific order: ['Timestamp', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz']
            data['Timestamp'] = list(columns[0])  # First column is 'Timestamp'
            data['Ax'] = [float(i) for i in columns[3]]  # Second column is 'Ax'
            data['Ay'] = [float(i) for i in columns[4]]  # Third column is 'Ay'
            data['Az'] = [float(i) for i in columns[5]]  # Fourth column is 'Az'
            data['Gx'] = [float(i) for i in columns[6]]  # Fifth column is 'Gx'
            data['Gy'] = [float(i) for i in columns[7]]  # Sixth column is 'Gy'
            data['Gz'] = [float(i) for i in columns[8]]  # Seventh column is 'Gz'

    except (UnicodeDecodeError, csv.Error) as e:
        print(f"Error processing file {csv_file_path}: {e}")
        return

    # Write the output to a JSON file
    try:
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as e:
        print(f"Error writing JSON file {json_file_path}: {e}")


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Convert CSV files to JSON format.")
    parser.add_argument('-i', '--input', nargs='+', required=True, help="Input CSV file(s) or directory containing CSV files.")
    parser.add_argument('-o', '--output', required=True, help="Output directory for JSON files.")

    # Parse the arguments
    args = parser.parse_args()

    # Ensure output directory exists
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    # Process each input CSV file or path
    for input_path in args.input:
        if os.path.isfile(input_path) and input_path.lower().endswith('.csv'):
            # If it's a file and ends with .csv
            csv_file_path = input_path
            json_file_name = os.path.splitext(os.path.basename(input_path))[0] + '.json'
            json_file_path = os.path.join(args.output, json_file_name)
            csv_columns_to_json(csv_file_path, json_file_path)
            print(f"Converted {csv_file_path} to {json_file_path}")
        elif os.path.isdir(input_path):
            # If it's a directory, process all CSV files within it
            for root, dirs, files in os.walk(input_path):
                for file in files:
                    if file.lower().endswith('.csv'):
                        csv_file_path = os.path.join(root, file)
                        json_file_name = os.path.splitext(file)[0] + '.json'
                        json_file_path = os.path.join(args.output, json_file_name)
                        csv_columns_to_json(csv_file_path, json_file_path)
                        print(f"Converted {csv_file_path} to {json_file_path}")

if __name__ == "__main__":
    main()
