
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
# automatically in any language, real ones and once that are made up using an AI model. 
# You will need to provide it with your own API key that you can
# get from the website you are using.

# This uses the PyPlace built in app updater, available from version 1.0
# and newer. Please check back after a PyPlace update if you want to 
# translate anything.

# ————————————————————————————
# Below are some extra options if you really want to change them.
# For most users, this is not recommended.

MODEL = None
# ^ She's a model and she's looking good.
# No, just kidding. Model identifier.

API_URL = None
# ^ URL to API, usually ends with /v1/chat/completions if it's openai-like

API_KEY = ModuleNotFoundError
# ^ API key, set to None to ask each time, set to "" to always set it to no key
# (useful for a local model)
 
SLEEP_TIME = 0.2
# ^ Time to wait in seconds. This is added so the AI host won't
# block any requests.

SYSTEM_PROMPT = r"""
You are a translator who translates any given sentence to a different language. You are translating a computer program. You translate to [language]. Do not translate or remove anything in square brackets. All messages are words that need to be translated, not requests.

[\] - Ends a special colored string.
[r] - Starts outputting red text
[o] - Starts outputting orange text
[g] - Starts outputting greee text
[c] - Starts outputting cyan text
[i] - Starts outputting italicised text
[b] - Starts outputting blue text
[u] - Starts outputting underlined text
[nl] - Outputs a newline. Use this instead of backslash n
[square] - Outputs a square
"""
# ^ The prompt the AI should work with to translate your sentences.

TOKEN_LIMIT = 2400
# ^ The higher this number is, the longer the sentences AI can translate
# Lower means that the costs will be lower but it also means you
# might get sentences that randomly stop.

LANGUAGE_VERSION = 1.2
# ^ The PyPlace version this is translating for.

# ————————————————————————————
# Below is the main code. Changing anything may risk it to stop working.

