import os
import requests
from tqdm import tqdm
import math

def upload(file_path, api_key=None):
    """
    Uploads a file to Vikingfiles with a multi-part upload process and progress bar.
    
    :param file_path: Path to the file to upload.
    :param api_key: Optional Vikingfiles API key (user's hash) for authenticated upload.
    :return: A tuple (success: bool, message: str)
    """
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    user_hash = api_key if api_key else ""

    try:
        # Step 1: Get upload URL
        print(f"[{file_name}] Requesting upload URL from Vikingfiles...")
        get_upload_url_response = requests.post(
            "https://vikingfile.com/api/get-upload-url",
            data={'size': file_size}
        )
        get_upload_url_response.raise_for_status()
        upload_info = get_upload_url_response.json()

        if 'urls' not in upload_info:
            return (False, f"Failed to get upload URLs. Response: {upload_info}")

        upload_id = upload_info['uploadId']
        key = upload_info['key']
        part_size = upload_info['partSize']
        urls = upload_info['urls']
        
        uploaded_parts = []
        with open(file_path, 'rb') as f:
            with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Uploading {file_name}") as pbar:
                for i, url in enumerate(urls):
                    part_number = i + 1
                    chunk = f.read(part_size)
                    
                    if not chunk:
                        break

                    part_response = requests.put(url, data=chunk)
                    part_response.raise_for_status()
                    
                    etag = part_response.headers.get('ETag')
                    if not etag:
                        return (False, f"Error: ETag not found for part {part_number}")

                    uploaded_parts.append({'PartNumber': part_number, 'ETag': etag})
                    pbar.update(len(chunk))

        # Step 3: Complete upload
        print(f"[{file_name}] Completing upload...")
        complete_upload_response = requests.post(
            "https://vikingfile.com/api/complete-upload",
            data={
                'key': key,
                'uploadId': upload_id,
                'name': file_name,
                'user': user_hash,
                **{f'parts[{idx}][PartNumber]': part['PartNumber'] for idx, part in enumerate(uploaded_parts)},
                **{f'parts[{idx}][ETag]': part['ETag'] for idx, part in enumerate(uploaded_parts)}
            }
        )
        complete_upload_response.raise_for_status()
        final_info = complete_upload_response.json()

        if 'url' in final_info:
            return (True, final_info['url'])
        else:
            return (False, f"Upload failed: {final_info.get('error', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        return (False, f"Error: {e}")
    except Exception as e:
        return (False, f"An unexpected error occurred: {e}")
