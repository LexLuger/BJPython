#module cards
#the base classes for card game
class Card(object):
	"""One play card"""
	
	RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
	SUITS = ["c", "d", "h", "s"]
	
	def __init__(self, rank, suit, face_up = True):
		self.rank = rank
		self.suit = suit
		self.is_face_up = face_up
	
	def __str__(self):
		if self.is_face_up:
			rep = self.rank + self.suit
		else:
			rep = "XX"
		return rep
		
	def flip(self):
		"""Turn over the card"""
		self.is_face_up = not self.is_face_up

class Hand(object):
	"""Hand for one player"""
	
	def __init__(self):
		self.cards = []

	def __str__(self):
		if self.cards:
			rep = ""
			for card in self.cards:
				rep += str(card) + "\t"
		else:
			rep = "<empty>"
		return rep

	def clear(self):
		self.cards = []

	def add(self, card):
		self.cards.append(card)

	def give(self, card, other_hand):
		self.cards.remove(card)
		other_hand.add(card)

class Deck(Hand):
	"""The cards deck"""

	def populate(self):
		for suit in Card.SUITS:
			for rank in Card.RANKS:
				self.add(Card(rank, suit))

	def shuffle(self):
		import random
		random.shuffle(self.cards)

	def deal(self, hands, per_hand = 1):
		for rounds in range(per_hand):
			for hand in hands:
				if self.cards:
					top_card = self.cards[0]
					self.give(top_card, hand)
				else:
					print("I can't give more. \nWe run of cards.")

if __name__ == "__main__":
	print("This is a module with classes for card games.")
	input("Press Enter for exit.")