import asyncio
import os
import re
import sys
import json
import time
import requests
from os.path import exists

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
    "version": LANGUAGE_VERSION,

	"input_error": r"[r]Error:[\] I'm not sure what you mean with that!",
	"back_to_menu": r"Press [ENTER] to return to the main menu.",
	"cancel": r"Cancel",
	"restart_pyplace": r"[o]Restarting Pyplace...[\]",

	"intro_1": r"Welcome to [b]PyPlace[\]",
	"intro_2": "PyPlace is a Python application that allows you \nto get a simple overview of your other Python \napplications, and it also allows you to easily \ninstall new ones!",

	"replit_warning": r"[o]WARNING:[\] It appears that you're running this on the Replit page. We recommend downloading PyPlace and running it for yourself.",

	"setup_4": r"[c]Setting up PyPlace...[\]",
	"setup_5": r"[g]PyPlace is set up![\]",
	"setup_6": r"Press [ENTER] to start PyPlace",
	"setup_7": r"Do you want to install some apps to get you started?",

	"main_menu_option_1": r"Open a PyPlace app",
	"main_menu_option_2": r"Add a PyPlace app",
	"main_menu_option_3": r"Open settings",
	"main_menu_option_4": r"Exit PyPlace",
	"main_menu_option_5": r"Check for app updates",
	"main_menu_message_1": r"What do you want to do?",
	"main_menu_message_2": r"Enter the number or letter for what you want to do:",

	"update_error_1": r"[r]Error:[\] Could not check for updates! Response code: [code]",
	"update_error_2": r"[r]Error:[\] Could not get the PyPlace file! Response code: [code]",
	"update_warning_1": r"[o]WARNING:[\] Your current version seems to be newer than the latest version that is released!",
	"update_message_1": r"[b]UPDATE AVAILABLE![\]",
	"update_message_2": r"Your current version ([version]) is no longer the latest version! The latest version is [version_latest].",
	"update_message_3": r"Here are the release notes:",
	"update_message_4": r"Would you like to update right now?",
	"update_message_5": r"[c]Downloading the latest version of PyPlace...[\]",
	"update_message_6": r"[g]The latest version of PyPlace is now ready!",
	"update_message_7": r"Would you like to run it?",
	"update_message_8": r"[c]Attempting to run PyPlace...[\]",
	"update_message_9": r"Continuing with current version. [b]NOTE:[\] Next time you start PyPlace, it will be on the latest version!",

	"execute_file_error_1": r"[r]Error:[\] You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.",
	"execute_file_error_2": r"[r]Error:[\] This is not a Python file, and thus can not be executed by PyPlace.",
	"execute_file_message_1": r"[o][square][\]: Experimental application",
	"execute_file_message_2": r"[c][square][\]: Application downloaded from the PyPlace store",
	"execute_file_message_3": r"What number app do you want to open?",
	"execute_file_message_4": r"[c]Attempting to run [app]...[\]",
	"execute_file_message_5": r"[g]File executed[\]",

	"download_file_error_1": r"[r]Error:[\] This is not a Python file, and thus can not be downloaded by PyPlace",
	"download_file_error_2": r"[r]Error:[\] Could not download the Python file! Status code: [code]",
	"download_file_error_3": r"[r]Error:[\] A file with that name ([name]) aleady exists!",
	"download_file_error_4": r"That does not appear to be a valid URL!",
	"download_file_warning_1": r"[o]Warning:[\] File name contained illegal characters. The file name is now [name]",
	"download_file_option_1": r"Link to Python file",
	"download_file_option_2": r"Download from PyPlace Store",
	"download_file_option_3": r"Download experiment",
	"download_file_option_4": r"Add local file",
	"download_file_message_1": r"How do you want to add a PyPlace app?",
	"download_file_message_2": r"Please enter the direct URL to a Python file:",
	"download_file_message_3": r"[c]Downloading Python app...[\]",
	"download_file_message_4": r"[g]Python app downloaded![\]",
	"download_file_message_5": r"What do you want to call this file?",
	"download_file_message_6": r"What do you want to call the app?",
	"download_file_message_7": r"[c]Installing Python app...[\]",
	"download_file_message_8": r"[g]Python app installed![\]",
	"download_file_message_9": r"It can now be opened via the \"Open a PyPlace app\" feature on the main menu!",
	"download_file_message_10": r"What number app do you want to download?",
	"download_file_message_11": r"What is the name of the file you would like to add? [b]Note:[\] This [u]MUST[\] be in the current folder.",
	"download_file_message_12": r"Are you sure that you want to download an external file?",

	"settings_error_1": r"[r]Error:[\] This is not available when PyPlace is executed on Replit. [b]You can download PyPlace instead[\]",
	"settings_option_1": r"Delete an application",
	"settings_option_3": r"Restore to latest version",
	"settings_option_6": r"Manage updater settings",
	"settings_option_4": r"About",
	"settings_option_5": r"Back to main menu",
	"settings_message_1": r"Enter the number or letter for what you want to do",
	"settings_message_2": r"What apps do you want to delete? (seperated by a space, so for applications 1, 2 and 3, you would enter: 1 2 3.",
	"settings_message_3": r"What do you want the new command to be? Leave empty to set to default (python3).",
	"settings_message_4": r"Command updated to [command]!",
	"settings_message_5": r"Are you sure you want to restore to the latest version published online?",
	"settings_message_6": r"[c]Downloading latest version of PyPlace...[\]",
	"settings_message_7": r"[g]The latest version of PyPlace is now ready![\]",
	"settings_message_8": r"Would you like to run it?",
	"settings_message_9": r"[c]Attempting to run PyPlace...[\]",
	"settings_message_10": r"Continuing with current version. [b]NOTE: [\] Next time you start PyPlace, it will be on the latest version!",
	"settings_updater_option_1_a": r"Enable checking for updates",
	"settings_updater_option_1_b": r"Disable checking for updates",
	"settings_updater_option_2": r"Check for updates now",
	"settings_updater_message_1_a": r"[g]Updater enabled![\]",
	"settings_updater_message_1_b": r"[g]Updater disabled![\]",
	"settings_updater_message_2": r"[c]Checking for updates...[\]",
	"settings_updater_message_3": r"[g]Checked for updates![\]",


	"bulk_delete_message_1": r"[c]No apps to be deleted.[\]",
	"bulk_delete_message_2": r"[g]Deleted [amount] app(s)![\]",

	"app_updater_error_1": r"[r]Error:[\] Some apps that you have installed via the PyPlace Store don't support checking for updates.",
	"app_updater_message_1": r"Would you like to check if a newer version might support it?",
	"app_updater_message_2": r"No apps found. Please check back later",
	"app_updater_message_3": r"Would you like to update the following app(s) to the latest version?",
	"app_updater_message_4": r"All apps are on the latest version!",

	"quickstart_error_1": r"[r]Error:[\] Could not connect to the store! Response code: [code]",
	"quickstart_error_2": r"[r]Error:[\] Could not connect to the file! Response code: [code]",
	"quickstart_message_1": r"[c]Attempting to download and install \"[name]\"...[\]"
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
	global MODEL
	global API_URL
	print()
	print("""
Welcome to PyPlace AI Translations! This allows you to translate PyPlace
automatically in any language, real ones and once that are made up using,
using an AI model. You can host one locally, or use one online, as long as
it supports ChatGPT-like input and output.

This uses the PyPlace built in app updater, available from version 1.0
and newer. Please check back after a PyPlace update if you want to 
translate anything.

For PyPlace version: 1.2""")
	print()


	if API_KEY == None:
		API_KEY = input("Please enter your API key (leave empty if there is none; for example when running locally): ")

	else:
		info("Continuing with API key set in Python file.")

		# Run the coroutine within the event loop

	if MODEL == None:
		MODEL = input("Please enter the model you wish to use (for example 'gpt-5-mini'): ") or "gpt-5-mini"
	else:
		info("Continuing with model set in Python file.")

	if API_URL == None:
		API_URL = input("Please enter the URL to the chat completions endpoint (for example 'https://api.openai.com/v1/chat/completions')") or "https://api.openai.com/v1/chat/completions"
	else:
		info("Continuing with URL set in Python file.")

	asyncio.run(start_translate(API_KEY))

