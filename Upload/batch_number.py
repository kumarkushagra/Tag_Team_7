import pandas as pd

import csv
import datetime

# def latest_batch_number():
#     csv_file_path = 'Database/mapping.csv'

#     try:
#         # Open the CSV file
#         with open(csv_file_path, mode='r') as file:
#             reader = csv.DictReader(file)
            
#             # Initialize variables to track the latest batch and time
#             latest_time = datetime.datetime.min
#             latest_batch = None
#             latest_normal_number = 0
            
#             # Flag to check if there are any data rows
#             has_data = False
            
#             for row in reader:
#                 has_data = True
#                 # Combine date and time into a single datetime object
#                 timestamp = f"{row['date']} {row['Time']}"
#                 current_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
                
#                 # Compare current time with the latest time
#                 if current_time > latest_time:
#                     latest_time = current_time
#                     latest_batch = row['batch_no']
                    
#                     # Extract the integer part of the normal name if it starts with 'Normal_'
#                     if row['name_of_StudyID'].startswith('Normal_'):
#                         latest_normal_name = row['name_of_StudyID']
#                         latest_normal_number = int(''.join(filter(str.isdigit, latest_normal_name)))
            
#             # If there were no data rows, return 0
#             if not has_data:
#                 return 0, 0
            
#             # Extract the integer part of the batch number
#             latest_batch_number = int(''.join(filter(str.isdigit, latest_batch)))
            
#             return latest_batch_number, latest_normal_number
    
#     except FileNotFoundError:
#         # Return 0 if the file is not found
#         return 0, 0

import pandas as pd
import os

def latest_number():
    file_path = "Database/mapping.csv"
    # Initialize the output array
    output_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Check if csv exists or not, if not, return the initilized array
    if not os.path.exists(file_path):
        return output_array

    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Convert date and time to a single datetime column
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['Time'], format='mixed')

    # Sort the dataframe by datetime in descending order
    df = df.sort_values(by='datetime', ascending=False)


    # Define a dictionary to map study names to their respective indices in the output_array
    study_id_to_index = {
    #   'Batch':0,  DO NOT UN-COMMENT THIS LINE
        'Normal': 1,
        'Bleed-Epidural': 2,
        'Bleed-Subdural': 3,
        'Bleed-Subarachnoid': 4,
        'Bleed-Contusion': 5,
        'Bleed-Intraventricular': 6,
        'Bleed-Others': 7,
        'Midline Shift': 8,
        'Cervical Spine': 9,
        'Fracture': 10
    }

    # Iterate from the latest row to the earliest row
    for index, row in df.iterrows():
        # Batch number from column "batch_no"
        if output_array[0] == 0:
            output_array[0] = int(row['batch_no'][5:])  # Extract the integer part from the batch_no string

        # Update the corresponding index in the output_array based on "name_of_StudyID"
        study_id_parts = row['name_of_StudyID'].split('_')
        study_name = study_id_parts[0]
        if study_name in study_id_to_index:
            index_to_update = study_id_to_index[study_name]
            if output_array[index_to_update] == 0:
                output_array[index_to_update] = int(study_id_parts[1])

        # Check if all indices are filled
        if all(output_array):
            break

    return output_array



if __name__=="__main__":
    latest_number = latest_number()
    print(f"Array: {latest_number}")

