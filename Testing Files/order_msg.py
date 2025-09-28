import sys
import json
import requests


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

code = input("What is the code of the Order? ")

response = requests.get(f"https://pyplace.dantenl.com/orders/{code}/manifest.json")
if response.status_code == 404:
	print(f"{bcolors.FAIL}Error:{bcolors.END} That order does not exist.")
	sys.exit(1)
if response.status_code != 200:
	print(f"{bcolors.FAIL}Error:{bcolors.END} Could not look that order up! Response code: {response.status_code}")
	sys.exit(1)

RequestText = response.text
data = json.loads(RequestText)

try:
	data["name"]
except KeyError:
	print(f"{bcolors.FAIL}Error:{bcolors.END} Invalid order. (name is not set)")
	sys.exit(1)
try:
	data["description"]
except KeyError:
	print(f"{bcolors.FAIL}Error:{bcolors.END} Invalid order. (description is not set)")
	sys.exit(1)
try:
	data["type"]
except KeyError:
	print(f"{bcolors.FAIL}Error:{bcolors.END} Invalid order. (type is not set)")
	sys.exit(1)
try:
	data["min-version"]
except KeyError:
	print(f"{bcolors.FAIL}Error:{bcolors.END} Invalid order. (version is not set)")
	sys.exit(1)
try:
	data["downloads"][0]
except KeyError:
	print(f"{bcolors.FAIL}Error:{bcolors.END} Invalid order. (downloads is not set)")
	sys.exit(1)
try:
	if data["expired"] == True:
		print(f"{bcolors.FAIL}Error:{bcolors.END} This order is no longer valid.")
		sys.exit(1)
except KeyError:
	pass

print(f"""The Order's Discord message should be:
**{data["name"]}**
{data["description"]}
```Min version: {data["min-version"]}
Type: {data["type"]}
```
Enter `-install {code}` on your PyPlace home screen to install it.
""")