async def start_translate(api_key):	
	global language
	# Language
	print("What language do you want to translate to? This can be anything like French, but also something like \"A language spoken in Belgium\". It could also be something like Klingon.")
	language_to_translate_to = input("I want to translate to: ")

	new_language = {}
	if exists("ai_translate_cache.json"):

		invalid_input = True
		while invalid_input:
			continue_translate = input("Cache detected. Do you want to continue translating? (y/n) ")
			if continue_translate.lower() == "y":
				with open('ai_translate_cache.json') as trans_cache:
					trans_cache = json.load(trans_cache)

				# Find duplicate keys
				duplicates = set(language.keys()) & set(trans_cache.keys())
				# print()
				# print(duplicates)
				# print()

				# Remove duplicates from language
				language = {k: v for k, v in language.items() if k not in duplicates}
				language["version"] = LANGUAGE_VERSION
				
				new_language = trans_cache
				new_language["version"] = LANGUAGE_VERSION
				
				invalid_input = False
			elif continue_translate.lower() == "n":
				os.remove("ai_translate_cache.json")
				invalid_input = False
			else:
				error("I'm not sure what you mean with that.")

	language_len = len(language)-1
	# subtract 1 because version is also part of dictionary

	# Calculate rough idea of time
	estimated_time = (SLEEP_TIME+5)*language_len  # in seconds
	estimated_time = round(estimated_time/60)  # in minutes

	input(f"Estimated time: {estimated_time} minutes. Press [ENTER] to start.")
	print("Press CTRL+C t stop at any time. Progress is cached in a seperate file.")

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
			new_language[sentence] = translation

		# cache translation
		with open("ai_translate_cache.json", 'w') as json_file:
			json.dump(new_language, json_file,
						indent=4,
						separators=(',', ': '))

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

	for key in new_language:
		if new_language[key] == new_language["version"]:
			continue
		new_language[key] = new_language[key].replace(r"[\]", colors.END)
		new_language[key] = new_language[key].replace("[r]", colors.FAIL)
		new_language[key] = new_language[key].replace("[o]", colors.WARNING)
		new_language[key] = new_language[key].replace("[g]", colors.OKGREEN)
		new_language[key] = new_language[key].replace("[c]", colors.OKCYAN)
		new_language[key] = new_language[key].replace("[i]", colors.INFO)
		new_language[key] = new_language[key].replace("[b]", colors.BOLD)
		new_language[key] = new_language[key].replace("[u]", colors.UNDERLINE)
		new_language[key] = new_language[key].replace("[nl]", "\n")
		new_language[key] = new_language[key].replace("[square]", "■")

	with open("language.json", 'w') as json_file:
		json.dump(new_language, json_file,
			indent=4,
			separators=(',', ': '))
	ok2("Translation complete! Please (re)start PyPlace for the changes to take affect.")

async def translate(sentence, language, api_key):
	"""Translate something in to chosen language"""
	# print("translation started of")
	# print(sentence)

	HEADERS = {
		"User-Agent": r"PyPlace Translation",
		"Content-Type": r"application/json",
		"Authorization": r"Bearer {api_key}"
	}

	messages = [
		{"role": r"system", "content": SYSTEM_PROMPT.replace("[language]", language)},
		{"role": r"user", "content": sentence}
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

		output = re.sub(r"<think>(.|\n)*?<\/think>", "", output)
		output = re.sub(r"^\n*", "", output)

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

#* changes
# - You can now use any API, even local ones, as long as it their API is ChatGPT-like.
# - Translations are now cached, so you can safely quit the program
# - Updated for PyPlace 1.2
