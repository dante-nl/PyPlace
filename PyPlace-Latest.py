
# ██████╗░██╗░░░██╗██████╗░██╗░░░░░░█████╗░░█████╗░███████╗
# ██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔════╝
# ██████╔╝░╚████╔╝░██████╔╝██║░░░░░███████║██║░░╚═╝█████╗░░
# ██╔═══╝░░░╚██╔╝░░██╔═══╝░██║░░░░░██╔══██║██║░░██╗██╔══╝░░
# ██║░░░░░░░░██║░░░██║░░░░░███████╗██║░░██║╚█████╔╝███████╗
# ╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝

# 🄱🅈 🄳🄰🄽🅃🄴_🄽🄻

# Welcome to PyPlace! PyPlace is an easy-to-use Python
# application that allows you to open and install
# various Python applications. PyPlace is designed to
# be as easy to use, so everyone can use it! :D


# ————————————————————————————
# Below you can change more advanced settings,
# that are hard-coded in to PyPlace.
# We only recommend changing these settings
# when you know what you are doing.

# 𝗘𝗻𝗮𝗯𝗹𝗲 𝗼𝗿 𝗱𝗶𝘀𝗮𝗯𝗹𝗲 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗳𝗼𝗿 𝘂𝗽𝗱𝗮𝘁𝗲𝘀
# Default: True
# Possible options: True, False

# Do you want to check for updates when the
# program is ran? You can always check for
# updates via the advanced options.
# 𝗡𝗢𝗧𝗘: When Replit mode is enabled,
# this setting is ignored.
CheckForUpdates = True

# 𝗘𝗻𝗮𝗯𝗹𝗲 𝗼𝗿 𝗱𝗶𝘀𝗮𝗯𝗹𝗲 𝗹𝗼𝗴𝘀
# Default: True
# Possible options: True, False

# Do you want to see exactly what PyPlace
# is doing? This might clutter the output
# with various small things, such as when
# a file is created.
DoNotLogOutput = True

# 𝗘𝗻𝗮𝗯𝗹𝗲 𝗼𝗿 𝗱𝗶𝘀𝗮𝗯𝗹𝗲 𝘁𝗵𝗲 𝗺𝗮𝗶𝗻 𝘀𝗰𝗿𝗶𝗽𝘁
# Default: True
# Possible options: True, False

# This is mainly for stopping PyPlace
# while it is executing, and for allowing
# the code to be looped infinitely.
# NOTE: This should not be touched
DoINeedToRun = True

# 𝗘𝗻𝗮𝗯𝗹𝗲 𝗼𝗿 𝗱𝗶𝘀𝗮𝗯𝗹𝗲 𝗥𝗲𝗽𝗹𝗶𝘁 𝗺𝗼𝗱𝗲
# Default: False
# Possible options: True, False

# This decides whether PyPlace should
# run like it is being executed from
# the official Replit page, this
# disables settings such as updating,
# ignores file names and gives a 
# warning each time you run it.
ReplitMode = False

# 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝘃𝗲𝗿𝘀𝗶𝗼𝗻
# Default: 0.6 (changes every version)
# Possible options: any number

# This is the version of PyPlace and is
# absolutely not recommended to change,
# except for testing purposes.
Version = 0.6


# ————————————————————————————
# Below this line of text, everything
# that is needed in PyPlace is imported.
# It is absolutely NOT recommended to
# edit this as it can BREAK PyPlace!
import os
import re
import sys
import json
import requests
from os.path import exists


# ————————————————————————————
# Below is the main code, it is not
# recommended to edit it, as it might affect
# how well PyPlace runs.

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

if exists("setup.json") == True:
	with open('setup.json') as SetupFile:
		_data = json.load(SetupFile)
		PyCommand = _data["PythonCommand"]

FileName = f"{os.path.splitext(os.path.basename(__file__))[0]}.py"
FileNameWarning = False
print(FileName)
if ReplitMode == True:
	CheckForUpdates = False
else:
	if FileName.lower() != "pyplace.py":
		FileNameWarning = True


