
# ██████╗░██╗░░░██╗██████╗░██╗░░░░░░█████╗░░█████╗░███████╗  ░░░░░░
# ██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔════╝  ░░░░░░
# ██████╔╝░╚████╔╝░██████╔╝██║░░░░░███████║██║░░╚═╝█████╗░░  █████╗
# ██╔═══╝░░░╚██╔╝░░██╔═══╝░██║░░░░░██╔══██║██║░░██╗██╔══╝░░  ╚════╝
# ██║░░░░░░░░██║░░░██║░░░░░███████╗██║░░██║╚█████╔╝███████╗  ░░░░░░
# ╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝  ░░░░░░

# ░██████╗░██╗░░░██╗██╗░█████╗░██╗░░██╗░██████╗████████╗░█████╗░██████╗░████████╗
# ██╔═══██╗██║░░░██║██║██╔══██╗██║░██╔╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
# ██║██╗██║██║░░░██║██║██║░░╚═╝█████═╝░╚█████╗░░░░██║░░░███████║██████╔╝░░░██║░░░
# ╚██████╔╝██║░░░██║██║██║░░██╗██╔═██╗░░╚═══██╗░░░██║░░░██╔══██║██╔══██╗░░░██║░░░
# ░╚═██╔═╝░╚██████╔╝██║╚█████╔╝██║░╚██╗██████╔╝░░░██║░░░██║░░██║██║░░██║░░░██║░░░
# ░░░╚═╝░░░░╚═════╝░╚═╝░╚════╝░╚═╝░░╚═╝╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░

# 🄱🅈 🄳🄰🄽🅃🄴_🄽🄻

# Welcome to PyPlace - Quickstart! This app allows you to
# dive in to PyPlace without any problems, and some
# applications to start out with too!

# NOTE: This app is currently an experiment, and might
# get removed and/or it might not work properly.

# ————————————————————————————
import os
import sys
import json
import requests
from os.path import exists

class bcolors:
	LOG = '\033[95m'
	INFO = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

if exists("setup.json"):
	with open('setup.json') as SetupFile:
		_ = json.load(SetupFile)
		PythonCommand = _["PythonCommand"]

def setup():
	print("What command do you use to run a Python file in your terminal?")
	print("Leave empty to set it to the default (python3)")
	print(f"{bcolors.BOLD}NOTE: {bcolors.END}You can change this later in the settings.")
	PythonCommand = input("> ") or "python3"

	print(f"{bcolors.INFO}Setting up PyPlace...{bcolors.END}")

	AppDict = {
		"_NOTE": "When you delete this file, PyPlace can no longer interact with any downloaded applications.",
		"apps": {
		}
	}

	with open("applications.json", 'w') as json_file:
		json.dump(AppDict, json_file,
			indent=4,
			separators=(',', ': '))

	SetupDict = {
		"_comment1": "PYPLACE SETUP FILE",
		"_comment2": "This is an important file for PyPlace, because your settings are stored here! It is NOT recommended to delete or edit this file.",
		"_comment3": "Thanks for using PyPlace - Quickstart to set up PyPlace!",
		"SetupVersion": 0.1,
		"PythonCommand": f"{PythonCommand}"
	}

	SetupDictStr = json.dumps(SetupDict, indent=4, separators=(',', ': '))
	with open('setup.json', 'w') as SetupJSON:
		SetupJSON.write(SetupDictStr)

	print(f"{bcolors.OKGREEN}PyPlace is set up!{bcolors.END}")

def quickstart():
	StoreRequest = requests.get("https://cdn.dantenl.tk/pyplace/store.json", allow_redirects=True)
	if not StoreRequest.ok:
		print(f"{bcolors.FAIL}Error:{bcolors.END} Could not connect to the PyPlace Experiment Store! Response code: {StoreRequest.status_code}")
		return
	StoreRequestText = StoreRequest.text
	StoreRequestJSON = json.loads(StoreRequestText)

	download("Simple Password Gen", "Simple-Password-Generator.py", StoreRequestJSON)
	download("Calculator", "Calculator.py", StoreRequestJSON)
	download("dictiona.py", "dictiona.py", StoreRequestJSON)
	download("Rock, paper, scissors", "Rock-Paper-Scissors.py", StoreRequestJSON)
	download("Hangman", "Hangman.py", StoreRequestJSON)
	try:
		download("PyPlace Bulk Delete", "PyPlace-bulk-delete.py", StoreRequestJSON)
	except KeyError:
		print(f"{bcolors.INFO}NOTE:{bcolors.END} The PyPlace Bulk Delete app can not be installed yet, as it's still an experiment. You can download it from the experiment store in PyPlace.")

	print(exists("pyplace.py"))
	if exists("pyplace.py") == False:
		print(f"{bcolors.INFO}Downloading and installing PyPlace...{bcolors.END}")
		r = requests.get("https://cdn.dantenl.tk/PyPlace/PyPlace-Latest.py", allow_redirects=True)
		if not r.ok:
			print(f"{bcolors.FAIL}Error:{bcolors.END} Could not get the PyPlace file! Status code: {r.status_code}")
			return
		open('PyPlace.py', 'wb').write(r.content)
		print(f"{bcolors.OKGREEN}Installed PyPlace! You can run it in {bcolors.BOLD}PyPlace.py!{bcolors.END}")
		NotAnswered2 = True
		while NotAnswered2 == True:
			Answer2 = input("Would you like to run it? (y/n) ")
			Answer2 = Answer2.lower()
			if Answer2 == "y":
				print(f"{bcolors.INFO}Attempting to run PyPlace.py...{bcolors.END}")
				os.system(f"{PythonCommand} PyPlace.py")
				NotAnswered2 = False
				sys.exit(1)
			else:
				return

def download(OfficialName, FileName, StoreRequestJSON):
	"""Download an application from the PyPlace store."""
	Name = StoreRequestJSON["apps"][OfficialName]["name"]
	Author = StoreRequestJSON["apps"][OfficialName]["author"]
	print(f"{bcolors.INFO}Attempting to download and install \"{Name}\"...{bcolors.END}")
	AppRequest = requests.get(StoreRequestJSON['apps'][OfficialName]['url'], allow_redirects=True)
	if not AppRequest.ok:
		print(f"{bcolors.FAIL}Error:{bcolors.END} Could not connect to the file! Response code: {AppRequest.status_code}")
		return
	else:
		open(FileName, 'wb').write(AppRequest.content)
		with open('applications.json') as ApplicationsFile1:
				data3 = json.load(ApplicationsFile1)

				data3["apps"].update(
					{
						f"{Name} (Quickstart Installed)": {
							"name": f"{Name}",
							"file_name": f"{FileName}",
							"author": f"{Author}",
							"StoreApp": "true"
						}
					})
				with open("applications.json", 'w') as json_file:
					json.dump(data3, json_file,
							indent=4,
							separators=(',', ': '))
		print(f"{bcolors.OKGREEN}Downloaded file!{bcolors.END}")
		print()

print()
print("""————————————————————————————
Welcome to PyPlace - Quickstart! This app allows you to
dive in to PyPlace without any problems, and some
applications to start out with too!""")
if exists("setup.json") == False:
	setup()
quickstart()
