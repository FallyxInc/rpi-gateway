import requests
import os
import time

def upload_json_to_api(file_path: str, api_url: str, headers: dict = None) -> None:
    """
    Upload a JSON file to a REST API.

    :param file_path: Path to the JSON file to upload.
    :param api_url: URL of the REST API endpoint.
    :param headers: Optional headers to include in the request (e.g., for authentication).
    :return: None
    """
    try:
        # Open the JSON file
        with open(file_path, 'rb') as file:
            # Create a dictionary to represent the file payload
            files = {'file': (file_path, file, 'application/json')}
            
            # Send a POST request to the API
            response = requests.post(api_url, data=file, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                print("File uploaded successfully.")
                print("Response:", response.json())
            else:
                f = open("error_log.txt", "a")
                f.write(f"Failed to upload file. Status code: {response.status_code}")
                f.write(f"Response: {response.text}")
                #now = time.datetime.now()
                #current= now.strftime("%H:%M:%S") 
                #f.write(f"Time: {current}")
                f.write("-------------------------------")
                print(f"Failed to upload file. Status code: {response.status_code}")
                print("Response:", response.text)
                

    except Exception as e:

        f = open("error_log.txt", "a")
        f.write(f"Error upload file: {e}")
        #now = time.datetime.now()
        #current= now.strftime("%H:%M:%S") 
        #f.write(f"Time: {current}")
        f.write("-------------------------------")

        print(f"Error uploading file: {e}")

def get_json_files_from_directory(directory_path: str) -> list:
    """
    Get a list of all JSON files in a given directory.

    :param directory_path: Path to the directory to scan for JSON files.
    :return: List of paths to JSON files.
    """
    json_files = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.json')]
    return json_files

def get_oldest_file(files: list) -> str:
    """
    Get the path to the oldest file in a list of files.

    :param files: List of file paths.
    :return: Path to the oldest file.
    """
    if not files:
        return None

    # Initialize with the first file
    oldest_file = files[0]
    oldest_time = os.path.getmtime(oldest_file)

    for file in files[1:]:
        file_time = os.path.getmtime(file)
        if file_time < oldest_time:
            oldest_file = file
            oldest_time = file_time

    return oldest_file

def send_to_rest_api(api_url, file):
    # Define optional headers if needed (e.g., for authentication)
    headers = {
           'Content-Type': 'application/json'  # Optional: specify content type if required
    }

    # Upload the file
    upload_json_to_api(file, api_url, headers)



def main():
    api_url = "http://3.98.214.27/inference"
    script_directory = os.path.dirname(os.path.abspath(__file__))
    while(True):
        file_names = get_json_files_from_directory(script_directory) 
        if len(file_names) > 1:
            out_file = get_oldest_file(file_names)
            print("Sending: ")
            print(out_file)
            send_to_rest_api(api_url, out_file)
            time.sleep(10)
            os.remove(out_file)




if __name__ == "__main__":
    main()
