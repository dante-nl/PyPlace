	
#// import keyboard
#// ^ pip install keyboard

import re
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
	# print("Error: Please download opencv-python first. You can do this by doing pip install opencv-python --upgrade")
	pass
	# sys.exit(0)

try:
	import numpy as np
	optional_requirements_satisfied += 1
except:
	# print("Error: Please download numpy first. You can do this by doing pip install numpy --upgrade")
	pass
	# sys.exit(0)

try:
	import pyautogui
	optional_requirements_satisfied += 1
except:
	# print("Error: Please download pyautogui first. You can do this by doing pip install pyautoguis --upgrade")
	pass
	# sys.exit(0)

try:
	from PIL import Image, ImageDraw, ImageColor
	optional_requirements_satisfied += 1
except:
	# print("Error: Please download Pillow first. You can do this by doing pip install Pillow --upgrade")
	pass
	# sys.exit(0)
	

if optional_requirements_satisfied == 4:
	ALL = True
else:
	ALL = False
	print("""You are unable to use all features. You can fix this by running the following commands.

pip install opencv-python --upgrade
pip install numpy --upgrade
pip install pyautogui --upgrade
pip install Pillow --upgrade""")


def lid_closed():
	"""Returns True if the laptop lid is closed, False otherwise."""
	if sys.platform == 'darwin':
		# On macOS, we can use the 'ioreg' command to get the lid state
		import subprocess
		result = subprocess.run(
			['ioreg', '-r', '-k', 'AppleClamshellState', '-d', '4'], capture_output=True, text=True)
		output = result.stdout.strip()


		match = re.search(r'AppleClamshellState.*?(\d+)', output, re.DOTALL)
		if match:
			lid_state = int(match.group(1))
		else:
			lid_state = 1  # default to open
		return lid_state == 0
	elif sys.platform.startswith('win'):
		# On Windows, we can use the 'powercfg' command to get the lid state
		import subprocess
		result = subprocess.run(
			['powercfg', '-attributes', 'sub_buttonlid', '-q'], capture_output=True, text=True)
		output = result.stdout.strip()
		lid_state = output.split()[-1]
		return lid_state == '0x0'
	else:
		# Unsupported platform
		return False


lid_closed_ = lid_closed()
print(f"Laptop lid is closed: {lid_closed_}")

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
	img = image_file
	img.thumbnail((resize, resize))
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


def how_dark(color):
	"""Returns a number depening on how dark the color is.
	```py
	print(how_dark("#000000"))  # 1 (black)
	print(how_dark("#808080"))  # 2 (gray)
	print(how_dark("#FFFFFF"))  # 4 (white)
	print(how_dark("#FF0000"))  # 2 (red)
	print(how_dark("#F1B0AE"))  # 1 (dark pink)
	```
	| Darkness  	| Value 	|
	|-----------	|-------	|
	| Very dark 	| 1     	|
	| Dark      	| 2     	|
	| Medium    	| 3     	|
	| Light     	| 4     	|
	"""
	  # Convert the HEX color to RGB
	r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
	# brightness = (0.212 * r + 0.701 * g + 0.087 * b) / 255
	# brightness = float(((r * g * b) ^ (1/3)) / 255)
	# print(type(r, g, b))
	# print(type(r))
	# print(type(g))
	# print(type(b))


	denominator = 255 * (3) ** (1/2)
	brightness = (r**2 + g**2 + b**2) ** (1/2) / denominator
	# return brightness

	# Calculate the brightness using the formula:
	# brightness = sqrt(0.241*r^2 + 0.691*g^2 + 0.068*b^2)
	# brightness = math.sqrt(0.241 * r**2 + 0.691 * g**2 + 0.068 * b**2)

	# Return a brightness level based on the calculated brightness

	if brightness < 0.25:
		return 1
	elif brightness >= 0.25 and brightness < 0.35:
		return 2
	elif brightness >= 0.35 and brightness < 1:
		return 3
	# elif brightness >= .7 and brightness <= 1:
	# 	return 3
	else:
		return 3
	# if brightness < 90:
	# 	return 1
	# elif brightness >= 90 and brightness < 170:
	# 	return 2
	# elif brightness >= 170 and brightness < 250:
	# 	return 3
	# else:
	# 	return 4

