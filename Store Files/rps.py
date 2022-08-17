import random

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

# Setting up
print("Welcome to rock, paper, scissors!")
selection = int(input("What do you choose? 1 for rock, 2 paper or 3 for scissors.\n"))

# Randomizing
random_computer = random.randint(1, 3)

# Iffing (to do if stuff)
if selection == 1:
	print(f"You chose: {rock}")
elif selection == 2:
	print(f"You chose: {paper}")
elif selection == 3:
	print(f"You chose: {scissors}")
else:
	selection = random.randint(1, 3)
	if selection == 1:
		print(f"You chose nothing, so I chose for you! You have to deal with: {rock}")
	elif selection == 2:
		print(f"You chose nothing, so I chose for you! You have to deal with: {paper}")
	elif selection == 3:
		print(f"You chose nothing, so I chose for you! You have to deal with: {scissors}")

if random_computer == selection:
	if random_computer == 1:
		print(f"The computer has: {rock}")
	elif random_computer == 2:
		print(f"The computer has: {paper}")
	elif random_computer == 3:
		print(f"The computer has: {scissors}")
	else:
		print("The computer has a option that is not rock, paper or scissors?")
	print("That's a tie :/")
elif random_computer == 1 and selection == 2:
	print(f"The computer has: {rock}")
	print("You won! :D")
elif random_computer == 1 and selection == 3:
	print(f"The computer has: {rock}")
	print("You lost... D:")
elif random_computer == 2 and selection == 1:
	print(f"The computer has: {paper}")
	print("You lost... D:")
elif random_computer == 2 and selection == 3:
	print(f"The computer has: {paper}")
	print("You won! :D")
elif random_computer == 3 and selection == 1:
	print(f"The computer has: {scissors}")
	print("You won! :D")
elif random_computer == 3 and selection == 2:
	print(f"The computer has: {scissors}")
	print("You lost... D:")
else:
	print("Hmmm, this is not supposed to happen...")
