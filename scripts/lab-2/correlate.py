import os
import csv

# Function to read s2.csv
def read_s2_data():
    s2_csv_path = './scripts/sprint-2/dataset/s2.csv'
    s2_data = {}
    if os.path.exists(s2_csv_path):
        with open(s2_csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name_with_owner = row['nameWithOwner']
                s2_data[name_with_owner] = row
    return s2_data

# Function to calculate LOC from a file
def calculate_loc(file_path):
    loc = 0
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            loc += 1
    return loc

# Function to process files
def process_files():
    s2_data = read_s2_data()
    for name_with_owner, data in s2_data.items():
        repo_name = name_with_owner.replace("/", "-")
        class_csv_filename = f"./scripts/sprint-2/dataset/{repo_name}class.csv"
        
        if os.path.exists(class_csv_filename):
            if os.path.getsize(class_csv_filename) > 0:
                cbo_sum = 0
                dit_sum = 0
                lcom_sum = 0
                loc_sum = 0
                with open(class_csv_filename, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        cbo_sum += int(row['cbo'])
                        dit_sum += int(row['dit'])
                        lcom_sum += int(row['lcom'])
                loc_sum = calculate_loc(class_csv_filename)

                s2_data[name_with_owner]['CBO'] = cbo_sum
                s2_data[name_with_owner]['DIT'] = dit_sum
                s2_data[name_with_owner]['LCOM'] = lcom_sum
                s2_data[name_with_owner]['LOC'] = loc_sum

    # Write updated data to a new file
    with open('./scripts/sprint-2/dataset/s2_updated.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(s2_data.values())[0].keys()  # Extract fieldnames from the first row of s2.csv
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(s2_data.values())

# Execute the script
process_files()
