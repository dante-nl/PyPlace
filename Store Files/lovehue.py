	
#// import keyboard
#// ^ pip install keyboard

import time
import sys
import json
from os.path import exists
import os
import random

import requests
# from PIL import Image, ImageDraw


VERSION = 1.0

print()
print()
print()

try:
	from huesdk import Hue
	from huesdk import Discover
	#* ^ pip install huesdk
except:
	print("Error: Please download huesdk first. You can do this by doing: pip install huesdk --upgrade")
	sys.exit(0)

optional_requirements_satisfied = 0
try:
	import cv2
	optional_requirements_satisfied += 1
except:
	print("Error: Please download opencv-python first. You can do this by doing pip install opencv-python --upgrade")
	# sys.exit(0)

try:
	import numpy as np
	optional_requirements_satisfied += 1
except:
	print("Error: Please download numpy first. You can do this by doing pip install numpy --upgrade")
	# sys.exit(0)

try:
	import pyautogui
	optional_requirements_satisfied += 1
except:
	print("Error: Please download pyautogui first. You can do this by doing pip install pyautoguis --upgrade")
	# sys.exit(0)

try:
	from PIL import Image, ImageDraw
	optional_requirements_satisfied += 1
except:
	print("Error: Please download Pillow first. You can do this by doing pip install Pillow --upgrade")
	# sys.exit(0)

if optional_requirements_satisfied == 4:
	SIMULATE_SCREEN = True
else:
	SIMULATE_SCREEN = False
	print("""You are unable to use all features. Please also import with the following commands.

pip install opencv-python --upgrade
pip install numpy --upgrade
pip install pyautogui --upgrade
pip install Pillow --upgrade""")


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
	print(f"{colors.FAIL}Warning:{colors.END} {text}")

def flicker_light(lamp):
	"""Flickers the light on and off.
	```py
	lamp = hue.get_lights()[0]
	flicker_light(lamp)
	```
	"""
	brightness = lamp.bri
	if lamp.is_on:
		lamp.off(transition=0)
		time.sleep(.5)
		lamp.on(transition=0)
		lamp.set_brightness(brightness)
		time.sleep(.5)
		lamp.off(transition=0)
		time.sleep(.5)
		lamp.on(transition=0)
		lamp.set_brightness(brightness)
	else:
		lamp.on(transition=0)
		lamp.set_brightness(brightness)
		time.sleep(.5)
		lamp.off(transition=0)
		time.sleep(.5)
		lamp.on(transition=0)
		lamp.set_brightness(brightness)
		time.sleep(.5)
		lamp.off(transition=0)

def randomHEX():
	"""Generates a random HEX color. Does not include the hashtag"""
	def r(): return random.randint(0, 255)
	return '%02X%02X%02X' % (r(), r(), r())


def rgb_to_hex(r, g, b):
	"""Converts r, g, b to a HEX color. Does not include the hashtag"""
	return ('{:X}{:X}{:X}').format(r, g, b)


def get_colors(image_file, numcolors=10, resize=150):
	"""Get dominant color of an image"""
	# Resize image to speed up processing
	# img = Image.open(image_file)
	# img = img.copy()
	img = image_file
	img.thumbnail((resize, resize))
	# Reduce to palette
	paletted = img.convert('P', palette=Image.Palette.ADAPTIVE, colors=numcolors)
	# Find dominant colors
	palette = paletted.getpalette()
	color_counts = sorted(paletted.getcolors(), reverse=True)
	colors = list()
	for i in range(numcolors):
		palette_index = color_counts[i][1]
		dominant_color = palette[palette_index*3:palette_index*3+3]
		colors.append(tuple(dominant_color))
	return colors[0]





if exists("data.json"):
	with open('data.json') as dataFile:
		data = json.load(dataFile)
		USERNAME = data["username"]
		if type(USERNAME) != str:
			error("Could not find username")
			sys.exit(0)
else:
	try:
		discover = Discover()
		discover = json.loads(discover.find_hue_bridge())
		HUE_IP = discover[0]["internalipaddress"]
		USERNAME = Hue.connect(bridge_ip=HUE_IP)
	except:
		info("Please press the link button and run LoveHue again.")
		sys.exit(0)

	data_dict = {}
	data_dict["username"] = USERNAME
	data_dict["ip"] = HUE_IP

	data_dict_str = json.dumps(data_dict, indent=4, separators=(',', ': '))
	with open('data.json', 'w') as dataJSON:
		dataJSON.write(data_dict_str)
		# log("File created: setup.json")
try:
	discover = Discover()
	# print(discover)
	discover = json.loads(discover.find_hue_bridge())
	HUE_IP = discover[0]["internalipaddress"]
