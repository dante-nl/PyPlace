# 🄱🅈 🄳🄰🄽🅃🄴_🄽🄻

import sys
import random

logo = """                                             
 _______ _______ _______ _______ _______     _______ _______ _______     _______ _______ _______ _______ _______ _______ 
|\     /|\     /|\     /|\     /|\     /|   |\     /|\     /|\     /|   |\     /|\     /|\     /|\     /|\     /|\     /|
| +---+ | +---+ | +---+ | +---+ | +---+ |   | +---+ | +---+ | +---+ |   | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
| |   | | |   | | |   | | |   | | |   | |   | |   | | |   | | |   | |   | |   | | |   | | |   | | |   | | |   | | |   | |
| |G  | | |u  | | |e  | | |s  | | |s  | |   | |t  | | |h  | | |e  | |   | |n  | | |u  | | |m  | | |b  | | |e  | | |r  | |
| +---+ | +---+ | +---+ | +---+ | +---+ |   | +---+ | +---+ | +---+ |   | +---+ | +---+ | +---+ | +---+ | +---+ | +---+ |
|/_____\|/_____\|/_____\|/_____\|/_____\|   |/_____\|/_____\|/_____\|   |/_____\|/_____\|/_____\|/_____\|/_____\|/_____\|                                                                                                                       
"""

print(logo)
print("Welcome to a number guessing game! Here you have to guess a number between 1 and 100.")
def guess_the_number():
	invalid_answer = True
	while invalid_answer == True:
		DIFFICULTY_INPUT = input("What difficulty do you want to play on? (easy/hard) ").lower()
		if DIFFICULTY_INPUT == "easy":
			lives = 10
			invalid_answer = False
		elif DIFFICULTY_INPUT == "hard":
			lives = 5
			invalid_answer = False
		elif DIFFICULTY_INPUT == "impossible":
			lives = 2
			invalid_answer = False
		else:
			print("I'm not sure what you mean with that!")
			
	
	CORRECT_NUMBER = random.randint(1, 100)
	
	def correct_number(number, lives):
		"""Returns if the number is correct, and checks if the user ran out of lives too or won."""
		if lives == 1:
			print(f"You have run out of lives! The correct number was {CORRECT_NUMBER}")
			return "lost"
		elif number > CORRECT_NUMBER:
			print("Too high!")
			return
		elif number < CORRECT_NUMBER:
			print("Too low!")
			return
		elif number == CORRECT_NUMBER:
			print(f"You won! The correct number was {CORRECT_NUMBER}")
			return "won"
	
	game_over = False
	while game_over == False:
		try:
			if lives == 1:
				print(f"You have {lives} live")
			else:
				print(f"You have {lives} lives")
			number = int(input("Guess a number: "))
			game = correct_number(number, lives)
			if game == "won" or game == "lost":
				game_over = True
				answer = "invalid"
				while answer == "invalid":
					play_again = input("Do you want to play again? (y/n) ").lower()
					if play_again == "y":
						guess_the_number()
					elif play_again == "n":
						print("Bye!")
						print()
						sys.exit(0)
					else:
						print(f"I'm not sure what you mean with {play_again}")
			else:
				lives -= 1
				
		except ValueError:
			print("That does not appear to be a valid number!")

guess_the_number()