# Test the function
# print(how_dark("#000000"))  # 1 (black)
# print(how_dark("#808080"))  # 2 (gray)
# print(how_dark("#FFFFFF"))  # 3 (white)
# print(how_dark("#FF0000"))  # 2 (red)
# print(how_dark("#F1B0AE"))  # 2 (dark pink)

# sys.exit(0)

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
{colors.OKGREEN}[2] Random brightness{colors.END}""")
	if ALL == True:
		print(f"{colors.OKGREEN}[3] Simulate screen{colors.END}")
	else:
		print(f"{colors.FAIL}[3] Simulate screen{colors.END}")
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
	print(lamp.bri)
	if selected_option == 1:
		# repeat_times = input("How many times to repeat? ")
		time_between = input("How long between each color change in seconds? ")

		try:
			# int(repeat_times)
			# int(time_between)
			invalid_input = True
			execute_code = True
			while invalid_input == True:
				# if int(time_between) * int(repeat_times) < 60:
				# 	time_total = f"{round(int(time_between) * int(repeat_times))} second(s)"
				# elif int(time_between) * int(repeat_times) >= 60:
				# 	time_total = f"{round(int(time_between) * int(repeat_times) / 60)} minute(s)"
				# elif int(time_between) * int(repeat_times) / 60 >= 60:
				# 	time_total = f"{round(int(time_between) * int(repeat_times) / 60)} hour(s)"
				input_value = input(
					f"This will take stop when you press ctrl+C. Press [ENTER] to confirm or c to cancel. ").lower()
				if input_value != "c":
					invalid_input = False

					info("Animation started.")
					current_loop = 0
					try:
						while execute_code == True:
							try:
								if(lid_closed() == True):
									print()
									lamp.off(transition=20)
									ok2("Animation completed.")
									input("Press [ENTER] to go home")
									execute_code = False
							except Exception as e:
								error(e)
								pass
							current_loop += 1
							color = randomHEX()
							lamp.on()
							lamp.set_color(hexa=color, transition=10)
							time.sleep(int(time_between))
							# info(f"{round((current_loop / int(repeat_times)) * 100)}%")
					except KeyboardInterrupt:
						print()
						ok2("Animation completed.")
						flicker_light(lamp)
						input("Press [ENTER] to go home")
						execute_code = False
					except:
						pass
				else:
					invalid_input = False
		except:
			error("Invalid number")
	elif selected_option == 2:
		# repeat_times = input("How many times to repeat? ")
		time_between = input("How long between each brightness change in seconds? ")
		execute_code = True

		try:
			# int(repeat_times)
			# int(time_between)
			invalid_input = True
			while invalid_input == True:
				# if int(time_between) * int(repeat_times) < 60:
				# 	time_total = f"{round(int(time_between) * int(repeat_times))} second(s)"
				# elif int(time_between) * int(repeat_times) >= 60:
				# 	time_total = f"{round(int(time_between) * int(repeat_times) / 60)} minute(s)"
				# elif int(time_between) * int(repeat_times) / 60 >= 60:
				# 	time_total = f"{round(int(time_between) * int(repeat_times) / 60)} hour(s)"
				input_value = input(
					f"This will take stop when you press ctrl+C. Press [ENTER] to confirm or c to cancel. ").lower()
				if input_value != "c":
					invalid_input = False
					info("Animation started.")
					try:
						while execute_code == True:
							try:
								if(lid_closed() == True):
									print()
									lamp.off(transition=20)
									ok2("Animation completed.")
									input("Press [ENTER] to go home")
									execute_code = False
							except:
								pass
							lamp.set_brightness(round(random.randint(1, 254)))
							time.sleep(int(time_between))
					except KeyboardInterrupt:
						flicker_light(lamp)
						ok2("Animation completed.")
						input("Press [ENTER] to go home")
					except:
						pass
				else:
					invalid_input = False
		except:
			error("Invalid number")

	elif selected_option == 3:
		if ALL == False:
			error("You are unable to use this feature. Please import everything in order to use this.")
		else:
			input_value = input(f"This will only stop after pressing ctrl+C. Press [ENTER] to confirm or c to cancel. ").lower()
			images = []
			old_brightness = lamp.bri
			if old_brightness <= 50:
				old_brightness = 254
			# print(old_brightness)
			# print(lamp.bri)
			execute_code = True
			if input_value != "c":
				while execute_code == True:
					try:
						# If the lid is closed, turn lights off and stop animation
						try:
							if(lid_closed() == True):
								print()
								lamp.off(transition=20)
								ok2("Animation completed.")
								input("Press [ENTER] to go home")
								execute_code = False
						except:
							pass
						# print(len(images))
						# If 3 images collected, do stuff
						if len(images) == 3:
							result = Image.new('RGBA', images[0].size)
							for image in images:
								result = Image.alpha_composite(result, image)
							# ^ combine all images in to one

							colors_rgb = get_colors(result)
							hex_color = rgb_to_hex(colors_rgb[0], colors_rgb[1], colors_rgb[2])
							# ^ getting the most dominant color
							
							# huesdk only accepts 6 character HEX
							hex_list = []
							for letter in hex_color:
								hex_list.append(letter)
							if len(hex_list) == 3:
								hex_color = hex_list[0]+hex_list[0] + hex_list[1]+hex_list[1] + hex_list[2]+hex_list[2]
							# There were occasions with 5 character HEX codes
							if len(hex_color) != 6:
								hex_color = hex_color[0]+hex_color[0]+hex_color[1]+hex_color[1]+hex_color[2]+hex_color[2]

							# Getting how dark the color is and changing lights accordingly
							if how_dark(hex_color) == 1:
								# Extremely dark
								lamp.set_color(hexa="00010a", transition=20)
								lamp.on(transition=1)
								lamp.set_brightness(round(old_brightness / 3), transition=1)
							elif how_dark(hex_color) == 2:
								# Dark
								lamp.set_color(hexa=hex_color, transition=20)
								lamp.on(transition=1)
								lamp.set_brightness(round(old_brightness / 2), transition=1)
							elif how_dark(hex_color) == 3:
								# Medium
								lamp.set_color(hexa=hex_color, transition=20)
								lamp.on(transition=1)
								lamp.set_brightness(round(old_brightness), transition=1)
							elif how_dark(hex_color) == 4:
								# Light
								lamp.set_color(hexa=hex_color, transition=20)
								lamp.on(transition=1)
								lamp.set_brightness(round(old_brightness), transition=1)

							images = []


						try:
							img = pyautogui.screenshot()
							images.append(img.convert("RGBA"))
							time.sleep(1)
						except KeyboardInterrupt:
							print()
							ok2("Animation completed.")
							input("Press [ENTER] to go home")
							execute_code = False
							pass
						# except:
						# 	pass
							# Make screenshot, append to list
						# except Exception as e:
						# 	# In rare occasions, it might produce an error.
						# 	lamp.on(transition=1)
						# 	lamp.set_color(hexa="#FF0000", transition=20)
						# 	print(e)
						# 	time.sleep(1)
					except KeyboardInterrupt:
						# User chose to stop animation
						print()
						ok2("Animation completed.")
						input("Press [ENTER] to go home")
						execute_code = False
						pass
						# flicker_light(lamp)
					# except Exception as e:
					# 	error(e)
					# 	images = []
					# 	# pass		

			else:
				invalid_input = False
	else:
		# User chose to read external .lhad file
		with open(animation_list[selected_option - 4]) as dataFile:
			animation_json = json.load(dataFile)
			# As it uses JSON syntax, we can use json.load()
		try:
			animation_name = animation_json["name"]
			animation_colors = animation_json["colors"]
			# Try if animation is valid
		except KeyError:
			print(f"{colors.FAIL}[{current_item}] Invalid animation file ({f}) {colors.END}")
			return False
			# Invalid file

		# repeat_times = input("How many times repeat?")
		total_time = 0
		current_item = 0
		# V calculating how long it will take
		for value in animation_json["colors"]:
			try:
				total_time += int(animation_json["colors"][current_item]["time_until_next"])
			except KeyError:
				total_time += 5
			current_item += 1
		invalid_input = True
		while invalid_input == True:
			input_value = input(
                            f"This will only stop after pressing ctrl+C. Press [ENTER] to confirm or c to cancel. ").lower()
			if input_value != "c":
				invalid_input = False

				max_lenght = len(animation_json["colors"])
				current_item = 0
				current_number = 1
				execute_code = True
				while execute_code == True:
					if lamp.is_on == False:
						lamp.on()
					try:
						# for _ in range(int(repeat_times)):
						for __ in range(max_lenght):
							# Checking what data is set

							try:
								animation_json["colors"][current_item]["color"]
								from_memory = True
							except KeyError:
								animation_json["colors"][current_item]["color"] = lamp.hue
								from_memory = False
							# ^ If color value is not set, continue with current color

							try:
								animation_json["colors"][current_item]["brightness"]
							except KeyError:
								animation_json["colors"][current_item]["brightness"] = lamp.bri 
							# ^ If brightness value is not set, continue with current brightness
							
							try:
								animation_json["colors"][current_item]["time_until_next"]
							except KeyError:
								animation_json["colors"][current_item]["time_until_next"] = 5
							# ^ If time_until_next value is not set, continue with defualt (5 seconds)


							try:
								# If using default color value
								if from_memory == True:
									lamp.set_color(hexa=animation_json["colors"][current_item]["color"].replace("#", ""))
									# huesdk does not accept the hashtag, removing it here and setting color
								else:
									lamp.set_color(hue=animation_json["colors"][current_item]["color"])
									# Setting color to one previously set

								factor = int(animation_json["colors"][current_item]["brightness"]) / 100
								selected_light.set_brightness(round(factor * 254))
								# Converting from percentage to hard value

								time.sleep(int(animation_json["colors"][current_item]["time_until_next"]))

								current_item += 1
								if current_item == max_lenght:
									current_item = 0
								# If we're at the end of the animation, reset to beginning
							except KeyError:
								pass
						# info(f"{round((current_number / int(repeat_times)) * 100)}%")
						# Printing progress
						current_number += 1
						# Add lid close
					except KeyboardInterrupt:
						# If manually stopped
						print()
						ok2("Animation ended.")
						execute_code = False
						flicker_light(lamp)
						input("Press [ENTER] to go home")
						
			else:
				invalid_input = False

def UpdateCheck():
	log("Checking for latest version...")
	response = requests.get("http://pyplace.dantenl.com/Store%20Files/lovehueversion.json")
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
					f"{colors.INFO}Downloading latest version of LoveHue...{colors.END}")
				log("Retrieving latest version of LoveHue...")
				r = requests.get(
					"http://pyplace.dantenl.com/Store%20Files/lovehue.py", allow_redirects=True)
				if not r.ok:
					print(f"{colors.FAIL}Error:{colors.END} Could not get the LoveHue file! Status code: {r.status_code}")
					return
				log("Updating main LoveHue file")
				open('LoveHue.py', 'wb').write(r.content)
				print(
					f"{colors.OKGREEN}The latest version of LoveHue is now ready in {colors.BOLD}LoveHue.py!{colors.END}")
				NotAnswered2 = True
				while NotAnswered2 == True:
					Answer2 = input("Would you like to run it? (y/n) ")
					Answer2 = Answer2.lower()
					if Answer2 == "y":
						print(
							f"{colors.INFO}Attempting to run LoveHue.py...{colors.END}")
						os.execv(sys.argv[0], sys.argv)
						sys.exit(1)
					elif Answer2 == "n":
						print(
							f"Continuing with current version. {colors.BOLD}NOTE:{colors.END} Next time you start LoveHue.py, it will be on the latest version!")
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
