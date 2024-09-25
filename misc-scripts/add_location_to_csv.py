import csv

# Static row to add
location_row = ["Ayaan's Suite"]  # Modify this as per your static values

# Input and output file paths
input_csv = 'fall-5-old.csv'
output_csv = 'fall-5-old.csv'

# Read the original CSV
with open(input_csv, 'r') as infile:
    reader = list(csv.reader(infile))

# Write the static row followed by the original CSV content
with open(output_csv, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write the static row first
    writer.writerow(location_row)
    
    # Write the rest of the original CSV
    writer.writerows(reader)

print("Static row added and file saved as", output_csv)
