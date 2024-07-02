import requests
def log_message(log_file_path,message):
    with open(log_file_path, 'a') as file:
        file.write(message + '\n')

def anonymize_study(log_filepath,orthanc_url, study_id):
    """
    Anonymizes a specific study in Orthanc.
    
    Parameters:
    orthanc_url (str): The URL of the Orthanc server.
    study_id (str): The ID of the study to be anonymized.
    
    Returns:
    str: Success or error message.
    """
    anonymize_response = requests.post(
        f"{orthanc_url}/tools/bulk-anonymize",
        json={"Resources": [study_id]}
    )
    
    if anonymize_response.status_code == 200:
        # Reocrd in log File
        msg = f"Anonymized study {study_id} successfully"
        log_message(log_filepath,msg)
        return f"Anonymized study {study_id} successfully"
    else:
        # Reocrd in log File
        msg = f"Failed to anonymize study {study_id}: {anonymize_response.json()}"
        log_message(log_filepath,msg)
        return f"Failed to anonymize study {study_id}: {anonymize_response.json()}"


if __name__=="__main__":
    orthanc_url="http://localhost:8042"
    study_id="1971163a-26b23f46-66a62f33-229e6a17-9fddfee0"
    print(anonymize_study(orthanc_url,study_id))