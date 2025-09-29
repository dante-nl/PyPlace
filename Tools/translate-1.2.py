
# ██████╗░██╗░░░██╗██████╗░██╗░░░░░░█████╗░░█████╗░███████╗
# ██╔══██╗╚██╗░██╔╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔════╝
# ██████╔╝░╚████╔╝░██████╔╝██║░░░░░███████║██║░░╚═╝█████╗░░
# ██╔═══╝░░░╚██╔╝░░██╔═══╝░██║░░░░░██╔══██║██║░░██╗██╔══╝░░
# ██║░░░░░░░░██║░░░██║░░░░░███████╗██║░░██║╚█████╔╝███████╗
# ╚═╝░░░░░░░░╚═╝░░░╚═╝░░░░░╚══════╝╚═╝░░╚═╝░╚════╝░╚══════╝

# ████████╗██████╗░░█████╗░███╗░░██╗░██████╗██╗░░░░░░█████╗░████████╗██╗░█████╗░███╗░░██╗░██████╗
# ╚══██╔══╝██╔══██╗██╔══██╗████╗░██║██╔════╝██║░░░░░██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔════╝
# ░░░██║░░░██████╔╝███████║██╔██╗██║╚█████╗░██║░░░░░███████║░░░██║░░░██║██║░░██║██╔██╗██║╚█████╗░
# ░░░██║░░░██╔══██╗██╔══██║██║╚████║░╚═══██╗██║░░░░░██╔══██║░░░██║░░░██║██║░░██║██║╚████║░╚═══██╗
# ░░░██║░░░██║░░██║██║░░██║██║░╚███║██████╔╝███████╗██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║██████╔╝
# ░░░╚═╝░░░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝╚═════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═════╝░

# F̲o̲r̲ v̲e̲r̲s̲i̲o̲n̲ 1̲.̲2̲ (version 4.3)
# 🄱🅈 🄳🄰🄽🅃🄴_🄽🄻

# This PyPlace app allows you to help translate PyPlace in to your language!
# First time translating something in your language should not take longer
# than 10 minutes, minor updates should just take a few seconds and larger
# updates will probably take just a few minutes. 

# ————————————————————————————
# Please do not edit anything below this point as it may break the code.

import json
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


output = {
	"version": 1.2
}


def error(error_msg):
	print(f"{bcolors.FAIL}Error:{bcolors.END} {error_msg}")


def info(info_msg):
	print(f"{bcolors.INFO}{info_msg}{bcolors.END}")

def convert_colors(text):
	"""Converts color variables to actual color codes."""
	result = text.replace(r"[\]", bcolors.END)
	result = result.replace(r"[r]", bcolors.FAIL)
	result = result.replace(r"[o]", bcolors.WARNING)
	result = result.replace(r"[g]", bcolors.OKGREEN)
	result = result.replace(r"[c]", bcolors.OKCYAN)
	result = result.replace(r"[i]", bcolors.INFO)
	result = result.replace(r"[b]", bcolors.BOLD)
	result = result.replace(r"[u]", bcolors.UNDERLINE)
	result = result.replace(r"[nl]", "\n")
	result = result.replace("[square]", "■")
	return result

def ask_translation(prompt, name):
	global output
	print()
	print()
	translation_complete = False
	while translation_complete == False:
		translation = input(f"{prompt} \n> ")
		print()
		print(convert_colors(translation))
		confirmation = input("Is this correct? (y/n) ").lower()
		if confirmation == "y":
			output[name] = convert_colors(translation)
			translation_complete = True
		elif confirmation == "n":
			pass
		else:
			error("I'm not sure what you mean with that.")


print("————————————————————————————")
print(f"Welcome to {bcolors.BOLD}PyPlace Translate{bcolors.END}!")
print()
print("It is really easy! Just translate the text and share the output in the Discord server!")
print("Please do not translate anything in [square brackets]. These are used for variables, such")
print("as the current version number. It is also used for colors.")

