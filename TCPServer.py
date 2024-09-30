from socket import *
import random

def makeDeck():
    card_suits = ["Hearts", 'Diamonds', 'Spades', 'Clubs']
    card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(val, suit) for val in card_values for suit in card_suits]   
    return deck

def addCards(cards):
    cardSum = sum(values(val) for val in cards)
    return cardSum

def playerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, dealer_score, connectionSocket, dealersDeck):
    gameGoesOn = True
    while gameGoesOn:
        # Show current game status
        print("----------------------------")
        print("Player shows: ", playerCards)
        print("Player score: ", playerSum)
        print("Dealer shows: ", dealerCards)
        print("Dealer score: ", dealerSum)
        print("----------------------------")

        # Prepare the message to send to the client
        message = [
            "----------------------------", "\n",
            "Player shows: ", str(playerCards), "\n",
            "Player score: ", playerSum, "\n",
            "Dealer shows: ", str(dealerCards[0]), "****", "\n",
            "Dealer score: ", dealer_score, "\n",
            "----------------------------", "\n",
            "Would you like to Hit or Stay?\n"
        ]

        message_str = " ".join(map(str, message))
        connectionSocket.send(message_str.encode())  # sends the card draw

        # Receive player's answer (hit or stay)
        answer = connectionSocket.recv(1024).decode()

        if answer.lower() == "stay":
            gameGoesOn = False
            # Call dealer's action and get the result
            reply = dealerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, dealer_score, connectionSocket, dealersDeck)

            # Determine the winner
            if playerSum > dealerSum:
                reply.append("You win\n")
            elif playerSum < dealerSum:
                reply.append("Dealer wins\n")
            else:
                reply.append("It's a tie!\n")

            # Convert the reply to a string and send it to the client
            message_str = " ".join(map(str, reply))
            connectionSocket.send(message_str.encode())

        elif answer.lower() == "hit":
            playerCards.append(dealersDeck.pop())
            playerSum = addCards(playerCards)

            if playerSum > 21:
                reply = "Player busts! Game over."
                print(reply)
                connectionSocket.send(reply.encode())
                gameGoesOn = False

def dealerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, dealer_score, connectionSocket, dealersDeck):
	dealersTurn = True
	while dealersTurn:
		if dealerSum < 17:
			dealerCards.append(dealersDeck.pop())
			dealerSum = addCards(dealerCards)
		elif dealerSum >= 17:
			print("----------------------------")
			print("Player shows: ", playerCards)
			print("Player score: ", playerSum)
			print("Dealer shows: ", dealerCards)
			print("Dealer score: ", dealerSum)
			print("----------------------------")

			# Prepare the message to send to the client
			message = [
				"----------------------------", "\n",
				"Player shows: ", str(playerCards), "\n",
				"Player score: ", playerSum, "\n",
				"Dealer shows: ", str(dealerCards[0]), "****", "\n",
				"Dealer score: ", dealer_score, "\n",
				"----------------------------", "\n",
			]
			return message

#def moreCardsDealer():
      

def values(val):
	if val[0] in ['Jack', 'Queen', 'King']:
		return 10
	elif val[0] == 'Ace':	
		return 11
	else:
		return int(val[0]) 


def main():
	print("Starting server...")
	serverPort = 16666
	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(('', serverPort))
	serverSocket.listen(5)
	print('The server is ready to receive')

	while True:
		connectionSocket, addr = serverSocket.accept()
		while True:
			sentence = connectionSocket.recv(1024).decode()  # yes or no

			if 'yes' == sentence:
				reply = "Okay, let's play a game.\n"
				connectionSocket.send(reply.encode())  # sends confirmation 

				dealersDeck = makeDeck()
				random.shuffle(dealersDeck)

				playerCards = []
				dealerCards = []

				# Deal initial cards
				playerCards.append(dealersDeck.pop())
				dealerCards.append(dealersDeck.pop())
				playerCards.append(dealersDeck.pop())
				dealerCards.append(dealersDeck.pop())

				playerSum = addCards(playerCards)
				dealerSum = addCards(dealerCards)
				dealer_score = values(dealerCards[0])
				if dealerSum == 21:
					youLose = "I won before the game even started to bad so sad.\n"
					connectionSocket.send(youLose.encode())  # sends confirmation 
					continue
				else:
					youLose = "I didn't win right way its go time.\n"
					connectionSocket.send(youLose.encode())  # sends confirmation 
				
				playerHitOrStay(playerCards, playerSum, dealerCards, dealerSum, dealer_score, connectionSocket, dealersDeck)
				
			elif 'no' == sentence:
				message = 'To bad I would have won.'
				connectionSocket.send(message.encode())
			else:
				message = 'Invalid input.'
				connectionSocket.send(message.encode())
        
		connectionSocket.close()  # Close the connection after the game            

if __name__ == '__main__':
    main()

