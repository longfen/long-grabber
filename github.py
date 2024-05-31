import os
import zipfile
import requests
import shutil

def download_extract_zip(repo_url, dest_path):
    """Download a ZIP file from the specified GitHub repository and extract its contents."""
    response = requests.get(repo_url)
    zip_path = os.path.join(dest_path, 'temp.zip')
    with open(zip_path, 'wb') as f:
        f.write(response.content)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(dest_path)
    os.remove(zip_path)

def main():
    # GitHub repository URL
    repo_url = 'https://github.com/longfen/test/archive/main.zip'
    
    # Destination path (Documents folder)
    dest_path = os.path.expanduser('~/Documents')
    
    # Download and extract the ZIP file
    download_extract_zip(repo_url, dest_path)

if __name__ == "__main__":
    main()
