#################################################################################
#################################################################################
## ██████╗░░█████╗░░██╗░░░░░░░██╗███████╗██████╗░██████╗░██╗███╗░░██╗░██████╗░ ##
## ██╔══██╗██╔══██╗░██║░░██╗░░██║██╔════╝██╔══██╗██╔══██╗██║████╗░██║██╔════╝░ ##
## ██████╔╝██║░░██║░╚██╗████╗██╔╝█████╗░░██████╔╝██████╔╝██║██╔██╗██║██║░░██╗░ ##
## ██╔═══╝░██║░░██║░░████╔═████║░██╔══╝░░██╔══██╗██╔═══╝░██║██║╚████║██║░░╚██╗ ##
## ██║░░░░░╚█████╔╝░░╚██╔╝░╚██╔╝░███████╗██║░░██║██║░░░░░██║██║░╚███║╚██████╔╝ ##
## ╚═╝░░░░░░╚════╝░░░░╚═╝░░░╚═╝░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░░╚══╝░╚═════╝░ ##
#################################################################################
#################################################################################
# © 2023-present — dante_nl

# PowerPing is a simple Python project that pings a website for you and once you
# press control+c, it will generate an HTML file with the data of your ping requests.

# ————————————————————————————
# Below you can change some more advanced settings that the average user should not
# need to change.

# 𝗖𝗵𝗲𝗰𝗸 𝗳𝗼𝗿 𝘂𝗽𝗱𝗮𝘁𝗲𝘀
# Default: True
# Options: True, False | Boolean
# Disable the update checking feature.
import platform
import socket
import struct
UPDATE_CHECK = False

# 𝗩𝗲𝗿𝘀𝗶𝗼𝗻
# Default: 1.0
# Options: Any floating point number
# Set the current version. This is used for checking for updates.
VERSION = 1.0

# 𝗟𝗼𝗴𝗴𝗶𝗻𝗴
# Default: False
# Options: True, False | Boolean
# Enable logging, pretty much everything noteworthy for debugging is told here,
#    this includes, but is not limited to file changed and web requests.
LOGGING = True

# ————————————————————————————
# Below here the code is found, feel free to edit it! I have tried to add comments
# where they might be neccesary but knowing me they're probably not everywhere where
# needed.
from datetime import datetime
from urllib.parse import urljoin
import io
import os
import re
import sys
import time
import base64
import string
import random
import asyncio
import requests
import webbrowser
try:
	import matplotlib.pyplot as plt
except ModuleNotFoundError:
	print("Please install this: pip install matplotlib")
	sys.exit(0)


def current_ms():
	"""Returns an integer with the current time in miliseconds"""
	return round(time.time() * 1000)


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
# Color values. Some devices may not show these properly
# TODO: Add settings page to disable these


def log(text):
	"""Sends a log message. Usage:
	```py
	log("Hello!")
	```"""
	if LOGGING == True:
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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))


def checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    countTo = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if (source_string[count + 1]):
            hiByte = source_string[count + 1]
        if (source_string[count]):
            loByte = source_string[count]
        sum = sum + (hiByte * 256 + loByte)
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string):  # Check for odd length
        loByte = source_string[len(source_string) - 1]
        sum += loByte

    sum &= 0xffffffff  # Truncate sum to 32 bits (a variance from ping.c, which
    # uses signed ints, but overflow is unlikely in ping)

    sum = (sum >> 16) + (sum & 0xffff)  # Add high 16 bits to low 16 bits
    sum += (sum >> 16)  # Add carry from above (if any)
    answer = ~sum & 0xffff  # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer


