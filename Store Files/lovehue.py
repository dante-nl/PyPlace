	
#// import keyboard
#// ^ pip install keyboard
import time
import sys
import json
from os.path import exists
import os
import random

print()
print()
print()

try:
	from huesdk import Hue
	#* ^ pip install huesdk
except:
	print("Error: Please download huesdk first. You can do this by doing: pip install huesdk --upgrade")
	sys.exit(0)


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



HUE_IP = "192.168.1.111"

if exists("data.json"):
	with open('data.json') as dataFile:
		data = json.load(dataFile)
		USERNAME = data["username"]
		if type(USERNAME) != str:
			error("Could not find username")
			sys.exit(0)
else:
	try:
		USERNAME = Hue.connect(bridge_ip=HUE_IP)
	except:
		info("Please press the link button and run LoveHue again.")
		sys.exit(0)

	data_dict = {}
	data_dict["username"] = USERNAME

	data_dict_str = json.dumps(data_dict, indent=4, separators=(',', ': '))
	with open('data.json', 'w') as dataJSON:
		dataJSON.write(data_dict_str)
		# log("File created: setup.json")

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
	files = [f for f in os.listdir('.') if os.path.isfile(f)]
	current_item = 2
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

	else:
		# print(animation_list[selected_option - 2])
		with open(animation_list[selected_option - 3]) as dataFile:
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

				current_item = 0
				current_number = 1
				max_lenght = len(animation_json["colors"]) - 1
				if lamp.is_on == False:
					lamp.on()
				for _ in range(int(repeat_times)):
					for __ in range(max_lenght):
						try:
							animation_json["colors"][current_item]["color"]
						except KeyError:
							animation_json["colors"][current_item]["color"] = lamp.color
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
							lamp.set_color(hexa=animation_json["colors"][current_item]["color"].replace("#", ""))
							# if animation_json["colors"][current_item]["brightness"]:
							factor = int(animation_json["colors"][current_item]["brightness"]) / 100
							selected_light.set_brightness(round(factor * 254))
							# if animation_json["colors"][current_item]["time_until_next"]:
							time.sleep(int(animation_json["colors"][current_item]["time_until_next"]))
							# print(current_item)
							if current_item == max_lenght:
								current_item = -1
							current_item += 1
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
	elif option == "e":
		sys.exit(0)
