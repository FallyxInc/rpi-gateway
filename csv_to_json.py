import csv
import json

def csv_columns_to_json(csv_file_path, json_file_path):
    data = {}

    # Open the CSV file and read its content
    with open(csv_file_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # Read the first row to get the location
        location_row = next(csv_reader)
        #data['Location'] = location_row[0]  # Assuming 'Location' is the first entry of the first row

        # Read the second row as headers and ignore it
        headers = next(csv_reader)

        # Read the remaining rows (data starting from the third row) and transpose them
        columns = list(zip(*csv_reader))  # Transpose the CSV rows to columns

        # Assuming a specific order: ['Timestamp', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz']
        #data['Timestamp'] = list(columns[0])  # First column is 'Timestamp'
        data['Ax'] = [float(i) for i in columns[3]]  # Second column is 'Ax'
        data['Ay'] = [float(i) for i in columns[4]]  # Third column is 'Ay'
        data['Az'] = [float(i) for i in columns[5]]  # Fourth column is 'Az'
        data['Gx'] = [float(i) for i in columns[6]]  # Fifth column is 'Gx'
        data['Gy'] = [float(i) for i in columns[7]]  # Sixth column is 'Gy'
        data['Gz'] = [float(i) for i in columns[8]]  # Seventh column is 'Gz'

    # Write the output to a JSON file
    with open(json_file_path, mode='w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
csv_file_path = 'imu_data_20240913_191719.csv'  # Path to your CSV file
json_file_path = 'walking_pat.json'  # Path to the output JSON file
csv_columns_to_json(csv_file_path, json_file_path)
