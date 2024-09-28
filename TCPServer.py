from socket import *
import random
serverPort = 16666
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)
print('The server is ready to receive')

card_suits = ["Hearts", 'Diamonds', 'Spades', 'Clubs']
card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
deck = [(val, suit) for val in card_values for suit in card_suits]

def values(val):
	if val[0] in ['Jack', 'Queen', 'King']:
		return 10
	elif val[0] == 'Ace':
		return 11
	else:
		return int(val[0]) 

while True:
	connectionSocket,addr = serverSocket.accept()
	random.shuffle(deck)
	player_card1 = [deck.pop()]
	p_card_val1 = (values(val) for val in player_card1)
	dealer_card1 = [deck.pop()]
	player_card2 = [deck.pop()]
	p_card_val2 = (values(val) for val in player_card2)
	dealer_card2 = [deck.pop()]

	player_sum = sum(values(val) for val in player_card1 + player_card2)
	dealer_sum = sum(values(val) for val in dealer_card1 + dealer_card2)
	dealer_score = sum(values(val) for val in dealer_card1)
	
	print("----------------------------")
	print("Player shows: ", player_card1, player_card2)
	print("Player score: ", player_sum)
	print("Dealer shows: ", dealer_card1, "****")
	print("Dealer score: ", dealer_score)
	print("----------------------------")


	
	sentence = int(connectionSocket.recv(1024).decode())
	if rn == sentence:
		message = 'correct'
		connectionSocket.send(message.encode())
		connectionSocket.close()
	else:
		message = 'incorrect'
		connectionSocket.send(message.encode())
	