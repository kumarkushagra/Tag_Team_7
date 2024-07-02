# import requests
import os
import pandas as pd
import shutil
import requests
import csv
import datetime

from .Fetch_UHID import return_uhid_array
from .Generate_Full_dir_Path import join_paths
from .Generate_Batches_Dir import create_subdirectory
from .batch_number import latest_number
from .Copy_to_Batch_dir import *
from .UP_Upload_batch import *
from .UP_generate_series_path import generate_all_series_path
from .UP_update_master_csv import update_csv
from .UP_upload_each_series import upload_dicom_files
from .UP_anonymize_given_study import anonymize_study
from .UP_append_to_mapping_csv import append_to_csv
from .UP_delete_study import delete_studies
from .UP_rename_studyID import *
from .UP_list_UHIDs import list_subdirectories 
from .UP_new_study_from_array import *

def log_message(log_file_path,message):
    with open(log_file_path, 'a') as file:
        file.write(message + '\n')


def Upload(unzip_dir,anonymize_flag, csv_file_path,batch_size,log_filepath):

    UHIDs = return_uhid_array(log_filepath,csv_file_path, batch_size, "LLM", 0,"Uploaded", 0, "Patient ID (UHID)")
    
    # Reocrd in log File
    msg = f"UHIDs Short-lited are: {UHIDs}"
    log_message(log_filepath,msg)

    # print(UHIDs)

    # Modify this to accomodate all variables in 1 array rather than 11 variables
    # batch_number, latest_normal_number = latest_batch_number()[0],latest_batch_number()[1]
    '''     study_id_to_index = {
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
        }'''

    # Calling function: "latest_batch_number()" will return an array containing latest Numbers of all the names
    
    # CHANGES MADE HERE
    last_number = latest_number()
    
    # CHANGES MADE HERE
    # batch_Name = "Batch" + str(batch_number+1)
    batch_Name = "Batch" + str(last_number[0]+1)
        
    # Reocrd in log File
    msg = f"last Batch number: {last_number[0]}, Normal number: {last_number[1]}"
    log_message(log_filepath,msg)


    Paths_to_copy= join_paths(unzip_dir, UHIDs)

    # Reocrd in log File
    msg = f"Paths to copy: {Paths_to_copy}"
    log_message(log_filepath,msg)


    # Full path of BATCH0X i.e. just created 
    target_dir ="Contains_Batches/"+  batch_Name 
    print(target_dir)

    if not os.path.exists(target_dir):
        # Create a new directory because it does not exist
        os.makedirs(target_dir)
        # Reocrd in log File
        msg = f"Made a Directory to copy Studies into: {target_dir}"
        log_message(log_filepath,msg)


    # Copying files from Unziped DIR to Batches
    copy_directories_to_Batch_dir(log_filepath, csv_file_path, target_dir, Paths_to_copy)

    # copy_directories_to_Batch_dir(log_filepath, target_dir, Paths_to_copy)
    # Reocrd in log File
    msg = "---Batch Creation complete---"
    log_message(log_filepath,msg)


    # Uploading Entire Batch
    Upload_Batch(log_filepath, target_dir, anonymize_flag, csv_file_path, batch_Name, last_number) # last_number is an array containing all numbers    


if __name__=="__main__":
    csv_file_path="C:/Users/EIOT/Desktop/Final.csv"
    batch_size=2
    anonymize_flag= True
    target_dir="Contains_Batches/"
    unzip_dir="C:/Users/EIOT/Desktop/Unziped_dir"
    Upload(unzip_dir,anonymize_flag, target_dir,csv_file_path,batch_size)