except:
	info("Trying cached version of IP...")
	try:
		with open('data.json') as dataFile:
			data = json.load(dataFile)
			HUE_IP = data["ip"]
	except:
		error("Could not connect to Hue bridge.")
		sys.exit(0)

# print(USERNAME)

hue = Hue(bridge_ip=HUE_IP, username=USERNAME)

validInput = False
while validInput == False:
	option = input("Would you like to use rooms (1) or light (2)? ")
	if option == "1":
		validInput = True
		room_or_light = "room"
	elif option == "2":
		validInput = True
		room_or_light = "light"
	else:
		error("You have to enter either 1 or 2.");
def selectLight():
	"""Gives the option for selecting lights. Returns the selected light as light/group object."""
	if(option == "1"):
		lights = hue.get_groups()
	else:
		lights = hue.get_lights()
	# print(rooms.lights)
	# for room in rooms:
	# 	print(room.name)
	# print()
	# print()
	# print()
	# print(lights)

	total_number = 1
	light_list = []
	for light in lights:
		print(f"[{total_number}] {light.name}")
		total_number += 1
		light_list.append(light)


	selected = input("What light do you want to do? ")
	return light_list[int(selected) -1]

def lightSelection():
	selected_light = selectLight()
	print(f"You selected {selected_light.name}! Flickering light(s) to confirm.")
	flicker_light(selected_light)
	incorrect_input = True
	while incorrect_input == True:
		correct_one = input("Light(s) flickered. Is this correct? (y/n) ")
		if correct_one.lower() == "y":
			incorrect_input = False
			return selected_light
		elif correct_one.lower() == "n":
			incorrect_input = False
			return lightSelection()
		else:
			error("You have to enter either y or n.")

