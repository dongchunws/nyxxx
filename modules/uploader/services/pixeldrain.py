import os
import requests
import base64
from ...utils import TqdmUploadWrapper

def upload(file_path, api_key):
    """
    Uploads a file to Pixeldrain with a progress bar.
    
    :param file_path: Path to the file to upload.
    :param api_key: Pixeldrain API key (required).
    :return: A tuple (success: bool, message: str)
    """
    if not api_key:
        return (False, "Error: Pixeldrain API key is required.")

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    auth_string = f":{api_key}"
    auth_header = f"Basic {base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')}"
    
    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/octet-stream"
    }
    
    upload_url = f"https://pixeldrain.com/api/file/{file_name}"

    try:
        with open(file_path, 'rb') as f:
            wrapped_file = TqdmUploadWrapper(f, file_size, f"Uploading {file_name}")
            response = requests.put(upload_url, data=wrapped_file, headers=headers)
        
        response.raise_for_status()
        
        upload_data = response.json()
        if upload_data.get("id"):
            file_id = upload_data.get("id")
            return (True, f"https://pixeldrain.com/u/{file_id}")
        else:
            return (False, f"Upload failed: {upload_data.get('message', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        error_message = f"Error: {e}"
        if e.response:
            try:
                error_body = e.response.json()
                error_message += f" - {error_body.get('message', 'No details')}"
            except ValueError:
                error_message += f" - Status: {e.response.status_code}"
        return (False, error_message)
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")
