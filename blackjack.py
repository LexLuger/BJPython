#Blackjack
#1-7 players against dealer
import cards, games, random

class BJ_Card(cards.Card):
	"""Card for blackjack play"""

	ACE_VALUE = 1
	
	@property
	def value(self):
		if self.is_face_up:
			v = BJ_Card.RANKS.index(self.rank) + 1
			if v > 10:
				v = 10
		else:
			v = None
		return v

class BJ_Deck(cards.Deck):
	"""Deck for blackjack"""
	
	def populate(self):
		for suit in BJ_Card.SUITS:
			for rank in BJ_Card.RANKS:
				self.cards.append(BJ_Card(rank, suit))

	def clear(self):
		self.cards == []

	def check(self):
		self.deck = len(self.cards)
		if self.deck != 52:
			return False
		else:
			return True

class BJ_Hand(cards.Hand):
	"""Playing cards for each player"""

	def __init__(self, name, wallet = 100):
		super(BJ_Hand, self).__init__()
		self.name = name
		self.wallet = wallet


	def __str__(self):
		rep = self.name + ":\t" + super(BJ_Hand, self).__str__()+ "And now have:" + str(self.wallet) + " money. The cards: "
		if self.total:
			rep += "(" + str(self.total) + ")"
		return rep

	@property
	def total(self):
		#if some card's value equal None, then entire property equal None
		for card in self.cards:
			if not card.value:
				return None

		#sum up the scores, each ace equal 1
		t = 0
		for card in self.cards:
			t += card.value

		#make sure, have any ace player
		contains_ace = False
		for card in self.cards:
			if card.value == BJ_Card.ACE_VALUE:
				contains_ace = True
		
		#if sum scores less than 11, then ace will be 11 points
		if contains_ace and t <= 11:
			t += 10
		return t

	def is_busted(self):
		return self.total > 21

	def bankrot_check(self):
		if self.wallet == 0:
			return True

	def bet(self):
		your_bet = 0
		while your_bet == 0:
			print(self.name, " have: ", self.wallet, " coins.")
			your_bet = int(input("How many coins you want to bet?"))
			if self.wallet < 0:
				print("You do not have enough coins!")
				your_bet = 0
			else: 
				self.wallet = self.wallet - your_bet

		return your_bet

	def money_add(self, money):
		self.wallet += money


class BJ_Player(BJ_Hand):
	""" blackjack player """

	def is_hitting(self):
		response = games.ask_yes_no("\n" + self.name + ", do you need one more card? (y/n): ")
		return response == "y"

	def bust (self):
		print(self.name, " busted!!")
		self.lose()

	def lose(self):
		print(self.name, " lost!")

	def win(self):
		print(self.name, " won!")

	def push(self):
		print(self.name, " has draw with cpu.")

	def bankrot(self):
		print(self.name, " player is bankrot and must leave the game.")

	

class BJ_Dealer(BJ_Hand):
	"""BJ dealer"""

	#extra coins for dealer
	def __init__(self, name, wallet = 150):
		super(BJ_Dealer, self).__init__(name, wallet)
		self.name = name
		self.wallet = wallet

	def is_hitting(self):
		return self.total < 17

	def bust(self):
		print(self.name, " busted!!")

	def win(self):
		print(self.name, " won!")

	def flip_first_card(self):
		first_card = self.cards[0]
		first_card.flip()

	def bankrot(self):
		print(self.name, " bankrot.")

	# bet for dealer
	def dealer_bet(self):
		your_bet = 0
		while your_bet == 0:
			print("Dealer have: ", self.wallet, " coins.")
			your_bet = random.randint(1, 70)
			self.wallet = self.wallet - your_bet
			if self.wallet < 0:
				print("You do not have enough coins!")
				your_bet = 0
		return your_bet