def log(message):
	if DoNotLogOutput == False:
		print(f"{bcolors.LOG}Log:{bcolors.END} {message}")

def UpdateCheck():
	log("Checking for latest version...")
	response = requests.get("https://cdn.dantenl.tk/PyPlace/version.json")
	if response.status_code != 200:
		print(f"{bcolors.FAIL}Error:{bcolors.END} Could not check for updates! Response code: {response.status_code}")
		return

	log("Comparing versions...")

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
				log("Retrieving latest version of PyPlace...")
				r = requests.get(
					"https://cdn.dantenl.tk/PyPlace/PyPlace-Latest.py", allow_redirects=True)
				if not r.ok:
					print(f"{bcolors.FAIL}Error:{bcolors.END} Could not get the PyPlace file! Status code: {r.status_code}")
					return
				log("Updating main PyPlace file")
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

			elif Answer == "n":
				NotAnswered = False
				print("Update cancelled!")
				return
			else:
				print(
					f"{bcolors.FAIL}Error:{bcolors.END} I'm not sure what you mean with \"{Answer}\".")


def ExecuteFile():
	if exists("applications.json") == False:
		print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
		return


	with open('applications.json') as AppsFile:
		json_data = json.load(AppsFile)
	
	if "apps" in json_data == False:
		print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
		return

	print(f"{bcolors.WARNING}■{bcolors.END}: Experimental application")
	print(f"{bcolors.OKCYAN}■{bcolors.END}: Application downloaded from the PyPlace store")
	print()
	ItemCount = 0
	for item in json_data["apps"]:
		ItemCount += 1
		if "StoreApp" in json_data['apps'][item]:
			if json_data['apps'][item]["StoreApp"] == "true":
				print(f"{bcolors.OKCYAN}[{ItemCount}] {json_data['apps'][item]['name']} by {json_data['apps'][item]['author']}{bcolors.END}")
		elif "experiment" in json_data['apps'][item]:
			if json_data['apps'][item]["experiment"] == "true":
				print(f"{bcolors.WARNING}[{ItemCount}] {json_data['apps'][item]['name']}{bcolors.END}")
		else:
			if "author" in json_data['apps'][item]:
				print(f"[{ItemCount}] {json_data['apps'][item]['name']} by {json_data['apps'][item]['author']}")
			else:
				print(f"[{ItemCount}] {json_data['apps'][item]['name']}")
	
	if ItemCount == 0:
		print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
		return

	print(f"[{bcolors.FAIL}c{bcolors.END}] Cancel")

	NumberAppNeeded = input("What number app do you want to open? ")
	ItemCount2 = 0
	for item in json_data["apps"]:
		ItemCount2 += 1
		if str(ItemCount2) == str(NumberAppNeeded):
			print(
				f"{bcolors.INFO}Attempting to run {json_data['apps'][item]['file_name']}...{bcolors.END}")

			FileExtensionCheck = str(json_data['apps'][item]['file_name'])[-3:]
			if FileExtensionCheck != ".py":
				print(
					f"{bcolors.FAIL}Error:{bcolors.END} This is not a Python file, and thus can not be executed by PyPlace.")
				return

			elif exists(f"{json_data['apps'][item]['file_name']}") == True:
				os.system(f"{PyCommand} {json_data['apps'][item]['file_name']}")
				print(f"{bcolors.OKGREEN}File executed{bcolors.END}")
				input("Press [ENTER] to return to the home menu. ")

			else:
				print(
					f"{bcolors.FAIL}Error:{bcolors.END} {PyCommand} {json_data['apps'][item]['file_name']} does not exist in the current folder.")


