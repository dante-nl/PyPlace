
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

# Remastered version of the first PyPlace version that is somewhat recognisable and fully functional.
# Slightly updated, to make sure that main PyPlace files remain unaffected.

# ————————————————————————————
# Below you can change more advanced settings,
# that are hard-coded in to PyPlace.
# We only recommend changing these settings
# when you know what you are doing.

# 𝗘𝗻𝗮𝗯𝗹𝗲 𝗼𝗿 𝗱𝗶𝘀𝗮𝗯𝗹𝗲 𝗰𝗵𝗲𝗰𝗸𝗶𝗻𝗴 𝗳𝗼𝗿 𝘂𝗽𝗱𝗮𝘁𝗲𝘀
# Default: False
# Possible options: True, False

# Do you want to check for updates when the
# program is ran? You can always check for
# updates via the advanced options.
# Disabled because you don't want to go to version 0.6, right?

CheckForUpdates = False

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
DoINeedToRun = True

# 𝗖𝘂𝗿𝗿𝗲𝗻𝘁 𝘃𝗲𝗿𝘀𝗶𝗼𝗻
# Default: 0.2 (changes every version)
# Possible options: any number

# This is the version of PyPlace and is
# absolutely not recommended to change,
# except for testing purposes.
Version = 0.22


# ————————————————————————————
# Below this line of text, everything
# that is needed in PyPlace is imported.
# It is absolutely NOT recommended to
# edit this as it can BREAK PyPlace!
from os.path import exists
import requests
import json
import sys
import re
import os

# ————————————————————————————
# Below is the main code, it is not
# recommended to edit it, as it might affect
# how well PyPlace runs.

# ! This was added during revamp
REQUEST_HEADERS = {
	"Cache-Control": "no-cache",
	"Expires": "0"
}

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


# For the Replit version:
# print(f"{bcolors.WARNING}Warning:{bcolors.END} It appears you're running this on the Replit page. Not everything might work properly because of different file names! We recommend downloading PyPlace and running it for yourself.")

if exists("setup-0.2.json") == True:
	with open('setup-0.2.json') as SetupFile:
		_data = json.load(SetupFile)
		PyCommand = _data["PythonCommand"]


def log(message):
	if DoNotLogOutput == False:
		print(f"{bcolors.LOG}Log:{bcolors.END} {message}")


def UpdateCheck():
	log("Checking for latest version...")
	response = requests.get("https://cdn.dantenl.com/PyPlace/version.json", allow_redirects=True, headers=REQUEST_HEADERS)
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
					"https://cdn.dantenl.com/PyPlace/PyPlace-Latest.py", allow_redirects=True, headers=REQUEST_HEADERS)
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
	if exists("applications-0.2.json") == False:
		print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
		return

	with open('applications-0.2.json') as AppsFile:
		json_data = json.load(AppsFile)

	if "apps" in json_data == False:
		print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
		return

	print(
		f"Applications colored {bcolors.OKCYAN}cyan{bcolors.END} are downloaded from the PyPlace Store.")
	ItemCount = 0
	for item in json_data["apps"]:
		ItemCount += 1
		if "StoreApp" in json_data['apps'][item]:
			if json_data['apps'][item]["StoreApp"] == "true":
				print(
					f"{bcolors.OKCYAN}[{ItemCount}] {json_data['apps'][item]['name']} by {json_data['apps'][item]['author']}{bcolors.END}")
		else:
			print(f"[{ItemCount}] {json_data['apps'][item]['name']}")

	if ItemCount == 0:
		print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
		return

	NumberAppNeeded = input("What number app do you want to open? ")
	ItemCount = 0
	for item in json_data["apps"]:
		ItemCount += 1
		if str(ItemCount) == str(NumberAppNeeded):
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
				input("Input any text to continue to the home page: ")

			else:
				print(
					f"{bcolors.FAIL}Error:{bcolors.END} {PyCommand} {json_data['apps'][item]['file_name']} does not exist in the current folder.")


