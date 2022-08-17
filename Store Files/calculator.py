import sys

logo = """
 _____________________
|  _________________  |
| |	         0. | |  .----------------.  .----------------.  .----------------.  .----------------. 
| |_________________| | | .--------------. || .--------------. || .--------------. || .--------------. |
|  ___ ___ ___   ___  | | |     ______   | || |      __      | || |   _____      | || |     ______   | |
| | 7 | 8 | 9 | | + | | | |   .' ___  |  | || |     /  \     | || |  |_   _|     | || |   .' ___  |  | |
| |___|___|___| |___| | | |  / .'   \_|  | || |    / /\ \    | || |    | |       | || |  / .'   \_|  | |
| | 4 | 5 | 6 | | - | | | |  | |         | || |   / ____ \   | || |    | |   _   | || |  | |         | |
| |___|___|___| |___| | | |  \ `.___.'\  | || | _/ /    \ \_ | || |   _| |__/ |  | || |  \ `.___.'\  | |
| | 1 | 2 | 3 | | x | | | |   `._____.'  | || ||____|  |____|| || |  |________|  | || |   `._____.'  | |
| |___|___|___| |___| | | |              | || |              | || |              | || |              | |
| | . | 0 | = | | / | | | '--------------' || '--------------' || '--------------' || '--------------' |
| |___|___|___| |___| |  '----------------'  '----------------'  '----------------'  '----------------' 
|_____________________|
"""


def add(n1, n2):
	return n1 + n2

def subtract(n1, n2):
	return n1 - n2

def multiply(n1, n2):
	return n1 * n2

def divide(n1, n2):
	return n1 / n2

operators = {
	"+": add, 
	"-": subtract, 
	"*": multiply, 
	"/": divide
}

print(logo)
def calculator():
	num1 = float(input("What is the first number? "))
	for operator in operators:
		print(operator)
	
	should_continue = True
	while should_continue == True:
		
		operator = input("Pick an operation: ")
		
		num2 = float(input("What is the next number? "))
		
		result = operators[operator](num1, num2)
		print(f"{num1} {operator} {num2} = {result}")

		InvalidAnswer = True
		while InvalidAnswer == True:
			continue_ = input(f"Continue calculating with {result}? (y/n) ")
			if continue_ == "y":
				num1 = result
				InvalidAnswer = False
			elif continue_ == "n":
				SecondInvalidAnswer = True
				while SecondInvalidAnswer == True:
					exit = input("Do you want to exit the program? (y/n) ")
					if exit.lower() == "y":
						InvalidAnswer = False
						SecondInvalidAnswer = False
						print("Bye!")
						sys.exit(0)
					elif exit.lower() == "n":	
						should_continue = False
						InvalidAnswer = False
						SecondInvalidAnswer = False
						print()
						calculator()
					else:
						print(f"I'm not sure what you mean with {exit}")
			else:
				print(f"I'm not sure what you mean with {continue_}")

calculator()
		
