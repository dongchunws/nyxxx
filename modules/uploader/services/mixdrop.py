import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

def upload(file_path, email, api_key):
    """
    Uploads a file to Mixdrop.ag with a progress bar.
    
    :param file_path: Path to the file to upload.
    :param email: Mixdrop API E-Mail.
    :param api_key: Mixdrop API Key.
    :return: A tuple (success: bool, message: str)
    """
    if not email or not api_key:
        return (False, "Error: Mixdrop API E-Mail and Key are required.")

    upload_url = "https://ul.mixdrop.ag/api"
    file_name = os.path.basename(file_path)

    fields = {
        'email': email,
        'key': api_key,
        'file': (file_name, open(file_path, 'rb'), 'application/octet-stream')
    }

    encoder = MultipartEncoder(fields=fields)
    
    with tqdm(total=encoder.len, unit='B', unit_scale=True, desc=f"Uploading {file_name}") as pbar:
        monitor = MultipartEncoderMonitor(encoder, lambda mon: pbar.update(mon.bytes_read - pbar.n))
        
        try:
            response = requests.post(upload_url, data=monitor, headers={'Content-Type': monitor.content_type})
            response.raise_for_status()
            
            upload_data = response.json()
            if upload_data.get("success"):
                return (True, upload_data.get("result", {}).get("url", "Success, but no URL found."))
            else:
                return (False, f"Upload failed. Full response: {upload_data}")

        except requests.exceptions.RequestException as e:
            error_message = f"Error: {e}"
            if e.response:
                error_message += f" - Status: {e.response.status_code}, Body: {e.response.text}"
            return (False, error_message)
        except Exception as e:
            return (False, f"An unexpected error occurred: {e}")
