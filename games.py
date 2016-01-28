#Games
#My first module
class Player(object):
	"""a player"""

	def __init__(self, name, score = 0):
		self.name = name
		self.score = score
	
	def __str__(self):
		rep = self.name + ":\t" + str(self.score)
		return rep

def ask_yes_no(question):
	"""Ask question yes or no"""

	response = None
	while response not in ("y", "n"):
		try:
			response = input(question).lower()
		except (ValueError):
			print("Incorrect input.")
	return response

def ask_number(question, low, high):
	"""Ask to input a number from consider range"""

	response = None
	while response not in range(low, high):
		try:
			response = int(input(question))
		except (ValueError):
			print("incorrect input.")
	return response

if __name__ == "__main__":
	print("You have run the module directly, module has not been called.")
	input("\n\nPress Enter for exit.")