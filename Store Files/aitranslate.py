
# ██████╗░██╗░░░██╗██████╗░██╗░░░░░░█████╗░░█████╗░███████╗  ░█████╗░██╗
# ██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔════╝  ██╔══██╗██║
# ██████╔╝░╚████╔╝░██████╔╝██║░░░░░███████║██║░░╚═╝█████╗░░  ███████║██║
# ██╔═══╝░░░╚██╔╝░░██╔═══╝░██║░░░░░██╔══██║██║░░██╗██╔══╝░░  ██╔══██║██║
# ██║░░░░░░░░██║░░░██║░░░░░███████╗██║░░██║╚█████╔╝███████╗  ██║░░██║██║
# ╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝  ╚═╝░░╚═╝╚═╝

# ████████╗██████╗░░█████╗░███╗░░██╗░██████╗██╗░░░░░░█████╗░████████╗██╗░█████╗░███╗░░██╗░██████╗
# ╚══██╔══╝██╔══██╗██╔══██╗████╗░██║██╔════╝██║░░░░░██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔════╝
# ░░░██║░░░██████╔╝███████║██╔██╗██║╚█████╗░██║░░░░░███████║░░░██║░░░██║██║░░██║██╔██╗██║╚█████╗░
# ░░░██║░░░██╔══██╗██╔══██║██║╚████║░╚═══██╗██║░░░░░██╔══██║░░░██║░░░██║██║░░██║██║╚████║░╚═══██╗
# ░░░██║░░░██║░░██║██║░░██║██║░╚███║██████╔╝███████╗██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║██████╔╝
# ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░

# 🄱🅈 🄳🄰🄽🅃🄴_🄽🄻

# Welcome to PyPlace AI Translations! This allows you to translate PyPlace
# automatically in any language, real ones and once that are made up using
# ChatGPT. You will need to provide it with your own API key that you can
# get from https://platform.openai.com/account/api-keys

# This uses the PyPlace built in app updater, available from version 1.0
# and newer. Please check back after a PyPlace update if you want to 
# translate anything.

# ————————————————————————————
# Below are some extra options if you really want to change them.
# For most users, this is not recommended.

MODEL = "gpt-3.5-turbo"
# ^ The model. At this point in time, we recommend gpt-3.5-turbo
# as it's the cheapest.

API_URL = "https://api.openai.com/v1/chat/completions"
# ^ you shouldn't have to change this

SLEEP_TIME = 0.2
# ^ Time to wait in seconds. This is added so OpenAI won't
# block any requests.

API_KEY = None
# ^ If you want to save it. Note that with every update, this is reset.

SYSTEM_PROMPT = "You are a translator who translates any given sentence to a different language. You are translating a computer program. You translate to [language]. Do not translate or remove anything in square brackets."
# ^ The prompt ChatGPT should work with to translate your sentences.

TOKEN_LIMIT = 1000
# ^ The higher this number is, the longer the sentences ChatGPT can translate
# Lower means that the costs will be lower but it also means you
# might get sentences that randomly stop.

# ————————————————————————————
# Below is the main code. Changing anything may risk it to stop working.

import asyncio
import sys
import json
import time
import requests

class colors:
	LOG = '\033[95m'
	INFO = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	END = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

