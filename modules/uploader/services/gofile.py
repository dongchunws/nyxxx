import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

def upload(file_path, api_key=None):
    """
    Uploads a file to Gofile with a progress bar.
    
    :param file_path: Path to the file to upload.
    :param api_key: Optional Gofile API key for authenticated upload.
    :return: A tuple (success: bool, message: str)
    """
    try:
        upload_url = "https://upload.gofile.io/uploadfile"
        headers = {}

        if api_key:
            server_response = requests.get("https://api.gofile.io/getServer")
            server_response.raise_for_status()
            server_data = server_response.json()
            if server_data["status"] == "ok":
                server_name = server_data["data"]["server"]
                upload_url = f"https://{server_name}.gofile.io/uploadFile"
                headers["Authorization"] = f"Bearer {api_key}"
            else:
                return (False, f"Warning: Could not get best server for Gofile. Using default upload URL. {server_data.get('message', '')}")
        
        file_name = os.path.basename(file_path)

        encoder = MultipartEncoder(fields={'file': (file_name, open(file_path, 'rb'), 'application/octet-stream')})
        
        with tqdm(total=encoder.len, unit='B', unit_scale=True, desc=f"Uploading {file_name}") as pbar:
            monitor = MultipartEncoderMonitor(encoder, lambda mon: pbar.update(mon.bytes_read - pbar.n))
            headers['Content-Type'] = monitor.content_type
            response = requests.post(upload_url, data=monitor, headers=headers)
        
        response.raise_for_status()
        
        upload_data = response.json()
        if upload_data["status"] == "ok":
            return (True, upload_data.get("data", {}).get("downloadPage", "Success, but no link found."))
        else:
            return (False, f"Upload failed: {upload_data.get('message', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        return (False, f"Error: {e}")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")