input("Press [ENTER] to continue")
print()
print("If you have already translated the most recent version, you can choose to only translate the things added in this version instead.")
print("[1] Translate everything")
print("[2] Translate only new sentences")
invalid_input = True
while invalid_input == True:
	input_to_handle = input("What would you like to do? ")
	if input_to_handle == "1":
		invalid_input = False
		info("Generic messages")
		ask_translation(r"[r]Error:[\] I'm not sure what you mean with that!", "input_error")
		ask_translation(r"Press [ENTER] to return to the main menu", "back_to_menu")
		ask_translation(r"Cancel", "cancel")
		ask_translation(r"[o]Restarting PyPlace...[\]", "restart_pyplace")

		info("Intro message.")
		ask_translation(r"Welcome to [b]PyPlace[\]!", "intro_1")


		info("There are multiple new lines so the text won't look so long.")
		ask_translation(r"PyPlace is a Python application that allows you [nl]to get a simple overview of your other Python [nl]applications, and it also allows you to easily [nl]install new ones!", "intro_2")

		info("Start-up warnings")
		ask_translation(r"[o]WARNING:[\] It appears that you're running this on the Replit page! We recommend downloading PyPlace and running it for yourself.", "replit_warning")

		info("The setup")
		ask_translation(r"[i]Setting up PyPlace...[\]", "setup_4")
		ask_translation(r"[g]PyPlace is set up![\]", "setup_5")
		ask_translation(r"Press [ENTER] to start PyPlace", "setup_6")

		info("The main menu")
		ask_translation(r"Open a PyPlace app", "main_menu_option_1")
		ask_translation(r"Add a PyPlace app", "main_menu_option_2")
		ask_translation(r"Check for app updates", "main_menu_option_5")
		ask_translation(r"Open settings", "main_menu_option_3")
		ask_translation(r"Exit PyPlace", "main_menu_option_4")
		ask_translation(r"What do you want to do?", "main_menu_message_1")
		ask_translation(r"Enter the number or letter for what you want to do:", "main_menu_message_2")

		info("The updater")
		ask_translation(r"[r]Error:[\] Could not check for updates! Response code: [code]", "update_error_1")
		ask_translation(r"[r]Error:[\] Could not get the PyPlace file! Response code: [code]", "update_error_2")
		ask_translation(r"[o]WARNING:[\] Your current version seems to be newer than the latest version that is released!", "update_warning_1")
		ask_translation(r"[b]UPDATE AVAILABLE![\]", "update_message_1")
		ask_translation(r"Your current version ([version]) is no longer the latest version! The latest version is [version_latest].", "update_message_2")
		ask_translation(r"Here are the release notes:", "update_message_3")
		ask_translation(r"Would you like to update right now?", "update_message_4")
		ask_translation(r"[i]Downloading latest version of PyPlace...[\]", "update_message_5")
		ask_translation(r"[g]The latest version of PyPlace is now ready!", "update_message_6")
		ask_translation(r"Would you like to run it?", "update_message_7")
		ask_translation(r"[i]Attempting to run PyPlace[\]", "update_message_8")
		ask_translation(r"Continuing with current version. [b]NOTE:[\] Next time you start PyPlace, it will be on the latest version!", "update_message_9")

		info("The app executer")
		ask_translation(r"[r]Error:[\] You do not have any applications installed! You can download them via \"Download a PyPlace app\" on the main menu.", "execute_file_error_1")
		ask_translation(r"[r]Error:[\] This is not a Python file, and thus can not be executed by PyPlace.", "execute_file_error_2")
		ask_translation(r"[o][square][\]: Experimental application", "execute_file_message_1")
		ask_translation(r"[c][square][\]: Application downloaded from the PyPlace store", "execute_file_message_2")
		ask_translation(r"What number app do you want to open?", "execute_file_message_3")
		ask_translation(r"[i]Attempting to run [app]...[\]", "execute_file_message_4")
		ask_translation(r"[g]File executed[\]", "execute_file_message_5")

		info("The app downloader")
		ask_translation(r"[r]Error:[\] This is not a Python file, and thus can not be downloaded by PyPlace", "download_file_error_1")
		ask_translation(r"[r]Error:[\] Could not download the Python file! Status code [code]", "download_file_error_2")
		ask_translation(r"[r]Error:[\] A file with that name ([name]) already exists!", "download_file_error_3")
		ask_translation(r"[r]Error:[\] That does not appear to be a valid URL!", "download_file_error_4")
		ask_translation(r"URL to Python file", "download_file_option_1")
		ask_translation(r"Download from PyPlace Store", "download_file_option_2")
		ask_translation(r"Download experiment", "download_file_option_3")
		ask_translation(r"Add local file", "download_file_option_4")
		ask_translation(r"How do you want to add a PyPlace app?", "download_file_message_1")
		ask_translation(r"Please enter the direct URL to a Python file:", "download_file_message_2")
		ask_translation(r"[i]Downloading Python app...[\]", "download_file_message_3")
		ask_translation(r"[g]Python app downloaded![\]", "download_file_message_4")
		ask_translation(r"What do you want to call this file?", "download_file_message_5")
		ask_translation(r"What do you want to call the app?", "download_file_message_6")
		ask_translation(r"[i]Installing the Python app...[\]", "download_file_message_7")
		ask_translation(r"[g]Python app installed![\]", "download_file_message_8")
		ask_translation(r"It can now be opened via the \"Open a PyPlace app\" feature on the main menu!", "download_file_message_9")
		ask_translation(r"What number app do you want to download?", "download_file_message_10")
		ask_translation(r"What is the name of the file you would like to add? [b]Note:[\] This [u]MUST[\] be in the current folder.", "download_file_message_11")
		ask_translation(r"Are you sure that you want to download an external file?", "download_file_message_12")

		info("The settings")
		ask_translation(r"[r]Error:[\] This is not available when PyPlace is executed on Replit. [b]You can download PyPlace instead.[\]", "settings_error_1")
		ask_translation(r"Delete an application", "settings_option_1")
		ask_translation(r"Restore to latest version", "settings_option_3")
		ask_translation(r"About", "settings_option_4")
		ask_translation(r"Back to main menu", "settings_option_5")
		ask_translation(r"Manage updater settings", "settings_option_6")
		ask_translation(r"Enter the number or letter for what you want to do.", "settings_message_1")
		ask_translation(r"What apps do you want to delete? (seperated by a space, so for applications 1, 2 and 3, you would enter 1 2 3.)", "settings_message_2")
		ask_translation(r"Are you sure you want to restore to the latest version published online?", "settings_message_5")
		ask_translation(r"[i]Downloading the latest version of PyPlace...[\]", "settings_message_6")
		ask_translation(r"[g]The latest version of PyPlace is now ready![\]", "settings_message_7")
		ask_translation(r"Would you like to run it?", "settings_message_8")
		ask_translation(r"[i]Attempting to run PyPlace...[\]", "settings_message_9")
		ask_translation(r"Continuing with current version. [b]NOTE:[\] Next time you start PyPlace, it will be on the latest version!", "settings_message_10")

		ask_translation(r"Enable checking for updates", "settings_updater_option_1_a")
		ask_translation(r"Disable checking for updates", "settings_updater_option_1_b")
		ask_translation(r"Check for updates now", "settings_updater_option_2")
		ask_translation(r"[g]Updater enabled![\]", "settings_updater_message_1_a")
		ask_translation(r"[g]Updater disabld![\]", "settings_updater_message_1_b")
		ask_translation(r"[i]Checking for updates...[\]", "settings_updater_message_2")
		ask_translation(r"[g]Checked for updates![\]", "settings_updater_message_2")

		info("PyPlace Bulk Delete prompts")
		ask_translation(r"[i]No apps to be deleted.[\]", "bulk_delete_message_1")
		ask_translation(r"[g]Deleted [amount] app(s)![\]", "bulk_delete_message_2")

		info("PyPlace App Updater")
		ask_translation(r"[r]Error:[\] Some apps that you have installed via the PyPlace Store don't support checking for updates.", "app_updater_error_1")
		ask_translation(r"Would you like to check if a newer version might support it?", "app_updater_message_1")
		ask_translation(r"No apps found. Please check back later.", "app_updater_message_2")
		ask_translation(r"Would you like to update the following app(s) to the latest version?", "app_updater_message_3")
		ask_translation(r"All apps are on the latest version!", "app_updater_message_4")

		can_try_out = True
	elif input_to_handle == "2":
		invalid_input = False

		ask_translation(r"[o]Restarting PyPlace...[\]", "restart_pyplace")
		ask_translation(r"[o]WARNING:[\] It appears that you're running this on the Replit page! We recommend downloading PyPlace and running it for yourself.", "replit_warning")
		ask_translation(r"Would you like to update the following app(s) to the latest version?", "app_updater_message_3")
		ask_translation(r"[g]The latest version of PyPlace is now ready!", "update_message_6")
		ask_translation(r"[i]Attempting to run PyPlace[\]", "update_message_8")
		ask_translation(r"Continuing with current version. [b]NOTE:[\] Next time you start PyPlace, it will be on the latest version!", "update_message_9")

		can_try_out = False

print(f"{bcolors.OKGREEN}Done!{bcolors.END} You have completed all the translations for this version!")
print(f"Please share the file named {bcolors.BOLD}language_export.json{bcolors.END} in the PyPlace Discord server (discord.gg/EXqsHeaXE3)")
if can_try_out == True:
	try_out = input(f"Would you like to try out your translations? {bcolors.BOLD}NOTE:{bcolors.END} This will overwrite your currently set language. (y/n) ")
	if try_out.lower() == "y":
		with open("language.json", 'w') as json_file:
			json.dump(output, json_file,
					indent=4,
				separators=(',', ': '))

with open("language_export.json", 'w') as json_file:
	json.dump(output, json_file,
            indent=4,
           	separators=(',', ': '))