language = {
    "version": 1.0,

	"input_error": f"[r]Error:[\]] I'm not sure what you mean with that!",
	"back_to_menu": "Press [ENTER] to return to the main menu.",
	"cancel": "Cancel",

	"intro_1": f"Welcome to [b]PyPlace[\]]",
	"intro_2": "PyPlace is a Python application that allows you",
	"intro_3": "to get a simple overview of your other Python",
	"intro_4": "applications, and it also allows you to easily",
	"intro_5": "install new ones!",

	"replit_warning": f"[o]WARNING:[\]] It appears that you're running this on the Replit page. Not everything might work properly because of different file names! We recommend downloading PyPlace and running it for yourself.",
	"file_name_warning": f"[o]WARNING:[\] It appears that you are running this from another file that is not called \"pyplace.py\". \nThis means you can not correctly restore and update PyPlace. We recommend changing it to \"pyplace.py\".",

	"setup_1": "What command do you use to run a Python file in your terminal?",
	"setup_2": "Leave empty to set it to the default. (python3)",
	"setup_3": f"[b]NOTE: [\]You can change this later in the settings.",
	"setup_4": f"[i]Setting up PyPlace...[\]",
	"setup_5": f"[g]PyPlace is set up![\]",
	"setup_6": "Press [ENTER] to start PyPlace",

	"main_menu_option_1": "Open a PyPlace app",
	"main_menu_option_2": "Add a PyPlace app",
	"main_menu_option_3": "Open settings",
	"main_menu_option_4": "Exit PyPlace",
	"main_menu_option_5": "Check for app updates",
	"main_menu_message_1": "What do you want to do?",
	"main_menu_message_2": "Enter the number or letter for what you want to do:",

	"update_error_1": f"[r]Error:[\] Could not check for updates! Response code: [code]",
	"update_error_2": f"[r]Error:[\] Could not get the PyPlace file! Response code: [code]",
	"update_warning_1": f"[o]WARNING:[\] Your current version seems to be newer than the latest version that is released!",
	"update_message_1": f"[g]UPDATE AVAILABLE![\]",
	"update_message_2": f"Your current version ([version]) is no longer the latest version! The latest version is [version_latest].",
	"update_message_3": f"Here are the release notes:",
	"update_message_4": f"Would you like to update right now?",
	"update_message_5": f"[i]Downloading the latest version of PyPlace...[\]",
	"update_message_6": f"[g]The latest version of PyPlace is now ready in [g]PyPlace.py![\]",
	"update_message_7": f"Would you like to run it?",
	"update_message_8": f"[i]Attempting to run PyPlace.py...[\]",
	"update_message_9": f"Continuing with current version. [g]NOTE:[\] Next time you start PyPlace.py, it will be on the latest version!",

	"execute_file_error_1": f"[r]Error:[\] You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.",
	"execute_file_error_2": f"[r]Error:[\] This is not a Python file, and thus can not be executed by PyPlace.",
	"execute_file_message_1": f"[o][square][\]: Experimental application",
	"execute_file_message_2": f"[c][square][\]: Application downloaded from the PyPlace store",
	"execute_file_message_3": f"What number app do you want to open?",
	"execute_file_message_4": f"[i]Attempting to run [app]...[\]",
	"execute_file_message_5": f"[g]File executed[\]",

	"download_file_error_1": f"[r]Error:[\] This is not a Python file, and thus can not be downloaded by PyPlace",
	"download_file_error_2": f"[r]Error:[\] Could not download the Python file! Status code: [code]",
	"download_file_error_3": f"[r]Error:[\] A file with that name ([name]) aleady exists!",
	"download_file_error_4": f"That does not appear to be a valid URL!",
	"download_file_warning_1": f"[o]Warning:[\] File name contained illegal characters. The file name is now [name]",
	"download_file_option_1": f"Link to Python file",
	"download_file_option_2": f"Download from PyPlace Store",
	"download_file_option_3": f"Download experiment",
	"download_file_option_4": f"Add local file",
	"download_file_message_1": f"How do you want to add a PyPlace app?",
	"download_file_message_2": f"Please enter the direct URL to a Python file:",
	"download_file_message_3": f"[i]Downloading Python app...[\]",
	"download_file_message_4": f"[g]Python app downloaded![\]",
	"download_file_message_5": f"What do you want to call this file?",
	"download_file_message_6": f"What do you want to call the app?",
	"download_file_message_7": f"[i]Installing Python app...[\]",
	"download_file_message_8": f"[g]Python app installed![\]",
	"download_file_message_9": f"It can now be opened via the \"Open a PyPlace app\" feature on the main menu!",
	"download_file_message_10": f"What number app do you want to download?",
	"download_file_message_11": f"What is the name of the file you would like to add? [g]Note:[\] This [u]MUST[\] be in the current folder.",
	"download_file_message_12": f"Are you sure that you want to download an external file?",

	"settings_error_1": f"[r]Error:[\] This is not available when PyPlace is executed on Replit. [g]You can download PyPlace instead[\]",
	"settings_option_1": "Delete an application",
	"settings_option_2": "Change Python command",
	"settings_option_3": "Restore to latest version",
	"settings_option_6": "Manage updater settings",
	"settings_option_4": "About",
	"settings_option_5": "Back to main menu",
	"settings_message_1": "Enter the number or letter for what you want to do",
	"settings_message_2": "What apps do you want to delete? (seperated by a space, so for applications 1, 2 and 3, you would enter: 1 2 3.",
	"settings_message_3": "What do you want the new command to be? Leave empty to set to default (python3).",
	"settings_message_4": "Command updated to [command]!",
	"settings_message_5": f"Are you sure you want to restore to the latest version published online?",
	"settings_message_6": f"[i]Downloading latest version of PyPlace...[\]",
	"settings_message_7": f"[g]The latest version of PyPlace is now ready in [g]PyPlace.py![\]",
	"settings_message_8": f"Would you like to run it?",
	"settings_message_9": f"[i]Attempting to run PyPlace.py...[\]",
	"settings_message_10": f"Continuing with current version. [g]NOTE: [\] Next time you start PyPlace.py, it will be on the latest version!",
	"settings_updater_option_1_a": f"Enable checking for updates",
	"settings_updater_option_1_b": f"Disable checking for updates",
	"settings_updater_option_2": f"Check for updates now",
	"settings_updater_message_1_a": f"[g]Updater enabled![\]",
	"settings_updater_message_1_b": f"[g]Updater disabled![\]",
	"settings_updater_message_2": f"[i]Checking for updates...[\]",
	"settings_updater_message_3": f"[g]Checked for updates![\]",


	"bulk_delete_message_1": f"[i]No apps to be deleted.[\]",
	"bulk_delete_message_2": f"[g]Deleted [amount] app(s)![\]",

	"app_updater_error_1": f"[r]Error:[\] Some apps that you have installed via the PyPlace Store don't support checking for updates.",
	"app_updater_message_1": f"Would you like to check if a newer version might support it?",
	"app_updater_message_2": f"No apps found. Please check back later",
	"app_updater_message_3": f"Would you like to update the following app(s) to the latest version?",
	"app_updater_message_4": f"All apps are on the latest version!"
}

