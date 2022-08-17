import higher_lower_accounts
import higher_lower_art
import random
import os

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

def get_person(first_person = None):
	global person_a
	global person_b
	if first_person == None:
		person_a = random.sample(higher_lower_accounts.data, 1)[0]
	else:
		person_a = first_person
	print(f"{bcolors.BOLD}A:{bcolors.END} {person_a['name']}, {person_a['description']} from {person_a['country']}")
	
	print(higher_lower_art.vs)
	
	person_b = random.sample(higher_lower_accounts.data, 1)[0]
	print(f"{bcolors.BOLD}B:{bcolors.END} {person_b['name']}, {person_b['description']} from {person_b['country']}")
	
	print()

clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

score = 0

clear()
print(higher_lower_art.logo)
get_person()

game_ended = False
while game_ended == False:
	user_input = input(f"Who has more followers? Person A ({person_a['name']}) or B ({person_b['name']})? (a/b) ").lower()
	if user_input == "a":
		if person_a["follower_count"] > person_b["follower_count"]:
			score += 1
			clear()
			print(higher_lower_art.logo)
			print(f"{bcolors.OKGREEN}Correct!{bcolors.END}")
			get_person(person_b)
		elif person_a["follower_count"] < person_b["follower_count"]:
			clear()
			print(higher_lower_art.logo)
			print(f"{bcolors.FAIL}Incorrect, your final score was {score} {bcolors.END}")
			game_ended = True
		elif person_a["follower_count"] == person_b["follower_count"]:
			clear()
			print(higher_lower_art.logo)
			print(f"{bcolors.INFO}Both accounts have equal followers!{bcolors.END}")
			get_person(person_b)
	elif user_input == "b":
		if person_b["follower_count"] > person_a["follower_count"]:
			score += 1
			clear()
			print(higher_lower_art.logo)
			print(f"{bcolors.OKGREEN}Correct!{bcolors.END}")
			get_person(person_b)
		elif person_b["follower_count"] < person_a["follower_count"]:
			clear()
			print(higher_lower_art.logo)
			print(f"{bcolors.FAIL}Incorrect, your final score was {score} {bcolors.END}")
			game_ended = True
		elif person_b["follower_count"] == person_a["follower_count"]:
			clear()
			print(higher_lower_art.logo)
			print(f"{bcolors.INFO}Both accounts have equal followers!{bcolors.END}")
			get_person(person_b)
