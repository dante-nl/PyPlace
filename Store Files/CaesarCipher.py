import re
import CaesarCipher_art

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def caesar(start_text, shift_amount, cipher_direction):
	end_text = ""
	if cipher_direction == "decode":
		shift_amount *= -1
	for char in start_text:
		RegEx = re.search("[A-z]", char)
		if RegEx:
			position = alphabet.index(char)
			new_position = position + shift_amount
			end_text += alphabet[new_position]
		else:
			end_text += char
    
	print(f"Here's the {cipher_direction}d result: {end_text}")

print(CaesarCipher_art.logo)
LoopProgram = True
while LoopProgram == True:
	direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n")
	text = input("Type your message:\n").lower()
	shift = int(input("Type the shift number:\n"))

	if shift > 26:
		shift = shift % 26

	caesar(start_text=text, shift_amount=shift, cipher_direction=direction)
	RunAgain = input("Do you want to run it again? (y/n) ")
	if RunAgain == "y":
		LoopProgram = True
	elif RunAgain == "n":
		print("Bye!")
		LoopProgram = False
	else:
		print(f"I'm not sure what you mean with \"{RunAgain}\"! I'm just guessing you want to run it again :D")
		LoopProgram = True
