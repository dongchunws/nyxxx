import os
import requests
from ...utils import TqdmUploadWrapper

def upload(file_path, api_key=None):
    """
    Uploads a file to Buzzheavier with a progress bar.
    
    :param file_path: Path to the file to upload.
    :param api_key: Optional Buzzheavier API key (ACCOUNT_ID) for authenticated upload.
    :return: A tuple (success: bool, message: str)
    """
    file_name = os.path.basename(file_path)
    
    upload_url = f"https://w.buzzheavier.com/{file_name}"
    headers = {}

    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        with open(file_path, 'rb') as f:
            wrapped_file = TqdmUploadWrapper(f, os.path.getsize(file_path), f"Uploading {file_name}")
            response = requests.put(upload_url, data=wrapped_file, headers=headers)
        
        response.raise_for_status()
        
        if response.status_code in [200, 201]:
            try:
                upload_data = response.json()
                file_id = upload_data.get("data", {}).get("id")
                if file_id:
                    return (True, f"https://buzzheavier.com/f/{file_id}")
                else:
                    return (False, f"Success, but couldn't parse ID. Full response: {upload_data}")
            except ValueError:
                return (False, response.text.strip() if response.text else "Success, but no URL found.")
        else:
            return (False, f"Upload failed. Status: {response.status_code}. Response: {response.text}")

    except requests.exceptions.RequestException as e:
        error_message = f"Error: {e}"
        if e.response:
            error_message += f" - Status: {e.response.status_code}, Body: {e.response.text}"
        return (False, error_message)
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")
