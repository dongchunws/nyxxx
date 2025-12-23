import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor
from tqdm import tqdm

def upload(file_path, api_key=None):
    """
    Uploads a file to Catbox.moe with a progress bar.
    
    :param file_path: Path to the file to upload.
    :param api_key: Optional Catbox.moe userhash for authenticated upload.
    :return: A tuple (success: bool, message: str)
    """
    upload_url = "https://catbox.moe/user/api.php"
    file_name = os.path.basename(file_path)

    fields = {
        'reqtype': 'fileupload',
        'fileToUpload': (file_name, open(file_path, 'rb'), 'application/octet-stream')
    }
    
    if api_key:
        fields['userhash'] = api_key

    encoder = MultipartEncoder(fields=fields)
    
    with tqdm(total=encoder.len, unit='B', unit_scale=True, desc=f"Uploading {file_name}") as pbar:
        monitor = MultipartEncoderMonitor(encoder, lambda mon: pbar.update(mon.bytes_read - pbar.n))
        
        try:
            response = requests.post(upload_url, data=monitor, headers={'Content-Type': monitor.content_type})
            response.raise_for_status()
            
            if response.text and response.text.startswith('http'):
                return (True, response.text)
            else:
                return (False, f"Upload failed. Response: {response.text}")

        except requests.exceptions.RequestException as e:
            return (False, f"Error: {e}")
        except Exception as e:
            return (False, f"An unexpected error occurred: {e}")
