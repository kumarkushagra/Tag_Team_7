'''Renaming The Studies On PACS, (mapping will be handeled accordingly)'''


"""

define a python function that inputs a CSV file named "mapping.csv" path and returns an array of numbers
by reffering a Column named "name_of_StudyID"
this column contains 9 values i.e. 
1) Batch number<int>
2) Normal<int>
3) Bleed-Epidural<int>
4) Bleed-Subdural<int>
5) Bleed-Subarachnoid<int>
6) Bleed-Contusion<int>
7) Bleed-Intraventricular<int>
8) Bleed-Others<int>
9) Midline Shift<int>
10) Cervical Spine<int>
11) Fracture<int>


if there exists such a name in mapping.csv, return the largest number, else return 0 

"""


""" NEW PROMPT
define a python function that inputs a CSV file named "mapping.csv" path and returns an array containing 11 elements
each index position stands 

"""

import pandas as pd
import os

def latest():
    file_path = "Database/mapping.csv"
    # Initialize the output array
    output_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Check if csv exists or not, if not, return the initilized array
    if not os.path.exists(file_path):
        return output_array

    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Convert date and time to a single datetime column
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['Time'], format='%d-%m-%Y %H:%M.%S')

    # Sort the dataframe by datetime in descending order
    df = df.sort_values(by='datetime', ascending=False)


    # Define a dictionary to map study names to their respective indices in the output_array
    study_id_to_index = {
        # Batch : 0, DO NOT UN-comment this line, Batches are handeled below
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

# Call the function and print the output
if __name__=="__main__":
    print(latest())
