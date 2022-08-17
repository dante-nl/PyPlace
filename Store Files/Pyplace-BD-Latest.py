
# ██████╗░██╗░░░██╗██████╗░██╗░░░░░░█████╗░░█████╗░███████╗  ░░░░░░  
# ██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔════╝  ░░░░░░  
# ██████╔╝░╚████╔╝░██████╔╝██║░░░░░███████║██║░░╚═╝█████╗░░  █████╗  
# ██╔═══╝░░░╚██╔╝░░██╔═══╝░██║░░░░░██╔══██║██║░░██╗██╔══╝░░  ╚════╝  
# ██║░░░░░░░░██║░░░██║░░░░░███████╗██║░░██║╚█████╔╝███████╗  ░░░░░░  
# ╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝  ░░░░░░  

# ██████╗░██╗░░░██╗██╗░░░░░██╗░░██╗  ██████╗░███████╗██╗░░░░░███████╗████████╗███████╗
# ██╔══██╗██║░░░██║██║░░░░░██║░██╔╝  ██╔══██╗██╔════╝██║░░░░░██╔════╝╚══██╔══╝██╔════╝
# ██████╦╝██║░░░██║██║░░░░░█████═╝░  ██║░░██║█████╗░░██║░░░░░█████╗░░░░░██║░░░█████╗░░
# ██╔══██╗██║░░░██║██║░░░░░██╔═██╗░  ██║░░██║██╔══╝░░██║░░░░░██╔══╝░░░░░██║░░░██╔══╝░░
# ██████╦╝╚██████╔╝███████╗██║░╚██╗  ██████╔╝███████╗███████╗███████╗░░░██║░░░███████╗
# ╚═════╝░░╚═════╝░╚══════╝╚═╝░░╚═╝  ╚═════╝░╚══════╝╚══════╝╚══════╝░░░╚═╝░░░╚══════╝

# 🄱🅈 🄳🄰🄽🅃🄴_🄽🄻
# Welcome to the PyPlace Bulk Delete script! This is an official
# and experimental thing for PyPlace, that allows you to delete
# a bunch of applications at once.

# 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝘃𝗲𝗿𝘀𝗶𝗼𝗻
# Default: 0.1 (changes	every version)
# Possible options: any number

# This is the version of PyPlace - Bulk Delete and is
# absolutely not recommended to change,
# except for testing purposes.
Version = 0.1

# ————————————————————————————

import os
import sys
import json
import requests
from os.path import	exists

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


if exists("setup.json") == False:
	print(f"{bcolors.FAIL}Error:{bcolors.END} It appears you have not set up PyPlace yet! Please run PyPlace and set it up.")
	sys.exit(0)

def error(error_msg):
	print(f"{bcolors.FAIL}Error:{bcolors.END} {error_msg}")

def info(info_msg):
	print(f"{bcolors.INFO}{info_msg}{bcolors.END}")

if exists("setup.json") == True:
    with open('setup.json') as SetupFile:
        _data = json.load(SetupFile)
        PyCommand = _data["PythonCommand"]

with open('applications.json') as AppsFile:
	AppDict = json.load(AppsFile)

def update():
	response = requests.get("https://cdn.dantenl.tk/PyPlace/bd-version.json")
	if response.status_code != 200:
		print(f"{bcolors.FAIL}Error:{bcolors.END} Could not check for updates! Response code: {response.status_code}")
		return

	RequestText = response.text
	data = json.loads(RequestText)

	if data["version"] < Version:
		print(f"{bcolors.WARNING}WARNING:{bcolors.END} Your current version seems to be newer than the latest version that is released!")
	elif data["version"] > Version:
		print("————————")
		print(f"{bcolors.BOLD}UPDATE AVAILABLE!{bcolors.END}")
		print(
			f"Your current version ({Version}) is no longer the latest version! The latest one is {data['version']}")
		print(f"""Here are the release notes:
	{data["release_notes"]}
		""")
		NotAnswered = True
		while NotAnswered == True:
			Answer = input("Would you like to update right now? (y/n) ")
			Answer = Answer.lower()
			if Answer == "y":
				NotAnswered = False
				print(
					f"{bcolors.INFO}Downloading latest version of PyPlace...{bcolors.END}")
				r = requests.get(
					"https://cdn.dantenl.tk/PyPlace/PyPlace-BD-Latest.py", allow_redirects=True)
				if not r.ok:
					print(f"{bcolors.FAIL}Error:{bcolors.END} Could not get the PyPlace file! Status code: {r.status_code}")
					return
				open('PyPlace.py', 'wb').write(r.content)
				print(
					f"{bcolors.OKGREEN}The latest version of PyPlace is now ready in {bcolors.BOLD}PyPlace.py!{bcolors.END}")
				NotAnswered2 = True
				while NotAnswered2 == True:
					Answer2 = input("Would you like to run it? (y/n) ")
					Answer2 = Answer2.lower()
					if Answer2 == "y":
						print(
							f"{bcolors.INFO}Attempting to run PyPlace.py...{bcolors.END}")
						os.system(f"{PyCommand} PyPlace.py")
						NotAnswered2 = False
						sys.exit(1)
					elif Answer2 == "n":
						print(
							f"Continuing with current version. {bcolors.BOLD}NOTE:{bcolors.END} Next time you start PyPlace.py, it will be on the latest version!")
						NotAnswered2 = False
						return
					else:
						print(
							f"{bcolors.FAIL}Error:{bcolors.END} I'm not sure what you mean with \"{Answer2}\".")

def bulk_delete(nums):
	if exists("applications.json") == False:
		error("You do not have any applications installed.")
		return "Error"
	info(f"Deleting {len(nums)} apps...")
	RightApps = []
	for number in nums:
		current_num_app_dict = 0
		for app in AppDict["apps"]:
			current_num_app_dict += 1
			if str(current_num_app_dict) == str(number):
				RightApps.append(app)

	for RightApp in RightApps:
		if exists(AppDict["apps"][RightApp]["file_name"]):
			os.remove(AppDict["apps"][RightApp]["file_name"])
		del AppDict["apps"][RightApp]
		with open('applications.json', 'w') as data_file:
				data = json.dump(AppDict, data_file,
									indent=4,
									separators=(',', ': '))
	
	print(f"{bcolors.OKGREEN}Deleted {len(nums)} app(s)!{bcolors.END}")

print()
print("""————————————————————————————
Welcome to the PyPlace Bulk Delete script! This is an official
and experimental thing for PyPlace, that allows you to delete
a bunch of applications at once.
""")

update()

num_app = 0
for item in AppDict["apps"]:
	num_app += 1
	print(f"[{num_app}] {AppDict['apps'][item]['name']}")

if num_app == 0:
	error("You do not have any applications installed!")
	sys.exit(0)

input = input("What apps do you want to delete? (seperated by a comma, so for applications 1, 2 and 3 you would enter 1,2,3) ")
input = input.split(",")
bulk_delete(input)