def DownloadFile():
	print(f"""
[1] Link to Python file
[2] Download from PyPlace Store
[3] Download experiment
[{bcolors.FAIL}c{bcolors.END}] Cancel
""")
	NotAnswered4 = True
	while NotAnswered4 == True:
		Answer4 = input("How do you want to add a PyPlace app? ")
		if Answer4 == "c":
			return
		if str(Answer4) == "1":
			NotAnswered4 = False
			URLToPythonFile = input("Please enter the direct URL to a Python file: ")
			log("Testing URL with RegEx...")
			RegExResult = re.search(
"^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?$", 
URLToPythonFile)
			if RegExResult:
				log("The input is a URL, testing for Python file extension...")
				FileExtensionCheck2 = URLToPythonFile[-3:]
				if FileExtensionCheck2 != ".py":
					print(f"{bcolors.FAIL}Error:{bcolors.END} This is not a Python file, and thus can not be downloaded by PyPlace.")
					return
				else:
					print(f"{bcolors.INFO}Downloading Python app...{bcolors.END}")
					log(f"Retrieving file from {URLToPythonFile}")
					r = requests.get(URLToPythonFile, allow_redirects=False)
					if not r.ok:
						print(f"{bcolors.FAIL}Error:{bcolors.END} Could not download the Python file! Status code: {r.status_code}")
						return

					print(f"{bcolors.OKGREEN}Python app downloaded!{bcolors.END}")
					InvalidAnswer = True
					while InvalidAnswer == True:
						FileName = input("What do you want to call the file? ") or "PyPlace Installed App.py"
						FileExtensionCheck3 = FileName[-3:]
						if FileExtensionCheck3 != ".py":
							FileName = f"{FileName}.py"

						FileName = FileName.replace(" ", "-")
						RegExResult2 = re.search("""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", FileName)
						if RegExResult2:
							FileName = re.sub("""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", "-", FileName)
							print(f"{bcolors.WARNING}Warning:{bcolors.END} File name contained illegal characters. The file name is now {FileName}")
							InvalidAnswer = False
						else:
							InvalidAnswer = False

						if exists(FileName):
							print(f"{bcolors.FAIL}Error:{bcolors.END} A file with that name ({FileName}) already exists!")
							InvalidAnswer = True
						
					Name = input("What do you want to call the app? ") or "PyPlace Installed App"


					print(f"{bcolors.INFO}Installing Python app...{bcolors.END}")


					open(FileName, 'wb').write(r.content)

					with open('applications.json') as ApplicationsFile:
						data2 = json.load(ApplicationsFile)
					
					data2["apps"].update(
					{
						f"{Name}": {
							"name": f"{Name}",
							"file_name": f"{FileName}",
						}
					})

					log("Appending to applications.json")
					with open("applications.json", 'w') as json_file:
						json.dump(data2, json_file, 
											indent=4,  
											separators=(',',': '))
					
					print(f"{bcolors.OKGREEN}Python app installed!{bcolors.END}")
					print("It can now be opened via the \"Open a PyPlace app\" feature on the homepage!")
					NotAnswered4 = False
			else:
				print(f"{bcolors.FAIL}Error:{bcolors.END} That does not appear to be a valid URL!")
		elif Answer4 == "2":
			StoreRequest = requests.get("https://cdn.dantenl.tk/pyplace/store.json", allow_redirects=False)
			if not StoreRequest.ok:
				print(f"{bcolors.FAIL}Error:{bcolors.END} Could not connect to the PyPlace store! Response code: {StoreRequest.status_code}")
				return
			StoreRequestText = StoreRequest.text
			StoreRequestJSON = json.loads(StoreRequestText)

			ItemCount = 0
			for item in StoreRequestJSON["apps"]:
				ItemCount += 1
				Author = StoreRequestJSON['apps'][item]['author']
				print(f"[{ItemCount}] {StoreRequestJSON['apps'][item]['name']} by {Author}")
			print(f"[{bcolors.FAIL}c{bcolors.END}] Cancel")
			print(f"[{bcolors.INFO}i{bcolors.END}] Interested in putting your project on the store? Enter 'i' for info")

			
			NumberStoreAppNeeded = input("What number app do you want to download? ")
			
			if NumberStoreAppNeeded.lower() == "c":
				return
			
			if NumberStoreAppNeeded.lower() == "i":
				print(f"{bcolors.BOLD}{bcolors.INFO}We're currently looking for apps on the store!{bcolors.END}")
				print("If you have a Python app you would like to put on the store,")
				print("please message dante_nl#1234 on Discord (you might have to")
				print("friend me first in order to message me) if you are interested!")
				input("Enter any text to continue: ")

			ItemCount = 0
			for item in StoreRequestJSON["apps"]:
				ItemCount += 1
				if str(ItemCount) == str(NumberStoreAppNeeded):
					Author = StoreRequestJSON['apps'][item]['author']
					print(f"{bcolors.INFO}Attempting to download {StoreRequestJSON['apps'][item]['name']}...{bcolors.END}")
					log(f"Retrieving file from {StoreRequestJSON['apps'][item]['url']}...")

					AppRequest = requests.get(StoreRequestJSON['apps'][item]['url'], allow_redirects=False)
					if not AppRequest.ok:
						print(f"{bcolors.FAIL}Error:{bcolors.END} Could not connect to the file! Response code: {AppRequest.status_code}")
						return
					print(f"{bcolors.OKGREEN}Downloaded file!{bcolors.END}")

					InvalidAnswer1 = True
					while InvalidAnswer1 == True:
						FileName1 = input(
							"What do you want to call the file? ") or "PyPlace Installed Store App.py"
						FileExtensionCheck4 = FileName1[-3:]
						if FileExtensionCheck4 != ".py":
							FileName1 = f"{FileName1}.py"

						FileName1 = FileName1.replace(" ", "-")
						RegExResult3 = re.search(
							"""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", FileName1)
						if RegExResult3:
							FileName1 = re.sub(
								"""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", "-", FileName1)
							print(
								f"{bcolors.WARNING}Warning:{bcolors.END} File name contained illegal characters. The file name is now {FileName1}")
							InvalidAnswer1 = False
						else:
							InvalidAnswer1 = False

						if exists(FileName1):
							print(
								f"{bcolors.FAIL}Error:{bcolors.END} A file with that name ({FileName1}) already exists!")
							InvalidAnswer1 = True

					Name = StoreRequestJSON["apps"][item]["name"]

					print(f"{bcolors.INFO}Installing Python app...{bcolors.END}")

					open(FileName1, 'wb').write(AppRequest.content)

					with open('applications.json') as ApplicationsFile1:
						data3 = json.load(ApplicationsFile1)

					data3["apps"].update(
						{
							f"{Name}": {
								"name": f"{Name}",
								"file_name": f"{FileName1}",
								"author": f"{Author}",
								"StoreApp": "true"
							}
						})
					log("Appending to applications.json")
					with open("applications.json", 'w') as json_file:
						json.dump(data3, json_file,
								indent=4,
								separators=(',', ': '))
					print(f"{bcolors.OKGREEN}Python app installed!{bcolors.END}")
					NotAnswered4 = False
		elif Answer4 == "3":

			ExperimentRequest = requests.get(
				"https://cdn.dantenl.tk/pyplace/experiments.json", allow_redirects=True)
			if not ExperimentRequest.ok:
				print(f"{bcolors.FAIL}Error:{bcolors.END} Could not connect to the PyPlace Experiment Store! Response code: {ExperimentRequest.status_code}")
				return
			ExperimentRequestText = ExperimentRequest.text
			ExperimentRequestJSON = json.loads(ExperimentRequestText)

			ItemCount = 0
			for item in ExperimentRequestJSON["apps"]:
				ItemCount += 1
				print(f"[{ItemCount}] {ExperimentRequestJSON['apps'][item]['name']}")

			print(f"[{bcolors.FAIL}c{bcolors.END}] Cancel")

			NumberExperimentNeeded = input("What number app do you want to download? ")

			if NumberExperimentNeeded.lower() == "c":
				return

			ItemCount = 0
			for item in ExperimentRequestJSON["apps"]:
				ItemCount += 1
				if str(ItemCount) == str(NumberExperimentNeeded):
					print(f"{bcolors.INFO}Attempting to download {ExperimentRequestJSON['apps'][item]['name']}...{bcolors.END}")
					log(f"Retrieving file from {ExperimentRequestJSON['apps'][item]['url']}...")

					AppRequest = requests.get(ExperimentRequestJSON['apps'][item]['url'], allow_redirects=False)
					if not AppRequest.ok:
						print(f"{bcolors.FAIL}Error:{bcolors.END} Could not connect to the file! Response code: {AppRequest.status_code}")
						return
					print(f"{bcolors.OKGREEN}Downloaded file!{bcolors.END}")

					InvalidAnswer1 = True
					while InvalidAnswer1 == True:
						FileName1 = input("What do you want to call the file? ") or "PyPlace Installed Experiment.py"
						FileExtensionCheck4 = FileName1[-3:]
						if FileExtensionCheck4 != ".py":
							FileName1 = f"{FileName1}.py"

						FileName1 = FileName1.replace(" ", "-")
						RegExResult3 = re.search(
							"""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", FileName1)
						if RegExResult3:
							FileName1 = re.sub(
								"""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", "-", FileName1)
							print(
								f"{bcolors.WARNING}Warning:{bcolors.END} File name contained illegal characters. The file name is now {FileName1}")
							InvalidAnswer1 = False
						else:
							InvalidAnswer1 = False

						if exists(FileName1):
							print(
								f"{bcolors.FAIL}Error:{bcolors.END} A file with that name ({FileName1}) already exists!")
							InvalidAnswer1 = True

					Name = ExperimentRequestJSON["apps"][item]["name"]

					print(f"{bcolors.INFO}Installing experiment app...{bcolors.END}")

					open(FileName1, 'wb').write(AppRequest.content)

					with open('applications.json') as ApplicationsFile1:
						data3 = json.load(ApplicationsFile1)

					data3["apps"].update(
						{
							f"Experiment: {Name}": {
								"name": f"{Name}",
								"file_name": f"{FileName1}",
								"experiment": "true"
							}
						})
					log("Appending to applications.json")
					with open("applications.json", 'w') as json_file:
						json.dump(data3, json_file,
								indent=4,
								separators=(',', ': '))
					print(f"{bcolors.OKGREEN}Experiment installed!{bcolors.END}")
					NotAnswered4 = False

def Settings():
	print("What do you want to do?")
	print(f"""
[1] Delete an application
[2] Change Python command 
[3] Restore to latest version
[4] About
[{bcolors.FAIL}c{bcolors.END}] Back to main menu
""")
	NotAnswered = True
	while NotAnswered == True:
		Answer = input("Enter the number or letter for what you want to do: ")
		if Answer == "1":
			if exists("applications.json") == False:
				print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
				return

			with open('applications.json') as AppsFile:
				json_data = json.load(AppsFile)

			if "apps" in json_data == False:
				print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
				return

			log("Reading applications.json...")
			print(f"{bcolors.WARNING}■{bcolors.END}: Experimental application")
			print(f"{bcolors.OKCYAN}■{bcolors.END}: Application downloaded from the PyPlace store")

			ItemCount = 0
			for item in json_data["apps"]:
				ItemCount += 1
				if "StoreApp" in json_data['apps'][item]:
					if "StoreApp" in json_data['apps'][item]:
						if json_data['apps'][item]["StoreApp"] == "true":
							print(f"{bcolors.OKCYAN}[{ItemCount}] {json_data['apps'][item]['name']} by {json_data['apps'][item]['author']}{bcolors.END}")
				elif "experiment" in json_data['apps'][item]:
					if json_data['apps'][item]["experiment"] == "true":
						print(f"{bcolors.WARNING}[{ItemCount}] {json_data['apps'][item]['name']}{bcolors.END}")
				else:
					if "author" in json_data['apps'][item]:
						print(f"[{ItemCount}] {json_data['apps'][item]['name']} by {json_data['apps'][item]['author']}")
					else:
						print(f"[{ItemCount}] {json_data['apps'][item]['name']}")
			
			print(f"[{bcolors.INFO}i{bcolors.END}] Looking to delete multiple apps at once? Enter \"i\"")
	
			if ItemCount == 0:
				print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
				return

			print(f"[{bcolors.FAIL}c{bcolors.END}] Cancel")
			NumberAppNeeded = input("What number app do you want to delete? ")
			if NumberAppNeeded.lower() == "c":
				NotAnswered = False
				return
			elif NumberAppNeeded.lower() == "i":
				print(f"""{bcolors.INFO}{bcolors.BOLD}Looking to delete multiple apps at once?{bcolors.END}

You can download \"PyPlace - Bulk Delete\" fron the PyPlace Experiment Store right now.
Just enter \"2\" at the home screen (for \"Download a PyPlace app\"), and then enter \"3\"
to open the PyPlace Expirements Store!

{bcolors.WARNING}NOTE:{bcolors.END} This is currently in beta, and things might not work properly.
""")
				input("Press [ENTER] to return to the home menu. ")
				NotAnswered = False
				return
			ItemCount = 0
			for item in json_data["apps"]:
				ItemCount += 1
				if str(ItemCount) == str(NumberAppNeeded):
					ItemNeeded = item
					AppName = json_data["apps"][item]["name"]

			if exists(json_data["apps"][ItemNeeded]["file_name"]):
				os.remove(json_data["apps"][ItemNeeded]["file_name"])
				log(f"Deleted {json_data['apps'][ItemNeeded]['file_name']}")
			del json_data["apps"][ItemNeeded]

			with open('applications.json', 'w') as data_file:
				data = json.dump(json_data, data_file,
								indent=4,
								separators=(',', ': '))
			print(f"{bcolors.OKGREEN}Deleted {AppName}!{bcolors.END}")
			NotAnswered = False

		elif Answer == "2":
			if ReplitMode != True:
				if exists("setup.json") == False:
					print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have a setup.json file! Please {bcolors.BOLD}restart PyPlace to set it up!{bcolors.END}")
					sys.exit(0)

				NewPythonCommand = input("What do you want the new command to be? Leave empty to set to default (python3). ") or "python3"

				SetupFile = open("setup.json", "r")
				json_object = json.load(SetupFile)
				SetupFile.close()
				log(json_object)

				json_object["PythonCommand"] = NewPythonCommand
				SetupFile = open("setup.json", "w")
				json.dump(json_object, SetupFile)
				SetupFile.close()

				print(f"{bcolors.OKGREEN}Command updated to {NewPythonCommand}!{bcolors.END}")
				NotAnswered = False
			else:
				print(f"{bcolors.FAIL}Error:{bcolors.END} This is not available when PyPlace is executed on Replit. {bcolors.BOLD}You can download PyPlace instead{bcolors.END}")

		elif Answer == "3":
			if ReplitMode != True:
				NotAnswered1 = True
				while NotAnswered1 == True:
					Answer1 = input("Are you sure you want to restore to the latest version published online? (y/n) ")
					if Answer1 == "y":
						NotAnswered1 = False
						print(f"{bcolors.INFO}Downloading latest version of PyPlace...{bcolors.END}")
						log("Retrieving latest version of PyPlace...")
						r = requests.get(
							"https://cdn.dantenl.tk/PyPlace/PyPlace-Latest.py", allow_redirects=True)
						if not r.ok:
							print(
								f"{bcolors.FAIL}Error:{bcolors.END} Could not get the PyPlace file! Status code: {r.status_code}")
							return
						log("Updating main PyPlace file")
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
								print(f"Continuing with current version. {bcolors.BOLD}NOTE:{bcolors.END} Next time you start PyPlace.py, it will be on the latest version!")
								NotAnswered2 = False
								return
							else:
								print(
									f"{bcolors.FAIL}Error:{bcolors.END} I'm not sure what you mean with \"{Answer2}\".")
					elif Answer1 == "n":
						NotAnswered1 = False
						NotAnswered = False
			else:
				print(f"{bcolors.FAIL}Error:{bcolors.END} This is not available when PyPlace is executed on Replit. {bcolors.BOLD}You can download PyPlace instead{bcolors.END}")

		elif Answer == "4":
			NotAnswered = False
			with open('setup.json') as SetupFile:
				data = json.load(SetupFile)

			print(f"""
██████╗░██╗░░░██╗██████╗░██╗░░░░░░█████╗░░█████╗░███████╗
██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔════╝
██████╔╝░╚████╔╝░██████╔╝██║░░░░░███████║██║░░╚═╝█████╗░░
██╔═══╝░░░╚██╔╝░░██╔═══╝░██║░░░░░██╔══██║██║░░██╗██╔══╝░░
██║░░░░░░░░██║░░░██║░░░░░███████╗██║░░██║╚█████╔╝███████╗
╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝

PyPlace is an easy-to-use Python
application that allows you to open and install
various Python applications. PyPlace is designed to
be as easy to use, so everyone can use it! :D

{bcolors.BOLD}Your version:{bcolors.END} {Version}
{bcolors.BOLD}Your setup version:{bcolors.END} {data["SetupVersion"]}""")
			input("Press [ENTER] to return to the home menu. ")
		elif Answer == "c":
			NotAnswered = False
			return
		else:
			print(f"{bcolors.FAIL}Error:{bcolors.END} I'm not sure what you mean with \"{Answer}\".")


				

def PyPlaceRegular():
	log("Reading application file...")
	print("What do you want to do?")
	print(f"""
[1] Open a PyPlace app
[2] Download a PyPlace app
[3] Open settings
[{bcolors.FAIL}e{bcolors.END}] Exit PyPlace
""")
	NotAnswered3 = True
	while NotAnswered3 == True:
		Answer3 = input("Enter the number or letter for what you want to do: ")
		if str(Answer3) == "1":
			NotAnswered3 = False
			ExecuteFile()
			return
		elif str(Answer3) == "2":
			NotAnswered3 = False
			DownloadFile()
			return
		elif str(Answer3) == "3":
			NotAnswered3 = False
			Settings()
			return
		elif str(Answer3) == "e":
			NotAnswered3 = False
			sys.exit(0)
		else:
			print(
				f"{bcolors.FAIL}Error:{bcolors.END} I'm not sure what you mean with \"{Answer3}\".")


print("————————————————————————————")
print(f"Welcome to {bcolors.BOLD}PyPlace{bcolors.END}!")
print()
print("PyPlace is a Python application that allows you to")
print("to get a simple overview of your other Python")
print("applications, and it also allows you to easily")
print("install new ones!")
print()
if ReplitMode == True:
	print(f"{bcolors.WARNING}WARNING:{bcolors.END} It appears you're running this on the Replit page. Not everything might work properly because of different file names! We recommend downloading PyPlace and running it for yourself.")
if FileNameWarning == True:
	print(f"""{bcolors.WARNING}WARNING:{bcolors.END} It appears that you are running this from another file that is not called \"pyplace.py\".
This means you can not correctly restore and update PyPlace. We recommend changin it to \"pyplace.py\".""")

log("Checking if setup.json exists...")
if exists("setup.json") == True:
	log("setup.json exists, launching the regular version of PyPlace...")
	log("Checking if applications.json exists...")
	if exists("applications.json") == False:
		log("applications.json does not exist, creating new file...")
		AppDict = {
			"_NOTE": "DO NOT DELETE THIS FILE! This file is crucial for downloading, opening and deleting apps, yet you deleted it :(",
			"apps": {
			}
		}

		with open("applications.json", 'w') as json_file:
			json.dump(AppDict, json_file,
				indent=4,
				separators=(',', ': '))
		log("applications.json created.")
	if CheckForUpdates != False:
		UpdateCheck()
	while DoINeedToRun == True:
		PyPlaceRegular()
else:
	log("setup.json does not exist, launching setup...")
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
		"SetupVersion": 0.1,
		"PythonCommand": f"{PythonCommand}"
	}

	SetupDictStr = json.dumps(SetupDict, indent=4, separators=(',', ': '))
	with open('setup.json', 'w') as SetupJSON:
		SetupJSON.write(SetupDictStr)
		log("File created: setup.json")

	print(f"{bcolors.OKGREEN}PyPlace is set up!{bcolors.END}")
	# Read content of setup.json key
	# with open('setup.json') as SetupFile:
	#     data = json.load(SetupFile)
	#     print(data["SetupVersion"])