def log(text):
	"""Sends a log message. Usage:
	```py
	log("Hello!")
	```"""
	print(f"{colors.LOG}Log:{colors.END} {text}")
def info(text):
	"""Sends an info message. Usage:
	```py
	info("Hello!")
	```"""
	print(f"{colors.INFO}Info:{colors.END} {text}")

def ok1(text):
	"""Sends a cyan OK message. Usage:
	```py
	ok1("Hello!")
	```"""
	print(f"{colors.OKCYAN}Success:{colors.END} {text}")

def ok2(text):
	"""Sends a green OK message. Usage:
	```py
	ok2("Hello!")
	```"""
	print(f"{colors.OKGREEN}Success:{colors.END} {text}")

def warning(text):
	"""Sends a warning message. Usage:
	```py
	warning("Hello!")
	```"""
	print(f"{colors.WARNING}Warning:{colors.END} {text}")

def error(text):
	"""Sends an error message. Usage:
	```py
	error("Hello!")
	```"""
	print(f"{colors.FAIL}Error:{colors.END} {text}")

def main():
	global API_KEY
	print()
	print("""
Welcome to PyPlace AI Translations! This allows you to translate PyPlace
automatically in any language, real ones and once that are made up using
ChatGPT. You will need to provide it with your own API key that you can
get from https://platform.openai.com/account/api-keys.

This uses the PyPlace built in app updater, available from version 1.0
and newer. Please check back after a PyPlace update if you want to 
translate anything.

Costs may apply. We're using the GPT3.5-turbo algorithm to keep costs low.

For PyPlace version: 1.0""")
	print()


	if API_KEY == None:
		invalid_input = True
		while invalid_input == True:
			API_KEY = input("Please enter your OpenAI API key: ")

			if API_KEY == "":
				print("Please enter a key.")
			else:
				# Create an event loop
				loop = asyncio.get_event_loop()

				# Run the coroutine within the event loop
				loop.run_until_complete(start_translate(API_KEY))
	else:
		invalid_input = False
		info("Continuing with API key set in Python file.")

		# Create an event loop
		loop = asyncio.get_event_loop()

		# Run the coroutine within the event loop
		loop.run_until_complete(start_translate(API_KEY))
		# start_translate(API_KEY)

