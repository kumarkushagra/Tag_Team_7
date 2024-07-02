import os
import csv
import shutil

def log_message(log_file_path,message):
    with open(log_file_path, 'a') as file:
        file.write(message + '\n')

def cut_and_paste_row(input_csv_filename,  patient_path, error_code):
    output_csv_filename = 'Logs/UHID error/output.csv'
    try:
        # Extract the Patient UHID from the path
        normalized_path = os.path.normpath(patient_path)
        components = normalized_path.split(os.sep)
        uhid_value = components[-1]
        
        # Read the input CSV and identify the rows to be cut
        rows_to_write = []
        remaining_rows = []
        with open(input_csv_filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames + ['ERROR CODE']
            
            for row in reader:
                if row['Patient ID (UHID)'] == uhid_value:
                    row['ERROR CODE'] = error_code
                    rows_to_write.append(row)
                else:
                    remaining_rows.append(row)
        
        if rows_to_write:
            # Write the identified rows to the output CSV, appending if the file exists
            if os.path.exists(output_csv_filename):
                with open(output_csv_filename, 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerows(rows_to_write)
            else:
                with open(output_csv_filename, 'w', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows_to_write)
            
            # Write the remaining rows back to the input CSV
            with open(input_csv_filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(remaining_rows)
            
            print(f"Rows with UHID '{uhid_value}' have been cut from '{input_csv_filename}' and appended to '{output_csv_filename}' with error code '{error_code}'.")
        else:
            print(f"No rows found with UHID '{uhid_value}' in '{input_csv_filename}'.")
            
    except FileNotFoundError:
        print(f"Error: File '{input_csv_filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def copy_directories_to_Batch_dir(log_filepath, input_csv_filename, target_dir, directory_paths_array):
    """
    Copies directories specified in directory_paths to the target directory.

    Parameters:
    - target_dir (str): Path to the target directory where directories will be copied.
    - directory_paths (list): List of paths to the directories that need to be copied.

    Returns:
    - None
    """
    for dir_path in directory_paths_array:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            dir_name = os.path.basename(dir_path)
            target_path = os.path.join(target_dir, dir_name)

            # Check if the directory already exists in the target location
            # if os.path.exists(target_path):
            #     print(f"Directory '{dir_name}' already exists in the target directory.")
        
            try:
                shutil.copytree(dir_path, target_path)
                print(f"Directory '{dir_name}' successfully copied to '{target_dir}'.")

                # Reocrd in log File
                msg = f"Directory '{dir_name}' successfully copied to '{target_dir}'"
                log_message(log_filepath,msg)

            except Exception as e:
                print(f"Failed to copy directory '{dir_name}': {str(e)}")
                cut_and_paste_row(input_csv_filename,  dir_path, str(e))

                # Reocrd in log File
                msg = f"Failed to copy directory '{dir_name}': {str(e)}"
                log_message(log_filepath,msg)

                
        else:
            print(f"Directory '{dir_path}' does not exist or is not a valid directory.")
            cut_and_paste_row(input_csv_filename,  dir_path, "Invalid Directory")

            # Reocrd in log File
            msg = f"Directory '{dir_path}' does not exist or is not a valid directory"
            log_message(log_filepath,msg)


# Example usage:
if __name__ == "__main__":
    target_directory = "C:/Users/EIOT/Desktop/Target"
    directories_to_copy = join_paths("C:/Users/EIOT/Desktop/Unziped_dir",["105325641","500261503"])

    copy_directories_to_Batch_dir(target_directory, directories_to_copy)