def animationSelection(lamp):
	print(f"{colors.OKGREEN}■{colors.END}: Built in animations")
	print(f"{colors.OKCYAN}■{colors.END}: .lhad files (LoveHue Animation Dictionary)")

	print(f"""{colors.OKGREEN}[1] Random color{colors.END}
{colors.OKGREEN}[2] Random brightness{colors.END}
{colors.OKGREEN}[3] Simulate screen{colors.END}""")
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	current_item = 3
	animation_list = []
	for f in files:
		# do something
		if f.endswith(".lhad"):
			with open(f) as dataFile:
				f_json = json.load(dataFile)
			current_item += 1
			try:
				animation_name = f_json["name"]
				print(f"{colors.OKCYAN}[{current_item}] {animation_name} {colors.END}")
			except KeyError:
				print(f"{colors.FAIL}[{current_item}] Invalid animation file ({f}) {colors.END}")
			animation_list.append(f)
		else:
			pass
	selected_option = input("Please select an animation for what you want to do. ")
	try:
		selected_option = int(selected_option)
	except:
		error("Invalid input")
		return False
	if selected_option == 1:
		repeat_times = input("How many times to repeat? ")
		time_between = input("How long between each color change in seconds? ")

		try:
			int(repeat_times)
			int(time_between)
			invalid_input = True
			while invalid_input == True:
				if int(time_between) * int(repeat_times) < 60:
					time_total = f"{round(int(time_between) * int(repeat_times))} second(s)"
				elif int(time_between) * int(repeat_times) >= 60:
					time_total = f"{round(int(time_between) * int(repeat_times) / 60)} minute(s)"
				elif int(time_between) * int(repeat_times) / 60 >= 60:
					time_total = f"{round(int(time_between) * int(repeat_times) / 60)} hour(s)"
				input_value = input(
					f"This will take {time_total} to complete. Press [ENTER] to confirm or c to cancel. ").lower()
				if input_value != "c":
					invalid_input = False

					info("Animation started.")
					current_loop = 0
					for _ in range(int(repeat_times)):
						current_loop += 1
						color = randomHEX()
						lamp.on()
						lamp.set_color(hexa=color, transition=10)
						time.sleep(int(time_between))
						info(f"{round((current_loop / int(repeat_times)) * 100)}%")
					flicker_light(lamp)
					ok2("Animation completed.")
					input("Press [ENTER] to go home")
				else:
					invalid_input = False
		except:
			error("Invalid number")
	elif selected_option == 2:
		repeat_times = input("How many times to repeat? ")
		time_between = input("How long between each brightness change in seconds? ")

		try:
			int(repeat_times)
			int(time_between)
			invalid_input = True
			while invalid_input == True:
				if int(time_between) * int(repeat_times) < 60:
					time_total = f"{round(int(time_between) * int(repeat_times))} second(s)"
				elif int(time_between) * int(repeat_times) >= 60:
					time_total = f"{round(int(time_between) * int(repeat_times) / 60)} minute(s)"
				elif int(time_between) * int(repeat_times) / 60 >= 60:
					time_total = f"{round(int(time_between) * int(repeat_times) / 60)} hour(s)"
				input_value = input(
					f"This will take {time_total} to complete. Press [ENTER] to confirm or c to cancel. ").lower()
				if input_value != "c":
					invalid_input = False
					info("Animation started.")
					current_loop = 0
					for _ in range(int(repeat_times)):
						current_loop += 1
						lamp.set_brightness(round(random.randint(1, 254)))
						time.sleep(int(time_between))

					flicker_light(lamp)
					ok2("Animation completed.")
					input("Press [ENTER] to go home")
				else:
					invalid_input = False
		except:
			error("Invalid number")

	elif selected_option == 3:
		input_value = input(f"This will only stop after pressing ctrl+C. Press [ENTER] to confirm or c to cancel. ").lower()
		if input_value != "c":
			try:
				while True:
					try:
						img = pyautogui.screenshot()
						colors_rgb = get_colors(img)
						hex_color = rgb_to_hex(colors_rgb[0], colors_rgb[1], colors_rgb[2])
						# print(hex_color)
						lamp.set_color(hexa=hex_color, transition=0)
						time.sleep(.1)
					except:
						lamp.set_color(hexa="007aff", transition=0)
						time.sleep(.1)
					# try:
					# 	print(rgb_to_hex(get_colors(img)))
					# except:
					# 	print(type(get_colors(img)))
					

			except KeyboardInterrupt:
				flicker_light(lamp)
				ok2("Animation completed.")
				input("Press [ENTER] to go home")
				pass

		else:
			invalid_input = False
	else:
		# print(animation_list[selected_option - 2])
		with open(animation_list[selected_option - 4]) as dataFile:
			animation_json = json.load(dataFile)
		try:
			animation_name = animation_json["name"]
			animation_colors = animation_json["colors"]
		except KeyError:
			print(f"{colors.FAIL}[{current_item}] Invalid animation file ({f}) {colors.END}")
			return False
		info("Reading instructions...")
		repeat_times = input("How many times repeat?")

		total_time = 0
		current_item = 0
		for value in animation_json["colors"]:
			try:
				total_time += int(animation_json["colors"][current_item]["time_until_next"])
			except KeyError:
				total_time += 5
			current_item += 1
		invalid_input = True
		while invalid_input == True:
			if int(total_time) * int(repeat_times) < 60:
				time_total = f"{round(int(total_time) * int(repeat_times))} second(s)"
			elif int(total_time) * int(repeat_times) >= 60:
				time_total = f"{round(int(total_time) * int(repeat_times) / 60)} minute(s)"
			elif int(total_time) * int(repeat_times) / 60 >= 60:
				time_total = f"{round(int(total_time) * int(repeat_times) / 60)} hour(s)"
			input_value = input(
                            f"This will take {time_total} to complete. Press [ENTER] to confirm or c to cancel. ").lower()
			if input_value != "c":
				invalid_input = False

				max_lenght = len(animation_json["colors"])
				current_item = 0
				current_number = 1
				if lamp.is_on == False:
					lamp.on()
				for _ in range(int(repeat_times)):
					for __ in range(max_lenght):
						try:
							animation_json["colors"][current_item]["color"]
							from_memory = True
						except KeyError:
							animation_json["colors"][current_item]["color"] = lamp.hue
							from_memory = False
						# print(animation_json["colors"][current_item]["color"])

						try:
							animation_json["colors"][current_item]["brightness"]
						except KeyError:
							animation_json["colors"][current_item]["brightness"] = lamp.bri / 1

						# print(animation_json["colors"][current_item]["brightness"])
						
						try:
							animation_json["colors"][current_item]["time_until_next"]
						except KeyError:
							animation_json["colors"][current_item]["time_until_next"] = 5
						# print(animation_json["colors"][current_item]["time_until_next"])


						try:
							# if animation_json["colors"][current_item]["color"]:
							if from_memory == True:
								lamp.set_color(hexa=animation_json["colors"][current_item]["color"].replace("#", ""))
							else:
								lamp.set_color(hue=animation_json["colors"][current_item]["color"])
							# if animation_json["colors"][current_item]["brightness"]:
							factor = int(animation_json["colors"][current_item]["brightness"]) / 100
							selected_light.set_brightness(round(factor * 254))
							# if animation_json["colors"][current_item]["time_until_next"]:
							time.sleep(int(animation_json["colors"][current_item]["time_until_next"]))
							# print(current_item)
							current_item += 1
							if current_item == max_lenght:
								current_item = 0
							# print(current_item)
						except KeyError:
							pass
					info(f"{round((current_number / int(repeat_times)) * 100)}%")
					current_number += 1

				flicker_light(lamp)
				ok2("Animation completed.")
				input("Press [ENTER] to go home")
			else:
				invalid_input = False