class BJ_Game(object):
	"""Blackjack game"""

	def __init__(self, names):
		self.players = []
		for name in names:
			player = BJ_Player(name)
			self.players.append(player)
		self.dealer = BJ_Dealer("Dealer")
		self.deck = BJ_Deck()
		self.deck.populate()
		self.deck.shuffle()

	@property
	def still_playing(self):
		sp = []
		for player in self.players:
			if not player.is_busted():
				sp.append(player)
		return sp

	def __additional_cards(self, player):
		while not player.is_busted() and player.is_hitting():
			self.deck.deal([player])
			print(player)
			if player.is_busted():
				player.bust()

	def game_over(self):
		print("Game Over!")

	def wallets_check(self):	
		#wallets check
		end = False
		for player in self.players:
			if player.bankrot_check() == True:
				player.bankrot()
				self.players.remove(player)
		if self.players == []:
			self.dealer.win()
			end = True
		if self.dealer.bankrot_check() == True:
			self.dealer.bankrot()
			for player in self.players:
				player.win()
				end = True
		return end

	def play(self):
		end = None

		#deck check
		if self.deck.check() == False:
			self.deck.clear()
			self.deck.populate()
			self.deck.shuffle()

		#take two cards to each player.
		self.deck.deal(self.players + [self.dealer], per_hand = 2)

		#first dealer's card must be overturn 
		self.dealer.flip_first_card()
		for player in self.players:
			print(player)
		print(self.dealer)

		#your bet please
		players_bets = 0
		for player in self.players:
			bet1 = player.bet()
			players_bets += bet1

		#dealer's bet
		dealer_bet_ = self.dealer.dealer_bet()

		#show bets
		print("Player's bet equal ", players_bets, ".")
		print("\n Dealer's bet ", dealer_bet_, ".")

		#distribution extra cards for players
		for player in self.players:
			self.__additional_cards(player)
		self.dealer.flip_first_card() #dealer's first card is open
		if not self.still_playing:
			#all the players is busted, only dealer's hand is show up
			print(self.dealer)
		else:
			#distrubtion extra cards for dealer
			print(self.dealer)
			self.__additional_cards(self.dealer)
			
			#variables for money distribution
			quantity_still_playing = len(self.still_playing)
			win_cash = dealer_bet_ / quantity_still_playing + players_bets / quantity_still_playing
			return_cash = players_bets / quantity_still_playing
			dealer_cash = players_bets + dealer_bet_
			
			if self.dealer.is_busted():
				#win everybody who still in a game
				win_cash = dealer_bet_/quantity_still_playing
				for player in self.still_playing:
					player.win()
					player.money_add(win_cash)

			elif self.still_playing == []:
						self.dealer.win()
						self.dealer.money_add(dealer_cash)
						dealer_bet_ = 0
						players_bets = 0
			else:
				#compare scores between the players, still in game
				#define win money for each player
				for player in self.still_playing:
					if player.total > self.dealer.total:
						player.win()
						player.money_add(win_cash)
					
					elif player.total < self.dealer.total:
						player.lose()
						self.dealer.win()
						self.dealer.money_add(dealer_cash)
						dealer_cash = 0

					else:
						player.push()
						player.money_add(return_cash)
						self.dealer.money_add(dealer_bet_)
						dealer_bet_ = 0

		#delete all bets
		players_bets = 0
		dealer_bet_ = 0

		#delete for all cards
		for player in self.players:
			player.clear()
		self.dealer.clear()
		
	

			

def main():
	print("\t\tWelcome to Blackjack game!\n")
	names = []
	number = games.ask_number("How many players will play the game? (1-7): ", low = 1, high = 8)

	for i in range(number):
		name = input("Enter player's name please: ")
		names.append(name)
		print()
	game = BJ_Game(names)
	again = None
	end = None
	while again != "n":
		while end != True:
			game.wallets_check()
			game.play()
		again = games.ask_yes_no("\nDo you want to play again (y/n)?")
	

main()
input("Press Enter for exit!")