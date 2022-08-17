word_dict = {}

exit_program = False
while exit_program == False:
	word = input("Enter the word (-e to exit): ")
	if word.lower() == "-e":
		exit_program = True
	else:
		definition = input(f"Enter the definition of \"{word}\": ")
		word_dict[word] = definition

print("\n")
for word in word_dict:
	print(f"{word}<>{word_dict[word]}")

print("\n")
print("You can copy the words from above in to the \"Import from Google Docs, Excel, etc.\" in a Quizlet set.")
print("Make sure that words and definitions are seperated with \"<>\" and cards are sperated with a new line.")