async def ping(host, timeout=5):
	"""
	Returns True is the request was successful, the delay and if it tried to get the headers
	
	Table for reference:

	| Response                                         	| Success 	| Delay 	| Using headers? 	| Return code 	|
	|--------------------------------------------------	|---------	|-------	|----------------	|-------------	|
	| ICMP request was successful, took 20ms           	| True    	| 20    	| False          	| None        	|
	| Headers request was successful, took 200ms       	| True    	| 200   	| True           	| 200         	|
	| ICMP request failed                              	| False   	| 0     	| False          	| None        	|
	| Headers request failed                           	| False   	| 0     	| True           	| None        	|
	| Headers request: page does not exist, took 200ms 	| True    	| 200   	| True           	| 404         	|
	"""

	if os.geteuid() != 0 or platform.system() == "Windows":
		# print("Error: Root permission is required to send an ICMP ping request.")
		try:
			delay, code = await alt_ping(host)
			return True, delay, True, code
		except:
			return False, 0, True, None
	try:
		# Create a raw socket
		s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
		s.settimeout(timeout)

		# Send the ping request
		send_time = time.time()
		id = os.getpid() & 0xFFFF
		data = b'abcdefghijklmnopqrstuvwabcdefghi'
		packet = struct.pack(
			'!BBHHH32s', 8, 0, 0, id, 1, data
		)
		checksum_val = checksum(packet)
		packet = struct.pack(
			'!BBHHH32s', 8, 0, checksum_val, id, 1, data
		)
		try:
			s.sendto(packet, (host.replace("https://", "").replace("http://", ""), 1))
		except:
			s.sendto(packet, (host.replace("https://", "").replace("http://", "").replace("tls://", "").replace("tcp://"), 1))

		# Wait for the response
		recv_time, _ = s.recvfrom(1024)
		recv_time = time.time()

		# Calculate the round trip time
		rtt = recv_time - send_time

		# Close the socket
		s.close()

		return True, round(rtt*100), False, None
	except socket.timeout:
		try:
			delay, code = await alt_ping(host)
			return True, round(delay), True, code
		except:
			return False, 0, True, None




