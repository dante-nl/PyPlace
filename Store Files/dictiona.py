
# ██████╗░██╗░█████╗░████████╗██╗░█████╗░███╗░░██╗░█████╗░░░░██████╗░██╗░░░██╗
# ██╔══██╗██║██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║██╔══██╗░░░██╔══██╗╚██╗░██╔╝
# ██║░░██║██║██║░░╚═╝░░░██║░░░██║██║░░██║██╔██╗██║███████║░░░██████╔╝░╚████╔╝░
# ██║░░██║██║██║░░██╗░░░██║░░░██║██║░░██║██║╚████║██╔══██║░░░██╔═══╝░░░╚██╔╝░░
# ██████╔╝██║╚█████╔╝░░░██║░░░██║╚█████╔╝██║░╚███║██║░░██║██╗██║░░░░░░░░██║░░░
# ╚═════╝░╚═╝░╚════╝░░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝╚═╝░░░░░░░░╚═╝░░░

# 🄱🅈 🄳🄰🄽🅃🄴_🄽🄻

# Welcome to dictiona.py! This is a simple
# Python script that tries to get the
# definition of a word and some examples
# for the word using the
# Merriam-Webster API.

import json
import sys
import urllib.request
import re


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

key = "55b752f3-d7ef-414e-8d35-8ce6d4dcb6d5"

RunScript = True
while RunScript == True:

	query = input("Enter word: ")
	query = query.replace(" ", "%20")

	urlfrmt = "https://dictionaryapi.com/api/v3/references/collegiate/json/"+query+"?key=" + key
	response = urllib.request.urlopen(urlfrmt)
	WordJSON = json.load(response)
	SearchForExamples = True
	print(f"{bcolors.BOLD}DEFINITION:{bcolors.END} \n")
	try:
		for meaning in WordJSON:
			definitions = meaning['shortdef']
			if meaning['meta']['id'] != query:
				print("\n"+meaning['meta']['id'])
			try:
				print('('+meaning['fl']+')')
				for i, eachDef in enumerate(definitions, 1):
					print(str(i) + ". " + eachDef)
			except KeyError:
				pass
	except:
		print(f"{bcolors.FAIL}Error:{bcolors.END} Could not find that word.")
		SearchForExamples = False

	if SearchForExamples == True:
		print(f"{bcolors.BOLD}EXAMPLES:{bcolors.END} \n")
		examples = 0
		for usage in WordJSON:
			try:
				longdefs = usage['def']
				for i, eachDef in enumerate(longdefs, 1):
					if 'sseq' in eachDef:
						for ill in eachDef['sseq']:
							if 'dt' in ill[0][1]:
								for illus in ill[0][1]['dt']:
									if illus[0] == 'vis':
										for ii in range(1, len(illus)):
											L = len(illus[ii])
											for jj in range(L):
												if 't' in illus[ii][jj]:
													examples += 1
													str = re.sub('\{(.*?)\}', '', illus[ii][jj]['t'])
													print(f"* {str}")
			except KeyError:
				pass
		if examples == 0:
			print(f"{bcolors.FAIL}Error:{bcolors.END} There are no examples available for this word.")

	InvalidAnswer = True
	while InvalidAnswer == True:
		RunAgain = input("Do you want to see the definition of another word? (y/n) ")
		if RunAgain.lower() == "y":
			InvalidAnswer = False
		elif RunAgain.lower() == "n":
			InvalidAnswer = False
			RunAgain = False
			sys.exit(0)
		else:
			print(f"{bcolors.FAIL}Error: {bcolors.END}I'm not sure what you mean with {RunAgain}")
