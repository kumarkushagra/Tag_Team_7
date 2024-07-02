import requests
 
def transfer_studies(source_url, destination_url):
    # Get the list of studies from the source Orthanc
    response = requests.get(f"{source_url}/studies")
    if response.status_code != 200:
        print(f"Failed to get studies from source Orthanc: {response.status_code}")
        return
 
    studies = response.json()
 
    for study in studies:
        print(f"Sending study: {study}")
 
        # Download the study as a ZIP file and stream it directly to the destination
        archive_url = f"{source_url}/studies/{study}/archive"
        with requests.get(archive_url, stream=True) as r:
            if r.status_code != 200:
                print(f"Failed to download study {study}: {r.status_code}")
                continue

            # Stream the downloaded ZIP file directly to the destination Orthanc
            upload_response = requests.post(
                f"{destination_url}/instances",
                headers={"Content-Type": "application/zip"},
                data=r.iter_content(chunk_size=8192) # 8192 bytes (8 kb)
                # if memory is the constraint, reduce this number 
            )
            if upload_response.status_code != 200:
                print(f"Failed to upload study {study} to destination Orthanc: {upload_response.status_code}")
            else:
                print(f"Study {study} transferred successfully.")
 
# Example usage
if __name__=="__main__":
    source_orthanc = "http://localhost:8042"
    destination_orthanc = "http://localhost:1111"
    transfer_studies(source_orthanc, destination_orthanc)