def makeHTML(name, graph, data, average, headers_used):
	"""Inputs:
	`name`: The file name
	`graph`: The base64 version of the graph
	`data`: The data list with dictionaries
	`average`: The average delay
	`headers_used`: If any request was made using HEAD"""
	ping_html = ""
	requests_total = 0
	requests_success = 0
	for entrance in data:
		requests_total += 1
		try:
			if (entrance["code"] // 100) * 100 == 100:
				response_class = "info"
			elif (entrance["code"] // 100) * 100 == 200:
				response_class = "success"
				requests_success += 1
			elif (entrance["code"] // 100) * 100 == 300:
				response_class = "info"
			elif (entrance["code"] // 100) * 100 == 400:
				response_class = "error"
			elif (entrance["code"] // 100) * 100 == 500:
				response_class = "error"
			else:
				response_class = "warning"
		except:
			response_class = "warning"

		if headers_used == True:
			ping_html += f"""
				<div class="ping">
					<p><b>Response:</b> <span class="{response_class}">{entrance["code"]}</span></p>
					<p><b>Delay:</b> {entrance["delay"]}ms</p>
					<p><b>Request made:</b> {entrance["request_time"]}</p>
				</div>
			"""
		else:
			ping_html += f"""
				<div class="ping">
					<p><b>Delay:</b> {entrance["delay"]}ms</p>
					<p><b>Request made:</b> {entrance["request_time"]}</p>
				</div>
			""" 	

	if headers_used == True:
		title = "Results for requesting headers"
		desc = "and are generated by taking the time it took for the headers to be loaded."
		invidual_explanation = "If it says None, this means the request was made using ICMP instead. This is by default the preffered way."
	else:
		title = "Results for pinging"
		desc = "and are generated by taking the time it took for the server to respond to an ICMP request."
		invidual_explanation = ""

	html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>PowerPing Results</title>
	<style>
		body {{
				font-family: Arial, Helvetica, sans-serif;
				margin: 0 1% 0 1%;
			}}

		h1 {{
			color: #6DB1BF
		}}


		.ping {{
			margin: 0 0 5px 0;
			border: 1px solid #6DB1BF;
			border-radius: 10px;
		}}

		.info {{
			padding: 2px 4px;
			background-color: #1F68AD;
			color: white;
			border-radius: 10px;
		}}
		
		.success {{
			padding: 2px 4px;
			background-color: #8FF7A7;
			color: black;
			border-radius: 10px;
		}}
		
		.error {{
			padding: 2px 4px;
			background-color: #F71735;
			color: white;
			border-radius: 10px;
		}}
		
		.warning {{
			padding: 2px 4px;
			background-color: #FFD400;
			color: black;
			border-radius: 10px;
		}}

		.ping {{
			margin: 0 0 5px 0;
			border: 1px solid #6DB1BF;
			border-radius: 10px;
		}}

		img {{
			border-radius: 10px;
			display: block;
			margin-left: auto;
			margin-right: auto;
			width: 50%;
		}}

		@media (prefers-color-scheme: dark) {{
			body {{
				background-color: #1a1a1a;
				color: #fff
			}}
		}}

	</style>
</head>
<body>
	<h1>{title}</h1>
	<h2>Generated on {datetime.now().strftime("%e %B, %Y at %H:%M")}</h2>
	<p>Delay times are shown in milliseconds {desc}</p>
	<p>Generated using PowerPing</p>
	<hr>
	
	<p>The average time was <b>{round(average)}ms</b>.</p>
	<img src="data:image/png;base64,{graph}" alt="Uptime graph" />

	<hr>
	<h2>Individual ping requests</h2>
	<p>{invidual_explanation}</p>
	{ping_html}
</body>
</html>
	"""


	filename = name+".html"

	# Check if the file already exists
	if not os.path.exists(filename):
		# Write the HTML content to a file
		with open(filename, 'w') as f:
			f.write(html_content)
		try:
			webbrowser.open('file://' + os.path.realpath(filename))
		except:
			error(f"Could not open file. You might be able to open {filename} yourself.")
	else:
		with open(filename+id_generator(6), 'w') as f:
			f.write(html_content)
		try:
			webbrowser.open('file://' + os.path.realpath(filename))
		except:
			error(f"Could not open file. You might be able to open the file yourself.")


async def alt_ping(url):
	"""Returns a dictionary with the amount of miliseconds it took for the server to respond and the status of the page.

	Usage:
	```py
	x = await ping(url="https://google.com")
	# url is the first argument
	print(x)
	# Will return something like following dictionaries:
	```

	Example with success:
	```json
	{
	  "code": 200,
	  "time": 23
	} 
	``` 
	Example with non-existent page:
	```json
	{
	  "code": 404,
	  "time": 23
	}
	```
	Example with invalid domain:
	```json
	{
		"code": 0,
		"time": 0
	}
	``` """

	time_1 = current_ms()
	# Get current time in ms
	try:
		r = requests.head(url)
		# Try to reach the page with a HEAD request
	except Exception as e:
		error(e)
		return {
			"code": 0,
			"time": 0,
			"message": e
		}
		# Could not make the request for some reason, also return error message
	difference = current_ms()-time_1
	# Get how long the request took in ms

	result = {
		"code": r.status_code,
		"time": difference,
		"message": "success"
	}
	return difference, r.status_code
	# Wrap it in a dictionary and return it


async def main():
	print("Welcome!")
	if platform.system() == "Windows":
		print("It seems like you are running this on Windows. For the best experience, please use a Linux device or macOS device")
	if os.geteuid() != 0:
		print("It appears that you are not running this as an administrator, please type \"sudo\" in fron of your Python command to use all features")
	url = input("Please enter a URL or IP to ping: ")
	if not url.startswith('http://') and not url.startswith('https://') and not url.startswith('tcp://') and not url.startswith('tls://'):
		url = 'http://' + url
	# Making sure it always has http:// or https://

	if re.search("""(?i)\\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""", url):
		run_loop = True
		# Valid domain name
	elif re.search("""((^\s*((([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]))\s*$)|(^\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?\s*$))""", url):
		run_loop = True
		# Valid IP addres (IPv4 or IPv6)
	else:
		error("Invalid URL or IP address")
		sys.exit(0)
		# Invalid all
	successful_codes = 0
	delays = []
	times = []
	data = []
	info("Pinging website! Press ctrl+C to get the results.")
	headers_used = False
	while run_loop == True:
		try:
			# return_value = await ping(url)
			success, rtt, headers, code = await ping(url)

			if success == True:
			# if return_value["code"] != 0:
				now = datetime.now()
				# dd/mm/YY H:M:S
				times.append(now.strftime("%H:%M:%S"))

				successful_codes += 1
				delays.append(rtt)
				if headers == True:
					print(f"""{colors.OKGREEN}PING SUCCESSFUL{colors.END} (using headers)
Response code: {code}
Time for loading headers: {rtt}ms""")
					data.append({
						"code": code,
						"delay": rtt,
						"request_time": now.strftime("%H:%M:%S")
					})
					headers_used = True
				else: 
					print(f"""{colors.OKGREEN}PING SUCCESSFUL{colors.END}
Round trip time: {rtt}ms""")
					data.append({
						"code": None,
						"delay": rtt,
						"request_time": now.strftime("%H:%M:%S")
					})
			else:
				# error(f"URL responded with code {return_value['code']}")
				#error(f"URL responded with error")

				print(f"""{colors.FAIL}PING FAILED{colors.END}
Round trip time: {rtt}ms""")
				data.append({
					"code": 502,
					"delay": 0,
					"request_time": datetime.now().strftime("%H:%M:%S")
				})
			time.sleep(1.5)
		except KeyboardInterrupt:
			print()
			print(f"{colors.OKCYAN}PING COMPLETED{colors.END}")
			# Calculating average ping
			average = 0
			for number in delays:
				average += number
			average = average / len(delays)

			# Calculating how many percent of the requests returned 200
			requests_total = 0
			requests_success = 0
			for entrance in data:
				requests_total += 1
				try:
					if (entrance["code"] // 100) * 100 == 200:
						# ^ formula rounds down to nearest 100, e.g. 279 is 200, 503 is 500.
						requests_success += 1
				except:
					pass
			if headers_used == True:
				print(f"The average delay was {colors.BOLD}{round(average)}ms{colors.END} and {colors.BOLD}{round((requests_success/requests_total)*100)}%{colors.END} of the requests were 200.")
			else:
				print(f"The average delay was {colors.BOLD}{round(average)}ms{colors.END}.")

			print("You can find more information, including a graph in the HTML file. The graph is also available as a standalone image file.")

			run_loop = False

			hours = []

			for time_ in times:
				time_array = time_.split(":")
				hours.append(time_array[0])

			for hour in hours:
				if hour != datetime.now().strftime("%H"):
					all_same_hour = False
				else:
					all_same_hour = True

			times_shown = ["null"]
			if all_same_hour == True:
				first_time = None
				for time_ in times:
					time_array = time_.split(":")
					if first_time == None:
						times_shown[0] = f"{time_array[0]}:{time_array[1]}.{time_array[2]}"
						first_time = True
					else:
						times_shown.append(":"+time_array[1]+"."+time_array[2])
			else:
				times_shown = times

			x = times_shown
			y = delays

			# Generate basic grid
			plt.plot(x, y, color="#6DB1BF", marker="o")

			# Automatically decide size
			plt.autoscale(enable=True, tight=False)

			# Setting labels for X and Y
			plt.xlabel("Time")
			plt.ylabel("Delay in ms")

			# Adding a title
			if headers_used == True:
				plt.title(f"Results for getting headers of {url}")
			else:
				plt.title(f"Results for pinging {url}")

			# Adding a sublte grid to the background
			plt.grid(True, linestyle='-', color='gray', alpha=0.5)

			# plt.xticks(x[::5])
			# plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
			# plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))
			plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
			# Automatically showing the right amount of values


			time_formatted = datetime.now().strftime("%H:%M.%S")
			plt.savefig(f"ping-results-{time_formatted}.png", bbox_inches='tight')
			# Save the plot to a buffer
			buf = io.BytesIO()
			plt.savefig(buf, format='png')
			buf.seek(0)

			# Encode the plot as a base64 string
			plot_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')

			# Get the base URL (e.g. https://example.com/page/page2?a=b&c=d --> example.com)
			# clean_url = os.path.dirname(url).replace("https://", "").replace("http://", "")
			clean_url = urljoin(url, ".").replace("https://", "").replace("http://", "").replace("/", "-")
			makeHTML(clean_url+id_generator(3), plot_base64, data, average, headers_used)
			#// plt.show()
asyncio.run(main())