async def start_translate(api_key):	
	# Language
	print("What language do you want to translate to? This can be anything like French, but also something like \"A language spoken in Belgium\". It could also be something like Klingon.")
	language_to_translate_to = input("I want to translate to: ")

	language_len = len(language)-1
	# subtract 1 because version is also part of dictionary

	# Calculate rough idea of time
	estimated_time = (SLEEP_TIME+5)*language_len # in seconds
	estimated_time = round(estimated_time/60) # in minutes

	input(f"Estimated time: {estimated_time} minutes. Press [ENTER] to start.")
	print("Press CTRL+C t stop at any time. Note that no progress is saved while translating.")

	index = 0
	for sentence in language:
		# info(f"Now translating: {sentence}")
		if language[sentence] == language["version"]:
			continue

		start_time = time.time()

		translation = await translate(language[sentence], language_to_translate_to, api_key)
		end_time = time.time()
		if translation == False:
			error("Could not translate something.")
			sys.exit(0)
		else:
			# print(translation)
			language[sentence] = translation

		# ok1("translation done")

		# Calculate time remaining

		items_left = language_len-index # items remaining
		time_remaining = ((end_time-start_time)*items_left)/60 # time remaining

		if round(time_remaining) >= 60:
			time_remaining = "more than 1 hour"
		elif round(time_remaining) < 1:
			time_remaining = "less than 1 minute"
		elif round(time_remaining) == 1:
			time_remaining = "1 minute"
		else:
			time_remaining = str(round(time_remaining))+" minutes"


		percentage_done = (index/language_len)*100

		print(f"{items_left}/{language_len} sentence(s) remaining | ETA: {time_remaining} | {round(percentage_done)}% complete")
		
		index += 1

	for key in language:
		if language[key] == language["version"]:
			continue
		language[key] = language[key].replace("[\]", colors.END)
		language[key] = language[key].replace("[r]", colors.FAIL)
		language[key] = language[key].replace("[o]", colors.WARNING)
		language[key] = language[key].replace("[g]", colors.OKGREEN)
		language[key] = language[key].replace("[c]", colors.OKCYAN)
		language[key] = language[key].replace("[i]", colors.INFO)
		language[key] = language[key].replace("[b]", colors.BOLD)
		language[key] = language[key].replace("[u]", colors.UNDERLINE)
		language[key] = language[key].replace("[nl]", "\n")
		language[key] = language[key].replace("[square]", "■")

	with open("language.json", 'w') as json_file:
		json.dump(language, json_file,
			indent=4,
			separators=(',', ': '))
	ok2("Translation complete! Please (re)start PyPlace for the changes to take affect.")

async def translate(sentence, language, api_key):
	"""Translate something in to chosen language"""
	# print("translation started of")
	# print(sentence)

	HEADERS = {
		"User-Agent": "PyPlace Translation",
		"Content-Type": "application/json",
		"Authorization": f"Bearer {api_key}"
	}

	messages = [
		{"role": "system", "content": SYSTEM_PROMPT.replace("[language]", language)},
		{"role": "user", "content": sentence}
	]

	# print(messages)

	request = requests.post(API_URL, headers=HEADERS, json= {
		"model": MODEL,
		"max_tokens": TOKEN_LIMIT,
		"messages": messages
	})

	# print(request.content)

	if request.status_code == 200:
		requestJSON = json.loads(request.content)
		output = requestJSON["choices"][0]["message"]["content"]

		# wait a bit not to overload OpenAI
		time.sleep(SLEEP_TIME)

		return output
	elif request.status_code == 429:
		warning("Request overload. Taking a timeout.")
		time.sleep(10)
		return await translate(sentence, language, api_key)
	else:
		error(request.status_code)
		print(request.content)
		return False


main()