def DownloadFile():
	print(f"""
[1] Link to Python file
[2] Download from PyPlace Store
[{bcolors.FAIL}c{bcolors.END}] Cancel
""")
	NotAnswered4 = True
	while NotAnswered4 == True:
		Answer4 = input("How do you want to add a PyPlace app? ")
		if Answer4 == "c":
			return
		if str(Answer4) == "1":
			NotAnswered4 = False
			URLToPythonFile = input(
				"Please enter the direct URL to a Python file: ")
			log("Testing URL with RegEx...")
			RegExResult = re.search(
				r"^(?:(?:https?|ftp):\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]-*)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,}))\.?)(?::\d{2,5})?(?:[/?#]\S*)?$", URLToPythonFile)
			if RegExResult:
				log("The input is a URL, testing for Python file extension...")
				FileExtensionCheck2 = URLToPythonFile[-3:]
				if FileExtensionCheck2 != ".py":
					print(
						f"{bcolors.FAIL}Error:{bcolors.END} This is not a Python file, and thus can not be downloaded by PyPlace.")
					return
				else:
					print(f"{bcolors.INFO}Downloading Python app...{bcolors.END}")
					log(f"Retrieving file from {URLToPythonFile}")
					r = requests.get(URLToPythonFile, allow_redirects=True,
					                 headers=REQUEST_HEADERS)
					if not r.ok:
						print(
							f"{bcolors.FAIL}Error:{bcolors.END} Could not download the Python file! Status code: {r.status_code}")
						return

					print(f"{bcolors.OKGREEN}Python app downloaded!{bcolors.END}")
					InvalidAnswer = True
					while InvalidAnswer == True:
						FileName = input(
							"What do you want to call the file? ") or "PyPlace Installed App.py"
						FileExtensionCheck3 = FileName[-3:]
						if FileExtensionCheck3 != ".py":
							FileName = f"{FileName}.py"

						FileName = FileName.replace(" ", "-")
						RegExResult2 = re.search(
							r"""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", FileName)
						if RegExResult2:
							FileName = re.sub(
								r"""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", "-", FileName)
							print(
								f"{bcolors.WARNING}Warning:{bcolors.END} File name contained illegal characters. The file name is now {FileName}")
							InvalidAnswer = False
						else:
							InvalidAnswer = False

						if exists(FileName):
							print(
								f"{bcolors.FAIL}Error:{bcolors.END} A file with that name ({FileName}) already exists!")
							InvalidAnswer = True

					Name = input(
						"What do you want to call the app? ") or "PyPlace Installed App"

					print(f"{bcolors.INFO}Installing Python app...{bcolors.END}")

					open(FileName, 'wb').write(r.content)

					with open('applications-0.2.json') as ApplicationsFile:
						data2 = json.load(ApplicationsFile)

					data2["apps"].update(
						{
							f"{Name}": {
								"name": f"{Name}",
								"file_name": f"{FileName}",
							}
						})

					log("Appending to applications-0.2.json")
					with open("applications-0.2.json", 'w') as json_file:
						json.dump(data2, json_file,
								indent=4,
								separators=(',', ': '))

					print(f"{bcolors.OKGREEN}Python app installed!{bcolors.END}")
					print(
						"It can now be opened via the \"Open a PyPlace app\" feature on the homepage!")
					NotAnswered4 = False
			else:
				print(
					f"{bcolors.FAIL}Error:{bcolors.END} That does not appear to be a valid URL!")
		elif Answer4 == "2":
			StoreRequest = requests.get(
				"https://cdn.dantenl.com/pyplace/store.json", allow_redirects=True, headers=REQUEST_HEADERS)
			if not StoreRequest.ok:
				print(
					f"{bcolors.FAIL}Error:{bcolors.END} Could not connect to the PyPlace store! Response code: {StoreRequest.status_code}")
				return
			StoreRequestText = StoreRequest.text
			StoreRequestJSON = json.loads(StoreRequestText)

			ItemCount = 0
			for item in StoreRequestJSON["apps"]:
				ItemCount += 1
				Author = StoreRequestJSON['apps'][item]['author']
				print(
					f"[{ItemCount}] {StoreRequestJSON['apps'][item]['name']} by {Author}")
			print(f"[{bcolors.FAIL}c{bcolors.END}] Cancel")
			print(
				f"[{bcolors.INFO}i{bcolors.END}] Interested in putting your project on the store? Enter 'i' for info")

			NumberStoreAppNeeded = input(
				"What number app do you want to download? ")

			if NumberStoreAppNeeded.lower() == "c":
				return

			if NumberStoreAppNeeded.lower() == "i":
				print(
					f"{bcolors.BOLD}{bcolors.INFO}We're currently looking for apps on the store!{bcolors.END}")
				print("If you have a Python app you would like to put on the store,")
				print(
					"please message dante_nl#1234 on Discord (you might have to")
				print("friend me first in order to message me) if you are interested!")
				input("Enter any text to continue: ")

			ItemCount = 0
			for item in StoreRequestJSON["apps"]:
				ItemCount += 1
				if str(ItemCount) == str(NumberStoreAppNeeded):
					Author = StoreRequestJSON['apps'][item]['author']
					print(
						f"{bcolors.INFO}Attempting to download {StoreRequestJSON['apps'][item]['name']}...{bcolors.END}")
					log(
						f"Retrieving file from {StoreRequestJSON['apps'][item]['url']}...")

					AppRequest = requests.get(
						StoreRequestJSON['apps'][item]['url'], allow_redirects=True, headers=REQUEST_HEADERS)
					if not AppRequest.ok:
						print(
							f"{bcolors.FAIL}Error:{bcolors.END} Could not connect to the PyPlace store! Response code: {AppRequest.status_code}")
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
							r"""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", FileName1)
						if RegExResult3:
							FileName1 = re.sub(
								r"""\`|\~|\!|\@|\#|\$|\%|\^|\&|\*|\(|\)|\+|\=|\[|\{|\]|\}|\||\\|\'|\<|\,|\>|\?|\/|\""|\;|\:|\s""", "-", FileName1)
							print(
								f"{bcolors.WARNING}Warning:{bcolors.END} File name contained illegal characters. The file name is now {FileName1}")
							InvalidAnswer1 = False
						else:
							InvalidAnswer1 = False

						if exists(FileName1):
							print(
								f"{bcolors.FAIL}Error:{bcolors.END} A file with that name ({FileName1}) already exists!")
							InvalidAnswer1 = True

					Name = input(
						"What do you want to call the app? ") or "PyPlace Installed Store App"

					print(f"{bcolors.INFO}Installing Python app...{bcolors.END}")

					open(FileName1, 'wb').write(AppRequest.content)

					with open('applications-0.2.json') as ApplicationsFile1:
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
					log("Appending to applications-0.2.json")
					with open("applications-0.2.json", 'w') as json_file:
						json.dump(data3, json_file,
								indent=4,
								separators=(',', ': '))
					print(f"{bcolors.OKGREEN}Python app installed!{bcolors.END}")
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
			if exists("applications-0.2.json") == False:
				print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
				return

			with open('applications-0.2.json') as AppsFile:
				json_data = json.load(AppsFile)

			if "apps" in json_data == False:
				print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
				return

			log("Reading applications-0.2.json...")
			print(
				f"Applications colored {bcolors.OKCYAN}cyan{bcolors.END} are downloaded from the PyPlace Store.")
			ItemCount = 0
			for item in json_data["apps"]:
				ItemCount += 1
				if "StoreApp" in json_data['apps'][item]:
					if json_data['apps'][item]["StoreApp"] == "true":
						print(
							f"{bcolors.OKCYAN}[{ItemCount}] {json_data['apps'][item]['name']} by {json_data['apps'][item]['author']}{bcolors.END}")
				else:
					print(f"[{ItemCount}] {json_data['apps'][item]['name']}")

			if ItemCount == 0:
				print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.")
				return

			print(f"[{bcolors.FAIL}c{bcolors.END}] Cancel")
			NumberAppNeeded = input("What number app do you want to delete? ")
			if NumberAppNeeded.lower() == "c":
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

			with open('applications-0.2.json', 'w') as data_file:
				data = json.dump(json_data, data_file,
								indent=4,
								separators=(',', ': '))
			print(f"{bcolors.OKGREEN}Deleted {AppName}!{bcolors.END}")
			NotAnswered = False
		elif Answer == "2":
			if exists("setup-0.2.json") == False:
				print(f"{bcolors.FAIL}Error:{bcolors.END} You do not have a setup-0.2.json file! Please {bcolors.BOLD}restart PyPlace to set it up!{bcolors.END}")
				sys.exit(0)

			NewPythonCommand = input(
				"What do you want the new command to be? Leave empty to set to default (python3). ") or "python3"

			SetupFile = open("setup-0.2.json", "r")
			json_object = json.load(SetupFile)
			SetupFile.close()
			log(json_object)

			json_object["PythonCommand"] = NewPythonCommand
			SetupFile = open("setup-0.2.json", "w")
			json.dump(json_object, SetupFile)
			SetupFile.close()

			print(
				f"{bcolors.OKGREEN}Command updated to {NewPythonCommand}!{bcolors.END}")
			NotAnswered = False

		elif Answer == "3":
			NotAnswered1 = True
			while NotAnswered1 == True:
				Answer1 = input(
					"Are you sure you want to restore to the latest version published online? (y/n) ")
				if Answer1 == "y":
					NotAnswered1 = False
					print(
						f"{bcolors.INFO}Downloading latest version of PyPlace...{bcolors.END}")
					log("Retrieving latest version of PyPlace...")
					r = requests.get(
						"https://cdn.dantenl.com/PyPlace/PyPlace-Latest.py", allow_redirects=True, headers=REQUEST_HEADERS)
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
							print(
								f"Continuing with current version. {bcolors.BOLD}NOTE:{bcolors.END} Next time you start PyPlace.py, it will be on the latest version!")
							NotAnswered2 = False
							return
						else:
							print(
								f"{bcolors.FAIL}Error:{bcolors.END} I'm not sure what you mean with \"{Answer2}\".")
				elif Answer1 == "n":
					NotAnswered1 = False
					NotAnswered = False

		elif Answer == "4":
			# ! Coding here now! (about)
			NotAnswered = False
			with open('setup-0.2.json') as SetupFile:
				data = json.load(SetupFile)

			print(f"""
██████╗░██╗░░░██╗██████╗░██╗░░░░░░█████╗░░█████╗░███████╗
██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔════╝
██████╔╝░╚████╔╝░██████╔╝██║░░░░░███████║██║░░╚═╝█████╗░░
██╔═══╝░░░╚██╔╝░░██╔═══╝░██║░░░░░██╔══██║██║░░██╗██╔══╝░░
██║░░░░░░░░██║░░░██║░░░░░███████╗██║░░██║╚█████╔╝███████╗
╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝

Release notes v0.2.2:
* All files are now seperate from the main version of PyPlace
* Fixed invalid escape sequences in RegEx (this error popped up because a newer version of Python)
		 
PyPlace is an easy-to-use Python
application that allows you to open and install
various Python applications. PyPlace is designed to
be as easy to use, so everyone can use it! :D
	 
You are currently using a remastered version of PyPlace 0.2.
Why this version? This was the first ever version to fully
be fully functiunal and actually recognisable as 0.1 only
had the option to open apps, nothing more. 
After version 0.6, PyPlace was switched over to a new domain
(from cdn.dantenl.tk/pyplace to pyplace.dantenl.tk (now 
pyplace.dantenl.com)) so the original older versions don't work.
In this update it was switched from cdn.dantenl.tk to cdn.dantenl.com
as the old files still exist. So you can actually browse the old store
as it was back in version 0.6. If you manually enable the updater you
can also see that it thinks the latest version is 0.6.

Enjoy! 
-dante_nl, creator of PyPlace.

{bcolors.BOLD}Your version:{bcolors.END} {Version} (remastered)
{bcolors.BOLD}Your setup version:{bcolors.END} {data["SetupVersion"]}""")
			input("Input any text to continue to the home page: ")
		elif Answer == "c":
			NotAnswered = False
			return
		else:
			print(
				f"{bcolors.FAIL}Error:{bcolors.END} I'm not sure what you mean with \"{Answer}\".")


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
print("Welcome to the remastered version! Go to [3] Settings > [4] About to learn more.")
print()

log("Checking if setup-0.2.json exists...")
if exists("setup-0.2.json") == True:
	log("setup-0.2.json exists, launching the regular version of PyPlace...")
	log("Checking if applications-0.2.json exists...")
	if exists("applications-0.2.json") == False:
		log("applications-0.2.json does not exist, creating new file...")
		AppDict = {
			"_NOTE": "DO NOT DELETE THIS FILE! This file is crucial for downloading, opening and deleting apps, yet you deleted it :(",
			"apps": {
			}
		}

		with open("applications-0.2.json", 'w') as json_file:
			json.dump(AppDict, json_file,
					indent=4,
					separators=(',', ': '))
		log("applications-0.2.json created.")
	if CheckForUpdates != False:
		UpdateCheck()
	while DoINeedToRun == True:
		PyPlaceRegular()
else:
	log("setup-0.2.json does not exist, launching setup...")
	PythonCommand = input(
		"What command do you use to run a Python file in your terminal? ") or "python3"
	print("Leave empty to set it to the default (python3)")
	print(f"{bcolors.BOLD}NOTE: {bcolors.END}You can change this later in the settings.")

	print(f"{bcolors.INFO}Setting up PyPlace...{bcolors.END}")

	AppDict = {
		"_NOTE": "DO NOT DELETE THIS FILE! This file is crucial for downloading, opening and deleting apps!",
		"apps": {
		}
	}

	with open("applications-0.2.json", 'w') as json_file:
		json.dump(AppDict, json_file,
				indent=4,
				separators=(',', ': '))

	SetupDict = {
		"_comment1": "PYPLACE SETUP FILE",
		"_comment2": "This is an important file for PyPlace, because your settings are stored here! It is NOT recommended to delete or edit this file.",
		"SetupVersion": 0.1,
		"PythonCommand": f"{PythonCommand}"
	}

	SetupDictStr = json.dumps(SetupDict)
	with open('setup-0.2.json', 'w') as SetupJSON:
		SetupJSON.write(SetupDictStr)
		log("File created: setup-0.2.json")

	print(f"{bcolors.OKGREEN}PyPlace is set up!{bcolors.END}")
	# Read content of setup-0.2.json key
	# with open('setup-0.2.json') as SetupFile:
	#     data = json.load(SetupFile)
	#     print(data["SetupVersion"])