def UpdateCheck():
	log("Checking for latest version...")
	response = requests.get("https://lovehue.dantenl.tk/version.json")
	if response.status_code != 200:
		print(f"{colors.FAIL}Error:{colors.END} Could not check for updates! Response code: {response.status_code}")
		return

	log("Comparing versions...")

	RequestText = response.text
	data = json.loads(RequestText)

	if data["version"] < VERSION:
		print(f"{colors.WARNING}WARNING:{colors.END} Your current version seems to be newer than the latest version that is released!")
	elif data["version"] > VERSION:
		print("————————")
		print(f"{colors.BOLD}UPDATE AVAILABLE!{colors.END}")
		print(
			f"Your current version ({VERSION}) is no longer the latest version! The latest one is {data['version']}")
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
					f"{colors.INFO}Downloading latest version of PyPlace...{colors.END}")
				log("Retrieving latest version of PyPlace...")
				r = requests.get(
					"https://pyplace.dantenl.tk/PyPlace-Latest.py", allow_redirects=True)
				if not r.ok:
					print(f"{colors.FAIL}Error:{colors.END} Could not get the PyPlace file! Status code: {r.status_code}")
					return
				log("Updating main PyPlace file")
				open('PyPlace.py', 'wb').write(r.content)
				print(
					f"{colors.OKGREEN}The latest version of PyPlace is now ready in {colors.BOLD}PyPlace.py!{colors.END}")
				NotAnswered2 = True
				while NotAnswered2 == True:
					Answer2 = input("Would you like to run it? (y/n) ")
					Answer2 = Answer2.lower()
					if Answer2 == "y":
						print(
							f"{colors.INFO}Attempting to run PyPlace.py...{colors.END}")
						os.execv(sys.argv[0], sys.argv)
						sys.exit(1)
					elif Answer2 == "n":
						print(
							f"Continuing with current version. {colors.BOLD}NOTE:{colors.END} Next time you start PyPlace.py, it will be on the latest version!")
						NotAnswered2 = False
						return
					else:
						print(
							f"{colors.FAIL}Error:{colors.END} I'm not sure what you mean with \"{Answer2}\".")

			elif Answer == "n":
				NotAnswered = False
				print("Update cancelled!")
				return
			else:
				print(
					f"{colors.FAIL}Error:{colors.END} I'm not sure what you mean with \"{Answer}\".")


selected_light = lightSelection()
# if variable is not set

invalid_option = True
while invalid_option == True:
	try:
		light_data
	except NameError:
		light_data = {
			"on": selected_light.is_on,
			"color": selected_light.hue,
			"brightness": selected_light.bri
		}
	print(light_data["color"])
	print(f"""What do you want to do?
[1] Turn on/off
[2] Set brightness
[3] Set light(s) to specific HEX color
[4] Start an animation
[5] Reset all to before execution of code
[{colors.INFO}u{colors.END}] Check for LoveHue updates
[{colors.FAIL}e{colors.END}] Exit""")
	option = input("Please enter the number or letter. ").lower()
	if option == "1":
		if selected_light.is_on == True:
			selected_light.off()
		else:
			selected_light.on()
			selected_light.set_brightness(light_data["brightness"])
	elif option == "2":
		print("Please input brightness in percent. 1 is least bright, 100 is brightest")
		brightness_percent = input("> ")
		brightness_percent = brightness_percent.replace("%", "")
		try:
			brightness_percent = int(brightness_percent)
			if brightness_percent <= 100:
				if brightness_percent > 0:
					factor = brightness_percent / 100
					print(factor*254)
					selected_light.set_brightness(round(factor * 254))
				else:
					error("Could not set brighness")
			else:
				error("Could not set brightness")

		except:
			error("Invalid!")
	elif option == "3":
		try:
			HEXColor = input("Please enter the HEX color: #")
			hex_list = []
			for letter in HEXColor:
				hex_list.append(letter)

			if len(hex_list) == 3:
				HEXColor = hex_list[0]+hex_list[0] + hex_list[1]+hex_list[1] + hex_list[2]+hex_list[2]
			selected_light.on()
			selected_light.set_color(hexa=HEXColor)
		except:
			error("Could not set light color.")
	elif option == "4":
		animationSelection(selected_light)
	elif option == "5":
		selected_light.set_color(hue=light_data["color"])
		if light_data["on"] == True:
			selected_light.on()
		else:
			selected_light.off()
		selected_light.set_brightness(light_data["brightness"])
		info("Reset all.")
	elif option == "u":
		UpdateCheck()
	elif option == "e":
		sys.exit(0)
