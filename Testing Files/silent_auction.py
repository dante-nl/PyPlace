import os
import sa_art

clear = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

print(sa_art.logo)

bid_dict = {}

RunAgain = True
while RunAgain == True:
	Name = input("What is your name? ")
	Bid = int(input("How much do you want to bid? €"))
	bid_dict[Name] = {"Bid": Bid}

	InvalidInput = True
	while InvalidInput == True:
		RunAgainInput = input("Are there any other bidders? (y/n) ")
		if RunAgainInput == "y":
			InvalidInput = False
			clear()
		elif RunAgainInput == "n":
			InvalidInput = False
			RunAgain = False

HeighestBid = 0
HeighestBidder = None
for item in bid_dict:
	if bid_dict[item]["Bid"] > HeighestBid:
		HeighestBid = bid_dict[item]["Bid"]
		HeighestBidder = item

print(f"The heighest bidder is {HeighestBidder} with €{HeighestBid}!")
